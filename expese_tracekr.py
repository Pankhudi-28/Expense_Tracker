import json
from datetime import datetime
from pathlib import Path

# Local database file
DB_FILE = Path("finance_data.json")

DEFAULT_CATEGORIES = {
    "Expense": ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Healthcare", "Education", "Other"],
    "Income": ["Salary", "Freelance", "Investments", "Gift", "Other"],
}

DEFAULT_PAYMENT_METHODS = ["Cash", "UPI", "Credit Card", "Debit Card", "Net Banking"]


def load_db():
    """Fetch stored finance data or return clean defaults if missing/corrupt."""
    if DB_FILE.is_file():
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not parse database file. Starting fresh.")
    
    return {
        "transactions": [],
        "categories": DEFAULT_CATEGORIES,
        "payment_methods": DEFAULT_PAYMENT_METHODS,
    }


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def display_dashboard(db):
    print("\n" + "=" * 40)
    print("         MONTHLY DASHBOARD")
    print("=" * 40)

    target_month = input("Enter month (YYYY-MM) or hit Enter for current month: ").strip()
    if not target_month:
        target_month = datetime.now().strftime("%Y-%m")

    income = 0.0
    expenses = 0.0
    category_breakdown = {}
    top_expense = {"amount": 0.0, "desc": "N/A"}

    for tx in db["transactions"]:
        if not tx["date"].startswith(target_month):
            continue

        amt = tx["amount"]
        if tx["type"] == "Income":
            income += amt
        elif tx["type"] == "Expense":
            expenses += amt
            cat = tx["category"]
            category_breakdown[cat] = category_breakdown.get(cat, 0.0) + amt

            if amt > top_expense["amount"]:
                top_expense = {"amount": amt, "desc": tx["description"] or "Unnamed expense"}

    net_balance = income - expenses

    print(f"\nSummary for: {target_month}")
    print("-" * 30)
    print(f"Total Income    : ₹{income:,.2f}")
    print(f"Total Expenses  : ₹{expenses:,.2f}")
    print("-" * 30)
    print(f"Current Balance : ₹{net_balance:,.2f}")
    print("-" * 30)

    if category_breakdown:
        top_cat = max(category_breakdown, key=category_breakdown.get)
        print(f"Top Category    : {top_cat} (₹{category_breakdown[top_cat]:,.2f})")
    else:
        print("Top Category    : N/A")

    print(f"Highest Expense : {top_expense['desc']} (₹{top_expense['amount']:,.2f})")
    print("=" * 40)


def add_transaction(db, kind):
    print(f"\n--- Add {kind} ---")

    try:
        amount = float(input("Enter amount (₹): "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid number format.")
        return

    date_str = input("Date (YYYY-MM-DD) [Enter for today]: ").strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Aborting entry.")
            return

    # Select Category
    available_cats = db["categories"][kind]
    print("\nAvailable Categories:")
    for i, cat in enumerate(available_cats, start=1):
        print(f"  {i}. {cat}")

    try:
        cat_idx = int(input("Select category number: ")) - 1
        category = available_cats[cat_idx]
    except (ValueError, IndexError):
        print("Invalid category selection.")
        return

    note = input("Description/Notes: ").strip()

    # Select Payment Method
    methods = db.get("payment_methods", DEFAULT_PAYMENT_METHODS)
    print("\nPayment Methods:")
    for i, method in enumerate(methods, start=1):
        print(f"  {i}. {method}")

    try:
        pm_idx = int(input("Select payment method: ")) - 1
        pay_method = methods[pm_idx]
    except (ValueError, IndexError):
        pay_method = "Cash"  # Fallback

    new_tx = {
        "id": len(db["transactions"]) + 1,
        "type": kind,
        "amount": amount,
        "date": date_str,
        "category": category,
        "description": note,
        "payment_method": pay_method,
    }

    db["transactions"].append(new_tx)
    save_db(db)
    print(f"\nLogged! {kind} of ₹{amount:,.2f} recorded.")


def view_transactions(db):
    transactions = db.get("transactions", [])
    if not transactions:
        print("\nNo transactions logged yet.")
        return

    print("\n--- View Transactions ---")
    print("1. All")
    print("2. Filter by Month (YYYY-MM)")
    print("3. Filter by Category")
    print("4. Filter by Payment Method")
    print("5. Search Description")

    choice = input("Option: ").strip()
    results = list(transactions)

    if choice == "2":
        query = input("Enter month (YYYY-MM): ").strip()
        results = [t for t in results if t["date"].startswith(query)]
    elif choice == "3":
        query = input("Enter category: ").strip().lower()
        results = [t for t in results if t["category"].lower() == query]
    elif choice == "4":
        query = input("Enter payment method: ").strip().lower()
        results = [t for t in results if t["payment_method"].lower() == query]
    elif choice == "5":
        query = input("Search term: ").strip().lower()
        results = [t for t in results if query in t["description"].lower()]

    if not results:
        print("\nNo matching records found.")
        return

    header = f"\n{'ID':<4} | {'Type':<8} | {'Amount':<10} | {'Date':<10} | {'Category':<15} | {'Method':<12} | {'Description'}"
    print(header)
    print("-" * len(header) + "-----------")

    for t in results:
        print(f"{t['id']:<4} | {t['type']:<8} | ₹{t['amount']:<9.2f} | {t['date']:<10} | {t['category']:<15} | {t['payment_method']:<12} | {t['description']}")


def manage_categories(db):
    print("\n--- Manage Categories ---")
    print("1. View Categories")
    print("2. Add Category")
    print("3. Rename Category")
    print("4. Delete Category")
    choice = input("Choice: ").strip()

    kind = "Expense" if input("Is this for Expense or Income? (e/i): ").strip().lower() == "e" else "Income"
    cats = db["categories"][kind]

    if choice == "1":
        print(f"\n{kind} Categories:")
        for cat in cats:
            print(f" - {cat}")

    elif choice == "2":
        new_name = input("New category name: ").strip()
        if new_name and new_name not in cats:
            cats.append(new_name)
            save_db(db)
            print(f"Added '{new_name}'.")
        else:
            print("Invalid or existing category name.")

    elif choice == "3":
        for i, c in enumerate(cats, 1):
            print(f"{i}. {c}")
        try:
            idx = int(input("Select category number: ")) - 1
            old_name = cats[idx]
            new_name = input(f"Rename '{old_name}' to: ").strip()

            if new_name:
                cats[idx] = new_name
                # Bulk update existing transaction categories
                for tx in db["transactions"]:
                    if tx["category"] == old_name:
                        tx["category"] = new_name
                save_db(db)
                print("Category updated across all entries.")
        except (ValueError, IndexError):
            print("Invalid selection.")

    elif choice == "4":
        for i, c in enumerate(cats, 1):
            print(f"{i}. {c}")
        try:
            idx = int(input("Select category number to remove: ")) - 1
            removed = cats.pop(idx)
            save_db(db)
            print(f"Deleted '{removed}'. Existing transactions were untouched.")
        except (ValueError, IndexError):
            print("Invalid selection.")


def main():
    db = load_db()

    actions = {
        "1": lambda: display_dashboard(db),
        "2": lambda: add_transaction(db, "Expense"),
        "3": lambda: add_transaction(db, "Income"),
        "4": lambda: view_transactions(db),
        "5": lambda: manage_categories(db),
    }

    while True:
        print("\n" + "=" * 30)
        print("    PERSONAL FINANCE TRACKER")
        print("=" * 30)
        print("1. Monthly Dashboard")
        print("2. Add Expense")
        print("3. Add Income")
        print("4. View / Search Transactions")
        print("5. Manage Categories")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "6":
            print("\nGoodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid input. Please choose between 1 and 6.")


if __name__ == "__main__":
    main()
