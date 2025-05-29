import streamlit as st
import math

from utils.utils import total_edit_stats

# TODO: Рахувати самостійно кількість сторінок.

st.title("Оплата редагування")

BASE = 200
PER_PAGE = 20

pages = st.number_input("Кількість сторінок", min_value=1, value=1, step=1)

uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")

try:
    stats_df = total_edit_stats(uploaded_file)
    stats = stats_df.set_index("Metric")["Value"]
    redacted_percentage = ((stats.at["Edit Distance"] + 0.25*stats.at["Formatting Changes"])
                           / stats.at["Total Words"] * 100)

    st.subheader("Statistics")
    st.dataframe(stats_df, hide_index=True)
    st.write(f"Redacted Percentage: {redacted_percentage:.2f}%")

    base_pay = BASE + pages * PER_PAGE
    redact_pay = math.ceil(redacted_percentage) * 20
    result = base_pay + redact_pay

    pay_table = {"Base Pay": base_pay, "Redact Pay": redact_pay, "Result": result}
    st.table(pay_table)

except Exception as e:
    st.warning("Please upload a DOCX file to analyze")
