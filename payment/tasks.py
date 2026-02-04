from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order


@shared_task
def send_order_confirmation_email(order_id):
    order = Order.objects.select_related("user").prefetch_related(
        "items__product"
    ).get(id=order_id)

    subject = f"Order Confirmation - Order #{order.id}"

    lines = [
        f"Hello {order.user.username},",
        "",
        f"Your order #{order.id} has been successfully placed.",
        "",
        "Order Details:",
    ]

    total = 0
    for item in order.items.all():
        item_total = item.product.price * item.quantity
        total += item_total
        lines.append(
            f"- {item.product.name} | Qty: {item.quantity} | "
            f"Price: {item.product.price} | Total: {item_total}"
        )

    lines.extend([
        "",
        f"Total Amount Paid: {total}",
        "",
        "Thank you for shopping with us!",
        "Smart Order Processing System"
    ])

    send_mail(
        subject,
        "\n".join(lines),
        None,
        [order.user.email],
        fail_silently=False,
    )
