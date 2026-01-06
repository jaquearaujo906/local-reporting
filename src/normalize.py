import pandas as pd

ALLOWED_STATUS = {"approved", "chargeback", "declined", "refunded"}
ALLOWED_TYPE = {"DEBIT", "CREDIT"}

def _parse_amount(x):
    if pd.isna(x):
        return None
    s = str(x).strip()

    # remove símbolos
    s = s.replace("R$", "").replace(" ", "")

    # lida com formatos "9.766,46" e "9766.46"
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s and "." not in s:
        s = s.replace(",", ".")

    try:
        return float(s)
    except ValueError:
        return None

def normalize_transactions(df: pd.DataFrame, month: str, min_amount: float):
    metrics = {
        "month": month,
        "rows_in": len(df),
        "rows_out": 0,
        "invalid_date": 0,
        "invalid_amount": 0,
        "invalid_status": 0,
        "invalid_type": 0,
        "below_threshold_excluded": 0,
        "duplicates_removed": 0,
    }

    work = df.copy()

    work["merchantid"] = work["merchantid"].astype(str).str.replace(r"\D", "", regex=True)

    # date parsing (soluciona vários formatos)
    raw_date = work["date"].astype(str).str.strip()

    # remove espaços 
    raw_date = raw_date.str.replace("\u00a0", " ", regex=False)

    # padroniza hora de "0:00:00" -> "00:00:00" 
    raw_date = raw_date.str.replace(r" (\d):", r" 0\1:", regex=True)

    # 1) formato ISO com hora: 2023-08-12 00:00:00
    dt_iso_time = pd.to_datetime(raw_date, format="%Y-%m-%d %H:%M:%S", errors="coerce")

    # 2) formato ISO só data: 2023-08-12
    dt_iso_date = pd.to_datetime(raw_date, format="%Y-%m-%d", errors="coerce")

    # 3) formato BR: 02-08-2023
    dt_br = pd.to_datetime(raw_date, format="%d-%m-%Y", errors="coerce")

    work["date_parsed"] = dt_iso_time.fillna(dt_iso_date).fillna(dt_br)
    metrics["invalid_date"] = int(work["date_parsed"].isna().sum())


    # status/type
    work["status_norm"] = work["status"].astype(str).str.strip().str.lower()
    invalid_status_mask = ~work["status_norm"].isin(ALLOWED_STATUS)
    metrics["invalid_status"] = int(invalid_status_mask.sum())

    work["type_norm"] = work["type"].astype(str).str.strip().str.upper()
    invalid_type_mask = ~work["type_norm"].isin(ALLOWED_TYPE)
    metrics["invalid_type"] = int(invalid_type_mask.sum())

    # amount
    work["amount_norm"] = work["amount"].apply(_parse_amount)
    invalid_amount_mask = work["amount_norm"].isna()
    metrics["invalid_amount"] = int(invalid_amount_mask.sum())

    # remove duplicates by id
    before = len(work)
    work = work.drop_duplicates(subset=["id"], keep="first")
    metrics["duplicates_removed"] = int(before - len(work))

    # filter month
    month_start = pd.to_datetime(month + "-01")
    month_end = (month_start + pd.offsets.MonthBegin(1))  # first day next month
    month_mask = (work["date_parsed"] >= month_start) & (work["date_parsed"] < month_end)

    # filter valid rows for report
    ok = work[
        month_mask
        & work["date_parsed"].notna()
        & ~invalid_status_mask
        & ~invalid_type_mask
        & work["amount_norm"].notna()
    ].copy()

    # threshold
    before_thr = len(ok)
    ok = ok[ok["amount_norm"] >= float(min_amount)].copy()
    metrics["below_threshold_excluded"] = int(before_thr - len(ok))

    # issues = o que sobrou fora (para alertas depois)
    issues = work.drop(ok.index, errors="ignore").copy()

    metrics["rows_out"] = len(ok)
    return ok, issues, metrics
