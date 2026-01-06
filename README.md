# Local Reporting Mini-System (Python)

This project implements a **local reporting mini-system** that reads a CSV file of transactions, normalizes and validates the data, generates a **single monthly XML report**, and optionally sends an **automated email** with a concise technical summary and alerts.

The system runs entirely **locally** and supports **two execution modes**:
- **CLI (Command Line Interface)** — required
- **Local REST API (FastAPI)** — chosen option

---

## Features

- Read input CSV (`transactions.csv`)
- Normalize and validate transaction data
- Handle mixed timestamp formats safely
- Generate a single XML report per month
- Generate summary metrics in JSON format
- Send email notification with XML attachment
- Expose a REST endpoint to trigger execution locally

---

## Project Structure

```text
local-reporting/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   └── transactions.csv
├── outputs/
│   └── <YYYYMM>/
│       ├── report.xml
│       └── summary.json
└── src/
    ├── __init__.py
    ├── api.py
    ├── config.py
    ├── emailer.py
    ├── io_csv.py
    ├── normalize.py
    ├── report_xml.py
    ├── runner.py
    └── summary.py


Requirements

Python 3.10+

Local execution (no cloud dependencies)

Setup
1. Create and activate a virtual environment

Windows (PowerShell):

python -m venv .venv
.venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Configure environment variables

Copy the example file:

copy .env.example .env


Edit .env with your SMTP credentials:

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=destination_email@gmail.com

DEFAULT_CURRENCY=BRL
MIN_AMOUNT=1.00


Note: If using Gmail, an App Password is required.
Never commit .env to the repository.

Run via CLI (Required)

Generate a report for a given month:

python app.py --month=2023-08 --input=./data/transactions.csv --output=./outputs


Generate a report and send email notification:

python app.py --month=2023-08 --send-email

Run via REST API (FastAPI)
Start the API server
python -m uvicorn src.api:app --reload --port 8000

Swagger UI

Access the interactive API documentation:

http://127.0.0.1:8000/docs

Trigger execution

Endpoint:

POST /run?month=YYYY-MM


Example request body:

{
  "input_path": "./data/transactions.csv",
  "output_dir": "./outputs",
  "send_email": false
}

Outputs

Generated files:

outputs/<YYYYMM>/report.xml — XML report with all valid transactions

outputs/<YYYYMM>/summary.json — metrics and alerts summary

Input CSV Notes

The input CSV does not fully match the target schema.
Some columns are mapped or derived during normalization:

transaction_code → id

timestamp → date

amount_brl → amount

category → type

Timestamp Handling

The CSV contains mixed timestamp formats, including:

DD-MM-YYYY

YYYY-MM-DD 0:00:00 (single-digit hour)

To avoid invalid dates, timestamps are normalized before parsing by:

Padding single-digit hours

Applying explicit parsing strategies for each format

AI Usage (Mandatory)

AI assistance was used as a development accelerator, not as a replacement for decision-making.

How AI was used

Project structure and module separation

Boilerplate generation for CLI, REST API, XML generation, and SMTP email

Suggestions for normalization rules and summary metrics

Debugging runtime errors and edge cases (e.g., mixed timestamps)

Human validation

All business rules, data mappings, and edge cases were manually validated through local execution and inspection of generated outputs.

Key Prompts Used (Examples)

“Design a local reporting system with CLI and REST execution.”

“Write a robust pandas normalization pipeline with validation and metrics.”

“Generate XML using ElementTree with a TransactionsReport root.”

“Implement SMTP email sending with attachment and summary.”

“Propose a strategy to parse mixed timestamp formats safely.”

Security Notes

Do not commit .env or credentials

Revoke and regenerate SMTP App Passwords if exposed

Generated outputs can be ignored or versioned selectively