import streamlit as st

from utils.utils import total_edit_stats

# TODO: Рахувати самостійно кількість сторінок.

THRESHOLD = 8

st.title("Оплата перекладу")

rank = st.radio(
    "Виберіть звання:",
    options=[0, 1],
    format_func=lambda x: "Старшина" if x == 0 else "Рядовий",
    horizontal=True,
)

base_per_page = 120 if rank == 0 else 100

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

    base_pay = pages * base_per_page
    penalty = (
        0 if redacted_percentage <= THRESHOLD else (redacted_percentage - THRESHOLD) * 2
    )
    result = base_pay - penalty

    pay_table = {"Base Pay": base_pay, "Penalty": penalty, "Result": result}
    st.table(pay_table)

except Exception as e:
    st.warning("Please upload a DOCX file to analyze")
