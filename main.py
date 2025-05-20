import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import traceback
import matplotlib.pyplot as plt
import seaborn as sns
import io
import contextlib
import re

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Streamlit UI setup
st.set_page_config(page_title="Secure Gemini Data Analyst", page_icon="🧠")
st.title("Gemini Secure Data Analyst")
st.write("Upload a CSV and ask data questions. Gemini generates code, we run it safely and show the result!")

# Upload file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    user_question = st.text_input("Ask a data question (e.g. correlation, trend, summary):")

    if st.button("Answer using Gemini AI") and user_question:
        with st.spinner("Gemini is analyzing your question..."):
            # Construct prompt with column info
            column_info = "\n".join([f"- {col}: {dtype}" for col, dtype in df.dtypes.items()])
            prompt = f"""
You are a helpful data analyst. A user uploaded a pandas DataFrame named `df` with the following columns and data types:

{column_info}

ONLY use these columns. Do NOT assume any missing or extra columns like 'Date' or 'Temp'.

Now answer the following question using Python code:

\"\"\"{user_question}\"\"\"

Output ONLY runnable code inside triple backticks (```python ... ```), no explanation.

Valid outputs should assign result to one of:
- `output_df` for tables
- `output_value` for single values
- or use `plt.show()` for plots
"""

            try:
                response = model.generate_content(prompt)
                generated_code = response.text.strip()

                # Clean up markdown formatting
                if generated_code.startswith("```python"):
                    generated_code = generated_code.replace("```python", "").replace("```", "").strip()

                # Strip unsafe import statements if any
                generated_code = re.sub(r'^import .*$', '', generated_code, flags=re.MULTILINE)

                st.subheader("Generated Python Code")
                st.code(generated_code, language="python")

                # Secure execution environment
                safe_globals = {
                    "__builtins__": {
                        "print": print,
                        "len": len,
                        "range": range,
                        "min": min,
                        "max": max,
                        "sum": sum,
                        "abs": abs,
                        "round": round,
                        "sorted": sorted,
                        "set": set,
                    },
                    "pd": pd,
                    "plt": plt,
                    "sns": sns,
                }
                safe_locals = {"df": df.copy()}

                with st.spinner("Executing generated code..."):
                    stdout = io.StringIO()
                    with contextlib.redirect_stdout(stdout):
                        exec(generated_code, safe_globals, safe_locals)

                    output_text = stdout.getvalue()
                    if output_text:
                        st.subheader("Console Output")
                        st.text(output_text)

                    if "output_df" in safe_locals:
                        st.subheader("Output DataFrame")
                        st.dataframe(safe_locals["output_df"])

                    if "output_value" in safe_locals:
                        st.subheader("Computed Value")
                        st.write(safe_locals["output_value"])

                    # Only show plot if question suggests visualization
                    visual_keywords = ["plot", "graph", "chart", "visual", "trend", "distribution", "bar", "line", "scatter", "histogram"]
                    if any(keyword in user_question.lower() for keyword in visual_keywords):
                        st.subheader("Visualization")
                        st.pyplot(plt)

            except Exception as e:
                st.error("Code execution failed:")
                st.text(traceback.format_exc())
