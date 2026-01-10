from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from app.domain.money import Money


class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    PAID = "PAID"


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    qty: int
    price: Money

    def __post_init__(self) -> None:
        if not self.product_id:
            raise ValueError("product_id is required")
        if self.qty <= 0:
            raise ValueError("qty must be > 0")

    @property
    def subtotal(self) -> Money:
        return self.price.mul_int(self.qty)


@dataclass
class Order:
    order_id: str
    currency: str = "USD"
    status: OrderStatus = OrderStatus.DRAFT
    _lines: List[OrderLine] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.order_id:
            raise ValueError("order_id is required")
        if not self.currency:
            raise ValueError("currency is required")

    @property
    def lines(self) -> List[OrderLine]:
        return list(self._lines)

    def add_line(self, product_id: str, qty: int, price_amount: int) -> None:
        self._assert_mutable()
        line = OrderLine(
            product_id=product_id,
            qty=qty,
            price=Money(price_amount, self.currency),
        )
        self._lines.append(line)

    def remove_line(self, product_id: str) -> None:
        self._assert_mutable()
        self._lines = [l for l in self._lines if l.product_id != product_id]

    @property
    def total(self) -> Money:
        total = Money(0, self.currency)
        for l in self._lines:
            if l.price.currency != self.currency:
                raise ValueError("Order line currency mismatch")
            total = total.add(l.subtotal)
        return total

    def pay(self) -> Money:
        if self.status == OrderStatus.PAID:
            raise ValueError("Order is already paid")
        if len(self._lines) == 0:
            raise ValueError("Cannot pay empty order")
        self.status = OrderStatus.PAID
        return self.total

    def _assert_mutable(self) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify order after payment")
