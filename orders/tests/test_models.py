import pytest
from accounts.models import User
from orders.models import Order, OrderItem
from products.models import Product
from decimal import Decimal

@pytest.mark.django_db
def test_order_creation_default_status():
    user = User.objects.create_user(
        username="orderuser",
        email="order@example.com",
        password="pass123"
    )

    order = Order.objects.create(user=user)

    assert order.user == user
    assert order.status == "CREATED"


@pytest.mark.django_db
def test_order_item_creation():
    user = User.objects.create_user(
        username="itemuser",
        email="item@example.com",
        password="pass123"
    )

    product = Product.objects.create(
        name="Test Product",
        price=Decimal("100.00"),
        stock=10
    )

    order = Order.objects.create(user=user)

    item = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=2
    )

    assert item.order == order
    assert item.product == product
    assert item.quantity == 2
