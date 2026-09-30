# Personal Expense Tracker

A dependency-free Python command-line application for recording personal income and expenses, maintaining categories, searching transactions, and reviewing monthly spending.

## Features

- Add income and expenses with dates, categories, notes, and payment methods.
- List, filter, search, update, and delete transactions.
- Add income or expense categories.
- Generate monthly income, expense, balance, category, and highest-expense summaries.
- Store data locally as readable JSON, with atomic saves to reduce corruption risk.
- Validate amounts and dates; report storage and input errors clearly.

## Technologies

Python 3.10 or newer; standard library only (`argparse`, `dataclasses`, `decimal`, `json`, `logging`, `unittest`, and related modules).

## Setup and use

No third-party packages or installation are required. From this directory:

```sh
python -m expense_tracker --help
```

Examples:

```sh
python -m expense_tracker add-expense 250 --category Food --date 2026-09-30 --description "Lunch" --payment UPI
python -m expense_tracker add-income 35000 --category Salary
python -m expense_tracker list --month 2026-09
python -m expense_tracker list --search lunch
python -m expense_tracker report --month 2026-09
python -m expense_tracker update TRANSACTION_ID --amount 275 --description "Lunch and tea"
python -m expense_tracker delete TRANSACTION_ID
python -m expense_tracker add-category Expense Travel
```

The default database is `finance_data.json` in the current directory. Select a different path with `--database path/to/data.json` or set `EXPENSE_TRACKER_DB`. Run `python -m expense_tracker --verbose ...` to show diagnostic logs. Amounts use decimal arithmetic and are stored to two decimal places. Dates must use `YYYY-MM-DD`; report and month filters use `YYYY-MM`.

## Tests

Run the unit tests from the project root:

```sh
python -m unittest discover -s tests -v
```

## Project layout

```text
expense-tracker/
├── expense_tracker/
│   ├── __init__.py
│   ├── __main__.py
│   ├── analytics.py
│   ├── cli.py
│   ├── models.py
│   ├── service.py
│   └── storage.py
├── tests/
│   └── test_tracker.py
├── README.md
└── statement.md
```

## GitHub deployment

After reviewing the files, run these commands in a shell from this project directory. They publish the project to the public repository named in the assignment. GitHub authentication must already be configured. If that repository already contains commits, first reconcile its history with `git pull --rebase origin main` before pushing.

```sh
git init
git branch -M main
git add README.md statement.md expense_tracker tests
git commit -m "Build modular Python expense tracker"
git remote add origin https://github.com/Pankhudi-28/Expense_Tracker.git
git push -u origin main
```

If `origin` already exists, use `git remote set-url origin https://github.com/Pankhudi-28/Expense_Tracker.git` instead of `git remote add origin ...`. A successful push makes the committed files visible on GitHub.
