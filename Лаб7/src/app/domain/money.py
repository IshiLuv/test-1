from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money.amount must be >= 0")
        if not self.currency:
            raise ValueError("Money.currency is required")

    def add(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def mul_int(self, k: int) -> "Money":
        if k < 0:
            raise ValueError("Multiplier must be >= 0")
        return Money(self.amount * k, self.currency)

    def _assert_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
