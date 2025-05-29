import streamlit as st

from utils.utils import total_edit_stats
from utils.calculate import (
    calculate_editor_payment,
    calculate_translation_payment,
    calculate_redacted_percentage,
)

st.title("Оплата перекладу")

pages = st.number_input("Кількість сторінок", min_value=1, value=1, step=1)

uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")

if uploaded_file is None:
    st.warning("Please upload a DOCX file to analyze")
else:
    stats_df = total_edit_stats(uploaded_file)
    stats = stats_df.set_index("Metric")["Value"]
    redacted_percentage = calculate_redacted_percentage(
        stats.at["Edit Distance"],
        stats.at["Formatting Changes"],
        stats.at["Total Words"],
    )

    st.subheader("Statistics")
    st.dataframe(stats_df, hide_index=True)
    st.write(f"Redacted Percentage: {redacted_percentage:.2f}%")

    rank = st.radio(
        "Виберіть звання:",
        options=[0, 1],
        format_func=lambda x: "Старшина" if x == 0 else "Рядовий",
        horizontal=True,
    )

    payment_df = calculate_translation_payment(pages, redacted_percentage, rank)
    st.dataframe(payment_df, hide_index=True)

    payment_df = calculate_editor_payment(pages, redacted_percentage)
    st.dataframe(payment_df, hide_index=True)
