import os

import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Set the GEMINI_API_KEY environment variable before running this script.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


df = pd.read_excel("sales.xlsx")

print("\nExcel Loaded Successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")



def chart_product_revenue():

    data = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    data.plot(kind="bar")

    plt.title("Revenue by Product")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()


def chart_region_sales():

    data = (
        df.groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    data.plot(kind="bar")

    plt.title("Revenue by Region")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()


def chart_revenue_trend():

    trend = (
        df.groupby("Date")["Revenue"]
        .sum()
    )

    trend.plot(kind="line")

    plt.title("Revenue Trend")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break


    if "revenue by product" in question.lower():

        chart_product_revenue()

        continue

    if "sales by region" in question.lower():

        chart_region_sales()

        continue

    if "revenue trend" in question.lower():

        chart_revenue_trend()

        continue


    data_sample = df.to_string()

    prompt = f"""
You are a senior data analyst.

Dataset:

{data_sample}

Question:

{question}

Answer clearly.
"""

    response = model.generate_content(prompt)

    print("\nAI:")
    print(response.text)
