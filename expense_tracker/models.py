"""Validated transaction data models."""

from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import uuid4


@dataclass
class Transaction:
    id: str
    kind: str
    amount: str
    date: str
    category: str
    description: str = ""
    payment_method: str = "Cash"

    @classmethod
    def create(cls, kind: str, amount: Any, when: str, category: str,
               description: str = "", payment_method: str = "Cash") -> "Transaction":
        kind = kind.strip().title()
        if kind not in {"Income", "Expense"}:
            raise ValueError("type must be Income or Expense")
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("amount must be a number") from None
        if not value.is_finite() or value <= 0:
            raise ValueError("amount must be a finite positive number")
        try:
            date.fromisoformat(when)
        except (TypeError, ValueError):
            raise ValueError("date must use YYYY-MM-DD format") from None
        category = category.strip()
        if not category:
            raise ValueError("category cannot be empty")
        return cls(str(uuid4()), kind, format(value.quantize(Decimal("0.01")), "f"),
                   when, category, description.strip(), payment_method.strip() or "Cash")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Transaction":
        return cls(**{key: data[key] for key in cls.__dataclass_fields__})

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
