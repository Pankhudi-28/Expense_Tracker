"""Transaction CRUD and category operations."""

from datetime import date

from .models import Transaction
from .storage import JsonStore


class Tracker:
    def __init__(self, store: JsonStore):
        self.store = store
        self.data = store.load()

    def add(self, kind: str, amount: str, category: str, when: str | None = None,
            description: str = "", payment_method: str = "Cash") -> Transaction:
        categories = self.data["categories"].get(kind.title(), [])
        if category not in categories:
            raise ValueError(f"unknown {kind.lower()} category: {category}")
        tx = Transaction.create(kind, amount, when or date.today().isoformat(), category,
                                description, payment_method)
        self.data["transactions"].append(tx)
        self.store.save(self.data)
        return tx

    def list(self, kind: str | None = None, month: str | None = None,
             category: str | None = None, search: str | None = None) -> list[Transaction]:
        rows = self.data["transactions"]
        return [tx for tx in rows
                if (not kind or tx.kind.lower() == kind.lower())
                and (not month or tx.date.startswith(month))
                and (not category or tx.category.lower() == category.lower())
                and (not search or search.lower() in tx.description.lower())]

    def update(self, transaction_id: str, **changes: str) -> Transaction:
        allowed = {"amount", "date", "category", "description", "payment_method"}
        if set(changes) - allowed:
            raise ValueError("only amount, date, category, description and payment_method can be updated")
        tx = self._find(transaction_id)
        category = changes.get("category", tx.category)
        if category not in self.data["categories"].get(tx.kind, []):
            raise ValueError(f"unknown {tx.kind.lower()} category: {category}")
        updated = Transaction.create(tx.kind, changes.get("amount", tx.amount),
                                     changes.get("date", tx.date), category,
                                     changes.get("description", tx.description),
                                     changes.get("payment_method", tx.payment_method))
        tx.amount, tx.date, tx.category = updated.amount, updated.date, updated.category
        tx.description, tx.payment_method = updated.description, updated.payment_method
        self.store.save(self.data)
        return tx

    def delete(self, transaction_id: str) -> None:
        tx = self._find(transaction_id)
        self.data["transactions"].remove(tx)
        self.store.save(self.data)

    def add_category(self, kind: str, name: str) -> None:
        key, name = kind.title(), name.strip()
        if key not in self.data["categories"] or not name:
            raise ValueError("type must be Income or Expense and category cannot be empty")
        if any(existing.lower() == name.lower() for existing in self.data["categories"][key]):
            raise ValueError("category already exists")
        self.data["categories"][key].append(name)
        self.store.save(self.data)

    def _find(self, transaction_id: str) -> Transaction:
        for tx in self.data["transactions"]:
            if tx.id == transaction_id:
                return tx
        raise ValueError(f"transaction not found: {transaction_id}")
