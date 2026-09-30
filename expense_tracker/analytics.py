"""Monthly summaries and category analytics."""

from collections import defaultdict
from decimal import Decimal

from .models import Transaction


def monthly_summary(transactions: list[Transaction], month: str) -> dict[str, object]:
    rows = [tx for tx in transactions if tx.date.startswith(month)]
    income = sum((Decimal(tx.amount) for tx in rows if tx.kind == "Income"), Decimal("0"))
    expenses = sum((Decimal(tx.amount) for tx in rows if tx.kind == "Expense"), Decimal("0"))
    categories: dict[str, Decimal] = defaultdict(Decimal)
    for tx in rows:
        if tx.kind == "Expense":
            categories[tx.category] += Decimal(tx.amount)
    highest = max((tx for tx in rows if tx.kind == "Expense"),
                  key=lambda tx: Decimal(tx.amount), default=None)
    return {"month": month, "income": income, "expenses": expenses,
            "balance": income - expenses, "categories": dict(categories), "highest": highest}
