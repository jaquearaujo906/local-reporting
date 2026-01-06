from fastapi import FastAPI
from pydantic import BaseModel
from src.runner import run_pipeline

app = FastAPI(
    title="Local Reporting Mini-System",
    description="Trigger local transaction report generation via REST API",
    version="1.0.0",
)

class RunRequest(BaseModel):
    input_path: str = "./data/transactions.csv"
    output_dir: str = "./outputs"
    send_email: bool = False

@app.post("/run")
def run(month: str, req: RunRequest):
    """
    Trigger the reporting pipeline for a given month (YYYY-MM).

    Example:
    POST /run?month=2023-08
    """
    result = run_pipeline(
        month=month,
        input_path=req.input_path,
        output_dir=req.output_dir,
        send_email=req.send_email,
    )
    return result
