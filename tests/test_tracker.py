"""Unit tests for transaction validation, CRUD, and monthly analytics."""

import tempfile
import unittest
from pathlib import Path

from expense_tracker.analytics import monthly_summary
from expense_tracker.service import Tracker
from expense_tracker.storage import JsonStore


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.tracker = Tracker(JsonStore(Path(self.temp.name) / "data.json"))

    def tearDown(self):
        self.temp.cleanup()

    def test_add_update_delete_and_reload(self):
        tx = self.tracker.add("Expense", "12.50", "Food", "2026-09-02", "Lunch")
        self.assertEqual(self.tracker.list()[0].amount, "12.50")
        self.tracker.update(tx.id, description="Dinner")
        self.assertEqual(Tracker(self.tracker.store).list()[0].description, "Dinner")
        self.tracker.delete(tx.id)
        self.assertEqual(self.tracker.list(), [])

    def test_rejects_invalid_amount_and_unknown_category(self):
        with self.assertRaises(ValueError):
            self.tracker.add("Expense", "-1", "Food")
        with self.assertRaises(ValueError):
            self.tracker.add("Expense", "1", "Unknown")

    def test_monthly_summary(self):
        self.tracker.add("Income", "1000", "Salary", "2026-09-01")
        self.tracker.add("Expense", "25.25", "Food", "2026-09-02")
        report = monthly_summary(self.tracker.list(), "2026-09")
        self.assertEqual(str(report["balance"]), "974.75")
        self.assertEqual(str(report["categories"]["Food"]), "25.25")


if __name__ == "__main__":
    unittest.main()
