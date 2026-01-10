from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.domain.money import Money
from app.domain.order import Order


@dataclass(frozen=True)
class PaymentResult:
    ok: bool
    transaction_id: str | None = None
    error: str | None = None


class OrderRepository(Protocol):
    def get_by_id(self, order_id: str) -> Order: ...
    def save(self, order: Order) -> None: ...


class PaymentGateway(Protocol):
    def charge(self, order_id: str, money: Money) -> PaymentResult: ...
