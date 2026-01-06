from src.config import settings
from src.io_csv import read_transactions_csv
from src.normalize import normalize_transactions
from src.report_xml import build_report_xml, write_report
from src.summary import write_summary


def run_pipeline(month: str, input_path: str, output_dir: str, send_email: bool = False) -> dict:
    df = read_transactions_csv(input_path)

    df_ok, df_issues, metrics = normalize_transactions(
        df=df,
        month=month,
        min_amount=settings.min_amount,
    )

    tree = build_report_xml(df_ok, month=month, currency=settings.default_currency)
    report_path = write_report(tree, output_dir=output_dir, month=month)
    summary_path = write_summary(output_dir=output_dir, month=month, metrics=metrics)

    alerts = {
        "invalid_date": metrics["invalid_date"],
        "invalid_status": metrics["invalid_status"],
        "invalid_type": metrics["invalid_type"],
        "invalid_amount": metrics["invalid_amount"],
        "duplicates_removed": metrics["duplicates_removed"],
        "below_threshold_excluded": metrics["below_threshold_excluded"],
    }

    # Resultado final
    result = {
        "status": "success",
        "month": month,
        "report_path": report_path,
        "summary_path": summary_path,
        "metrics": metrics,
        "alerts": alerts,
        "email_sent": False,
    }

    # Enviar email se solicitado
    if send_email:
        from src.emailer import send_report_email
        print("Sending email...")
        send_report_email(
            month=month,
            metrics=metrics,
            alerts=alerts,
            attachment_path=report_path,
        )
        print("Email sent (SMTP accepted).")
        result["email_sent"] = True

    return result
