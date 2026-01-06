# Local Reporting Mini-System (Python)

This project reads a CSV of transactions, normalizes/validates the data, generates a **single monthly XML report**, and can send an **automated email** with a concise technical summary + alerts and the XML attached. Everything runs locally.

It supports **two invocation modes**:
- **CLI** (required)
- **Local REST API** using FastAPI (chosen option)

---

## Features

- Read input CSV (`transactions.csv`)
- Normalize + validate data (including mixed timestamp formats)
- Generate one XML report per month:
  - `outputs/<YYYYMM>/report.xml`
- Generate summary metrics (JSON):
  - `outputs/<YYYYMM>/summary.json`
- Send email via SMTP with:
  - Subject: `Transactional Report — YYYY-MM`
  - Body: technical summary + alerts
  - Attachment: `report.xml`
- REST endpoint to trigger execution locally

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
```

---

## Requirements

- Python 3.10+ (works on Windows/macOS/Linux)

Internet access is not required for processing (only for SMTP email delivery).

---

## Setup

1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux (bash/zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Configure environment variables

Copy `.env.example` to `.env` and fill values:

Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Example `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=destination_email@gmail.com

DEFAULT_CURRENCY=BRL
MIN_AMOUNT=1.00
```

Note: If using Gmail, you typically need an App Password (requires 2-Step Verification). Do not commit `.env` to Git.

---

## Run via CLI (Required)

Generate report for a given month:

```bash
python app.py --month=2023-08 --input=./data/transactions.csv --output=./outputs
```

Generate report and send email:

```bash
python app.py --month=2023-08 --send-email
```

---

## Run via REST API (Chosen Option)

Start the local API:

```bash
python -m uvicorn src.api:app --reload --port 8000
```

Swagger UI:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Trigger execution:

POST `/run?month=YYYY-MM`

Example request body:

```json
{
  "input_path": "./data/transactions.csv",
  "output_dir": "./outputs",
  "send_email": false
}
```

---

## Outputs

- `outputs/<YYYYMM>/report.xml`  
  A single XML file containing all reportable transactions for the month.

- `outputs/<YYYYMM>/summary.json`  
  Metrics used for the technical email summary (e.g., `rows_in`, `rows_out`, `invalid_date`, etc.).

---

## Normalization Notes (High-Level)

- CSV columns are mapped to a standard internal schema (e.g., `transaction_code → id`, `timestamp → date`, `amount_brl → amount`).
- Mixed timestamp formats are supported (e.g., `DD-MM-YYYY` and `YYYY-MM-DD 0:00:00`).
- Transactions are filtered by the requested month (`YYYY-MM`).
- Amount is converted to numeric.
- `MerchantId` is cleaned to keep digits only.
- Metrics are produced for observability and email alerts.

---

## AI Usage (Mandatory)

AI assistance was used during development to speed up implementation and improve robustness. It was used to:

- Propose project structure and module responsibilities
- Draft boilerplate for CLI, REST API, XML generation, and SMTP email sending
- Suggest normalization rules and metrics for the summary report
- Help identify and fix edge cases during debugging (e.g., mixed timestamp formats and single-digit hour `0:00:00`)
- Improve documentation clarity

---

## Key Prompts Used (examples)

- “Design a local reporting system with CLI + REST execution, CSV normalization, XML output, and email notification.”
- “Write a robust pandas normalization function with month filtering, validation, duplicate handling, and summary metrics.”
- “Generate XML output using ElementTree with a TransactionsReport root and Transaction entries.”
- “Implement SMTP email sending with a concise technical summary and XML attachment.”
- “Propose a robust strategy to parse mixed timestamps like 02-08-2023 and 2023-08-12 0:00:00.”

---

## Security Note

Never commit `.env` to GitHub.

If an SMTP password/app password was exposed, revoke it and create a new one.

---

## Author

Jaqueline Araújo Xavier