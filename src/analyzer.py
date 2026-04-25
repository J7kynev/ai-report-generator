# analyzer.py
# Handles data analysis using OpenAI API

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze(data_preview: str, context: str = "business sales data") -> str:
    """Send data preview to OpenAI and return analysis with insights."""
    prompt = f"""
You are a professional business analyst.
Analyze the following {context} and provide:
1. A brief summary of the data
2. 3 key insights
3. 2 actionable recommendations

Data:
{data_preview}

Respond in a clear, structured format.
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content