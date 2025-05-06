import streamlit as st
import pandas as pd

from utils.utils import count_words, extract_comments, extract_text
from utils.xml_extract import extract_xml


# TODO: Не враховуємо в відсотку редагування форматування.
# TODO: Рахувати самостійно кількість сторінок.

THRESHOLD = 8

st.title("Оплата редагування")

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
    xml_content = extract_xml(uploaded_file)

    change_counts, deleted_text, inserted_text = extract_comments(xml_content)

    change_counts = {
        "Formatting Changes": change_counts["w:rPrChange"],
        "Removals": change_counts["w:del"],
        "Insertions": change_counts["w:ins"],
    }

    text = extract_text(xml_content)

    word_count = count_words(text)
    deleted_words_count = count_words(deleted_text)
    inserted_words_count = count_words(inserted_text)
    redacted_percentage = (
        (inserted_words_count + deleted_words_count) / word_count * 100
    )

    st.subheader("Change Counts")
    st.table(change_counts)

    st.subheader("Word Statistics")
    word_stats_df = pd.DataFrame(
        {
            "Metric": ["Total Words", "Deleted Words", "Inserted Words"],
            "Count": [
                int(word_count),
                int(deleted_words_count),
                int(inserted_words_count),
            ],
        }
    )
    st.dataframe(word_stats_df, hide_index=True)
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
