from __future__ import annotations

from app.interfaces.ports import OrderRepository, PaymentGateway, PaymentResult


class PayOrderUseCase:
    def __init__(self, repo: OrderRepository, gateway: PaymentGateway) -> None:
        self._repo = repo
        self._gateway = gateway

    def execute(self, order_id: str) -> PaymentResult:
        order = self._repo.get_by_id(order_id)

        amount_to_charge = order.pay()

        payment = self._gateway.charge(order_id, amount_to_charge)
        if not payment.ok:
            order.status = order.status.DRAFT
            return payment

        self._repo.save(order)
        return payment
