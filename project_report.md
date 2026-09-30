# Project Report: Personal Expense Tracker

## Overview

The Personal Expense Tracker is a local, Python command-line application developed from the supplied interactive expense tracker. It records income and expenses, manages categories, supports transaction CRUD, and produces monthly summaries. The implementation uses Python's standard library and JSON persistence, so it runs without installing third-party packages.

## Objectives and scope

The project aims to make routine personal finance records easy to enter and review. It serves individual users who want a simple offline ledger. The application is not a bank integration, multi-user service, or financial advice tool.

## Architecture

| Module | Responsibility |
| --- | --- |
| `models.py` | Transaction representation and input validation |
| `storage.py` | JSON loading, defaults, and atomic persistence |
| `service.py` | Add/list/update/delete transactions and add categories |
| `analytics.py` | Monthly totals and category/highest expense analysis |
| `cli.py` | Command parsing, output, and error presentation |
| `__main__.py` | Enables `python -m expense_tracker` |
| `tests/test_tracker.py` | Unit tests for CRUD, validation, persistence, and analytics |

The boundaries keep command handling, domain operations, data persistence, and reporting independently understandable and maintainable.

## Functional modules

1. **Transaction management:** Create, retrieve, update, and delete income or expense records; filter by month, type, or category and search descriptions.
2. **Category management:** Add custom income and expense categories while retaining useful defaults.
3. **Analytics and reporting:** Calculate income, expenses, net balance, spending by category, and the highest expense for a month.

## Non-functional requirements

- **Error handling:** Reject invalid amount/date/category input and report malformed or inaccessible data clearly.
- **Logging:** Use Python logging for diagnostics and persistence failures; detailed logs can be enabled with `--verbose`.
- **Performance:** Use in-memory filtering and aggregation with linear time over the locally stored transaction list; no database server is required.
- **Maintainability:** Separate CLI, model, service, persistence, and analytics code into focused modules with type hints and docstrings.
- **Data integrity:** Write to a temporary file and atomically replace the JSON database after successful serialization.
- **Portability:** Use only the Python standard library and a configurable local data-file path.

## Technologies and execution

- Python 3.10+
- JSON for local persistence
- `argparse` for command-line parsing
- `decimal.Decimal` for monetary calculations
- `unittest` for unit tests

Start with `python -m expense_tracker --help`. Examples and the test command are documented in `README.md`.

## Testing

Unit tests cover transaction creation, update, delete, reload persistence, validation failures, and monthly calculations. Run them with `python -m unittest discover -s tests -v` from the project root. The test suite is included; it has not been executed as part of preparing this deliverable.

## GitHub deployment

The README contains the exact Git initialization, commit, remote, and push commands for `https://github.com/Pankhudi-28/Expense_Tracker`. The files are prepared locally. Publishing to GitHub is pending the user's approval, as requested.

## Limitations and future improvements

The JSON file is intended for personal local use and has no encryption or concurrent-writer coordination. Potential future additions include export to CSV, budgets, recurring transactions, and optional backup support.
