# 📊 AI Report Generator

Automated report generation system that transforms raw data into structured, professional PDF reports using Python and OpenAI.

---

## 🚀 What it does

This tool takes data from a CSV or Google Sheets source, analyzes it using the OpenAI API, and automatically generates a clean, structured PDF report with insights, summaries, and recommendations — no manual work required.

---

## 🛠️ Tech Stack

- **Python 3.11**
- **OpenAI API** — GPT-4o for data analysis and insight generation
- **ReportLab** — PDF generation
- **Pandas** — Data processing
- **Google Sheets API** *(optional input source)*

---

## 📁 Project Structure

    ai-report-generator/
    ├── data/               # Input data files (CSV samples)
    ├── outputs/            # Generated PDF reports
    ├── src/
    │   ├── reader.py       # Data ingestion and cleaning
    │   ├── analyzer.py     # OpenAI analysis logic
    │   └── generator.py    # PDF report builder
    ├── .env.example        # Environment variable template
    ├── requirements.txt    # Python dependencies
    └── README.md

---

## ⚙️ Setup

```bash
git clone https://github.com/J7kynev/ai-report-generator.git
cd ai-report-generator
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your OpenAI API key:

---

## 📌 Status

🔧 In development — first release coming soon.

---

## 👤 Author

**J7kynev** — AI Automation & Business Systems
