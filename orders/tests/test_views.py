import pytest
from rest_framework.test import APIClient
from decimal import Decimal
from accounts.models import User
from orders.models import Order
from products.models import Product


@pytest.mark.django_db
def test_create_order_authenticated_user():
    client = APIClient()

    user = User.objects.create_user(
        username="apiorderuser",
        email="apiorder@example.com",
        password="pass123"
    )

    product = Product.objects.create(
        name="Test Product",
        price=Decimal("100.00"),
        stock=10
    )

    client.force_authenticate(user=user)

    response = client.post(
        "/api/orders/create/",
        data={
            "items": [
                {
                    "product": product.id,
                    "quantity": 2
                }
            ]
        },
        format="json"
    )

    assert response.status_code == 201
    assert response.data["status"] == "CREATED"
    assert Order.objects.filter(user=user).count() == 1
