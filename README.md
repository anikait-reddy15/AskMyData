# Gemini Secure Data Analyst

## Overview
This Streamlit app lets users upload CSV datasets and ask natural language data questions. It uses Google’s Gemini generative AI model to generate Python code that answers the questions by analyzing the uploaded data. The generated code is executed securely within the app, showing tables, values, or visualizations as results.

---

## Features
- Upload CSV files and preview the dataset.
- Ask data-related questions in plain English (e.g., summary stats, correlations, trends).
- Uses Gemini AI to generate Python code based on the dataset and question.
- Securely executes the generated code with restricted permissions.
- Displays outputs as tables, values, console text, or plots.
- Handles errors gracefully and shows detailed tracebacks if execution fails.

---

## Technologies Used
- Python
- Streamlit for the web UI
- Pandas for data handling
- Matplotlib and Seaborn for visualization
- Google Generative AI API (Gemini) for code generation
- python-dotenv for managing API keys securely

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/gemini-secure-data-analyst.git
cd gemini-secure-data-analyst
