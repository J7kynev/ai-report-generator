# main.py
# Entry point — orchestrates data reading, analysis and report generation

from src.reader import read_csv, preview
from src.analyzer import analyze
from src.generator import generate_pdf

def main():
    print("📊 AI Report Generator — Starting...\n")

    # Step 1: Read data
    filepath = "data/sample.csv"
    print(f"📂 Reading data from: {filepath}")
    df = read_csv(filepath)
    data_preview = preview(df)
    print("✅ Data loaded successfully\n")
    print(data_preview)
    print()

    # Step 2: Analyze with OpenAI
    print("🤖 Sending data to OpenAI for analysis...")
    analysis = analyze(data_preview, context="business sales data")
    print("✅ Analysis complete\n")
    print(analysis)
    print()

    # Step 3: Generate PDF report
    print("📄 Generating PDF report...")
    output_path = generate_pdf(analysis)
    print(f"✅ Report saved to: {output_path}")

if __name__ == "__main__":
    main()