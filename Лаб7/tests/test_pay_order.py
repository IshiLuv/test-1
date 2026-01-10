import pytest

from app.application.pay_order import PayOrderUseCase
from app.domain.order import Order, OrderStatus
from app.infrastructure.fake_gateway import FakePaymentGateway
from app.infrastructure.in_memory_repo import InMemoryOrderRepository


def test_success_payment():
    repo = InMemoryOrderRepository()
    gw = FakePaymentGateway(should_fail=False)
    uc = PayOrderUseCase(repo, gw)

    order = Order("o1", currency="USD")
    order.add_line("p1", qty=2, price_amount=50)
    order.add_line("p2", qty=1, price_amount=30)
    repo.add(order)

    res = uc.execute("o1")
    assert res.ok is True
    assert repo.get_by_id("o1").status == OrderStatus.PAID
    assert gw.last_charge[1].amount == 130


def test_cannot_pay_empty_order():
    repo = InMemoryOrderRepository()
    gw = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gw)

    repo.add(Order("empty", currency="USD"))

    with pytest.raises(ValueError, match="Cannot pay empty order"):
        uc.execute("empty")


def test_cannot_pay_twice():
    repo = InMemoryOrderRepository()
    gw = FakePaymentGateway()
    uc = PayOrderUseCase(repo, gw)

    order = Order("o2", currency="USD")
    order.add_line("p1", qty=1, price_amount=10)
    repo.add(order)

    assert uc.execute("o2").ok is True
    with pytest.raises(ValueError, match="already paid"):
        uc.execute("o2")


def test_cannot_modify_lines_after_payment():
    order = Order("o3", currency="USD")
    order.add_line("p1", qty=1, price_amount=10)
    order.pay()

    with pytest.raises(ValueError, match="Cannot modify order after payment"):
        order.add_line("p2", qty=1, price_amount=10)

    with pytest.raises(ValueError, match="Cannot modify order after payment"):
        order.remove_line("p1")


def test_total_equals_sum_of_lines():
    order = Order("o4", currency="USD")
    order.add_line("p1", qty=3, price_amount=10)
    order.add_line("p2", qty=2, price_amount=7)
    assert order.total.amount == 44
