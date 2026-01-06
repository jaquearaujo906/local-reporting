import smtplib
from email.message import EmailMessage
from pathlib import Path
from src.config import settings

def send_report_email(month: str, metrics: dict, alerts: dict, attachment_path: str):
    subject = f"Transactional Report — {month}"

    lines = []
    lines.append("Technical summary:")
    lines.append(f"- rows_in: {metrics['rows_in']}")
    lines.append(f"- rows_out: {metrics['rows_out']}")
    lines.append(f"- duplicates_removed: {metrics['duplicates_removed']}")
    lines.append(f"- below_threshold_excluded: {metrics['below_threshold_excluded']}")
    lines.append("")
    lines.append("Alerts:")
    has_alert = False
    for k, v in alerts.items():
        if v:
            lines.append(f"- {k}: {v}")
            has_alert = True
    if not has_alert:
        lines.append("- None")

    body = "\n".join(lines)

    # valida SMTP
    if not all([
        settings.smtp_host,
        settings.smtp_user,
        settings.smtp_pass,
        settings.email_from,
        settings.email_to
    ]):
        raise ValueError("Missing SMTP/email settings in .env")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.email_from
    msg["To"] = settings.email_to
    msg.set_content(body)

    path = Path(attachment_path)
    data = path.read_bytes()
    msg.add_attachment(
        data,
        maintype="application",
        subtype="xml",
        filename="report.xml"
    )

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.set_debuglevel(1)  # 👈 DEBUG SMTP (importante!)
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_pass)
        server.send_message(msg)
