from __future__ import annotations

from app.domain.order import Order
from app.interfaces.ports import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._db: dict[str, Order] = {}

    def get_by_id(self, order_id: str) -> Order:
        if order_id not in self._db:
            raise KeyError(f"Order not found: {order_id}")
        return self._db[order_id]

    def save(self, order: Order) -> None:
        self._db[order.order_id] = order

    def add(self, order: Order) -> None:
        self.save(order)
