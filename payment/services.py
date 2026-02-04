 

from asgiref.sync import async_to_sync
from decimal import Decimal
from django.db import transaction
from django.core.cache import cache

from .models import Payment
from .integrations import async_payment_gateway
from .tasks import send_order_confirmation_email


def create_payment(order):
    with transaction.atomic():
        amount = Decimal("0.00")

        for item in order.items.select_related("product"):
            product = item.product

            if product.stock < item.quantity:
                raise ValueError(f"Insufficient stock for {product.name}")

            product.stock -= item.quantity
            product.save(update_fields=["stock"])

            amount += product.price * item.quantity

        #  ASYNC PAYMENT GATEWAY CALL (CORRECT WAY)
        response = async_to_sync(async_payment_gateway)(amount)

        if response["status"] != "success":
            raise ValueError("Payment failed")

        payment = Payment.objects.create(
            order=order,
            amount=amount,
            status="success"
        )

        order.status = "PAID"
        order.save(update_fields=["status"])

        send_order_confirmation_email.delay(order.id)

        for item in order.items.select_for_update():
            product = item.product
            product.stock -= item.quantity
            product.save(update_fields=["stock"])

            cache.delete("products:list")
            cache.delete(f"products:detail:{product.id}")

        return payment
