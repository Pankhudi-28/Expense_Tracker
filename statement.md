# Problem Statement

People who track day-to-day finances manually can lose visibility into where money goes, how income compares with spending, and which expense categories account for the most. This project provides a simple local command-line tool to record and review that information.

## Scope

The application supports a single user's local transaction ledger. It stores data in a JSON file and provides transaction creation, retrieval, update and deletion, category management, filtering, and monthly summaries. It does not connect to banks, synchronize across devices, provide tax or investment advice, or encrypt the local data file.

## Target Users

Students, individuals, and households who want a lightweight offline tracker and are comfortable running Python commands.

## High-Level Features

- Record income and expenses with amount, date, category, description, and payment method.
- Review, search, filter, amend, and remove transactions.
- Add custom categories.
- Summarize monthly income, expenses, balance, category totals, and highest expense.
- Keep persistent, portable JSON data and provide clear validation and storage errors.
