from __future__ import annotations

from app.domain.money import Money
from app.interfaces.ports import PaymentGateway, PaymentResult


class FakePaymentGateway(PaymentGateway):
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail
        self.last_charge: tuple[str, Money] | None = None

    def charge(self, order_id: str, money: Money) -> PaymentResult:
        self.last_charge = (order_id, money)
        if self.should_fail:
            return PaymentResult(ok=False, error="payment declined")
        return PaymentResult(ok=True, transaction_id=f"tx_{order_id}")
