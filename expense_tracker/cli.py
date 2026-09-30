"""Command-line interface."""

import argparse
import logging
import os
from datetime import date
from decimal import Decimal

from .analytics import monthly_summary
from .service import Tracker
from .storage import JsonStore


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="expense-tracker", description="Track income and expenses locally.")
    root.add_argument("--database", default=os.environ.get("EXPENSE_TRACKER_DB", "finance_data.json"),
                      help="JSON database path (default: finance_data.json)")
    root.add_argument("--verbose", action="store_true", help="show diagnostic logs")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("add-expense", "add-income"):
        cmd = commands.add_parser(name)
        cmd.add_argument("amount"); cmd.add_argument("--category", required=True)
        cmd.add_argument("--date", default=date.today().isoformat())
        cmd.add_argument("--description", default=""); cmd.add_argument("--payment", default="Cash")
    listing = commands.add_parser("list")
    listing.add_argument("--type", choices=("Income", "Expense")); listing.add_argument("--month")
    listing.add_argument("--category"); listing.add_argument("--search")
    for name in ("update", "delete"):
        cmd = commands.add_parser(name); cmd.add_argument("id")
        if name == "update":
            cmd.add_argument("--amount"); cmd.add_argument("--date"); cmd.add_argument("--category")
            cmd.add_argument("--description"); cmd.add_argument("--payment")
    report = commands.add_parser("report"); report.add_argument("--month", default=date.today().strftime("%Y-%m"))
    cat = commands.add_parser("add-category"); cat.add_argument("type", choices=("Income", "Expense")); cat.add_argument("name")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING,
                        format="%(levelname)s: %(message)s")
    try:
        tracker = Tracker(JsonStore(args.database))
        if args.command in {"add-expense", "add-income"}:
            tx = tracker.add("Expense" if args.command == "add-expense" else "Income",
                             args.amount, args.category, args.date, args.description, args.payment)
            print(f"Recorded {tx.kind.lower()} {tx.id}: ₹{Decimal(tx.amount):,.2f}")
        elif args.command == "list":
            rows = tracker.list(args.type, args.month, args.category, args.search)
            if not rows:
                print("No matching transactions.")
            for tx in rows:
                print(f"{tx.id} | {tx.date} | {tx.kind:<7} | ₹{Decimal(tx.amount):>10,.2f} | {tx.category} | {tx.description}")
        elif args.command == "delete":
            tracker.delete(args.id); print("Transaction deleted.")
        elif args.command == "update":
            changes = {"amount": args.amount, "date": args.date, "category": args.category,
                       "description": args.description, "payment_method": args.payment}
            tx = tracker.update(args.id, **{key: value for key, value in changes.items() if value is not None})
            print(f"Updated transaction {tx.id}.")
        elif args.command == "add-category":
            tracker.add_category(args.type, args.name); print(f"Added {args.type.lower()} category: {args.name}")
        elif args.command == "report":
            summary = monthly_summary(tracker.data["transactions"], args.month)
            print(f"Monthly summary: {args.month}")
            print(f"Income:   ₹{summary['income']:,.2f}")
            print(f"Expenses: ₹{summary['expenses']:,.2f}")
            print(f"Balance:  ₹{summary['balance']:,.2f}")
            for category, amount in sorted(summary["categories"].items()):
                print(f"  {category}: ₹{amount:,.2f}")
            highest = summary["highest"]
            print(f"Highest expense: {highest.description or highest.category if highest else 'N/A'}"
                  f"{f' (₹{Decimal(highest.amount):,.2f})' if highest else ''}")
        return 0
    except (ValueError, OSError) as exc:
        logging.error("%s", exc)
        return 2
