import json
from pathlib import Path

def write_summary(output_dir: str, month: str, metrics: dict) -> str:
    yyyymm = month.replace("-", "")
    out_folder = Path(output_dir) / yyyymm
    out_folder.mkdir(parents=True, exist_ok=True)

    out_path = out_folder / "summary.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    return str(out_path)
