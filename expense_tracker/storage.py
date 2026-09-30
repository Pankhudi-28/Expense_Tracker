"""JSON persistence with atomic writes and defensive loading."""

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

from .models import Transaction

LOG = logging.getLogger(__name__)
DEFAULT_CATEGORIES = {
    "Expense": ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Healthcare", "Education", "Other"],
    "Income": ["Salary", "Freelance", "Investments", "Gift", "Other"],
}


class JsonStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"transactions": [], "categories": {k: v.copy() for k, v in DEFAULT_CATEGORIES.items()}}
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict) or not isinstance(raw.get("transactions"), list) or not isinstance(raw.get("categories"), dict):
                raise ValueError("database must contain transaction and category lists")
            raw["transactions"] = [Transaction.from_dict(item) for item in raw["transactions"]]
            return raw
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError, AttributeError) as exc:
            LOG.error("Cannot read database %s: %s", self.path, exc)
            raise ValueError(f"database is invalid or unreadable: {self.path}") from exc

    def save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"transactions": [tx.to_dict() for tx in data["transactions"]],
                   "categories": data["categories"]}
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=self.path.parent,
                                             delete=False, newline="\n") as temp:
                temp_name = temp.name
                json.dump(payload, temp, ensure_ascii=False, indent=2)
                temp.write("\n")
            os.replace(temp_name, self.path)
        except OSError:
            if temp_name and os.path.exists(temp_name):
                os.unlink(temp_name)
            LOG.exception("Could not save database %s", self.path)
            raise
