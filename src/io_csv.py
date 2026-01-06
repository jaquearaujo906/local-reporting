import pandas as pd

REQUIRED_COLS = {"id", "status", "date", "amount", "type", "merchantid", "network", "category"}

def read_transactions_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # normaliza nomes das colunas
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    rename_map = {
        "transaction_code": "id",
        "timestamp": "date",
        "amount_brl": "amount",
        "merchant_id": "merchantid",
    }

    df = df.rename(columns=rename_map)

    if "type" not in df.columns and "category" in df.columns:
        df["type"] = df["category"]

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns after mapping: {sorted(missing)}")

    return df
