
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from orders.models import Order
from .services import create_payment
from .serializers import PaymentSerializer


class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")

        if not order_id:
            raise ValidationError("order_id is required")

        try:
            order = Order.objects.get(
                id=order_id,
                user=request.user
            )
        except Order.DoesNotExist:
            raise ValidationError("Invalid order")

        if hasattr(order, "payment"):
            raise ValidationError("Payment already done")

        try:
            payment = create_payment(order)
        except ValueError as e:
            raise ValidationError(str(e))

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)