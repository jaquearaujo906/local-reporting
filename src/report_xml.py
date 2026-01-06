from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

def build_report_xml(df_ok, month: str, currency: str) -> ET.ElementTree:
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    root = ET.Element("TransactionsReport", attrib={"month": month, "generated_at": generated_at})

    for _, row in df_ok.iterrows():
        tx = ET.SubElement(root, "Transaction", attrib={"id": str(row["id"])})

        ET.SubElement(tx, "Status").text = str(row["status_norm"])
        ET.SubElement(tx, "Date").text = row["date_parsed"].date().isoformat()

        amount_el = ET.SubElement(tx, "Amount", attrib={"currency": currency})
        amount_el.text = f"{float(row['amount_norm']):.2f}"

        ET.SubElement(tx, "Type").text = str(row["type_norm"])
        ET.SubElement(tx, "MerchantId").text = str(row["merchantid"])
        ET.SubElement(tx, "Network").text = str(row["network"])
        ET.SubElement(tx, "Category").text = str(row["category"]).strip().upper()

    return ET.ElementTree(root)

def write_report(tree: ET.ElementTree, output_dir: str, month: str) -> str:
    yyyymm = month.replace("-", "")
    out_folder = Path(output_dir) / yyyymm
    out_folder.mkdir(parents=True, exist_ok=True)

    out_path = out_folder / "report.xml"
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    return str(out_path)
