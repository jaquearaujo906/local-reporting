import argparse
from src.runner import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="Local Reporting Mini-System")
    parser.add_argument("--month", required=True, help="Target month in format YYYY-MM")
    parser.add_argument("--input", default="./data/transactions.csv", help="Path to transactions CSV")
    parser.add_argument("--output", default="./outputs", help="Output base directory")
    parser.add_argument("--send-email", action="store_true", help="Send email with report attached")
    args = parser.parse_args()

    result = run_pipeline(
        month=args.month,
        input_path=args.input,
        output_dir=args.output,
        send_email=args.send_email,
    )

    print("DONE ✅")
    print(f"Report: {result['report_path']}")
    print(f"Summary: {result['summary_path']}")
    print(f"Metrics: {result['metrics']}")

if __name__ == "__main__":
    main()
