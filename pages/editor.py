import streamlit as st
import pandas as pd
import math

from utils.utils import count_words, extract_comments, extract_text
from utils.xml_extract import extract_xml


# TODO: Рахувати самостійно кількість сторінок.

st.title("Оплата редагування")

BASE = 200
PER_PAGE = 20

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
    substitutions = min(deleted_words_count, inserted_words_count)

    adjusted_deleted = deleted_words_count - substitutions
    adjusted_inserted = inserted_words_count - substitutions

    redacted_percentage = (
        (adjusted_inserted + adjusted_deleted + 0.25 * change_counts["Formatting Changes"])
        / word_count
        * 100
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

    base_pay = BASE + pages * PER_PAGE
    redact_pay = math.ceil(redacted_percentage) * 20
    result = base_pay + redact_pay

    pay_table = {"Base Pay": base_pay, "Redact Pay": redact_pay, "Result": result}
    st.table(pay_table)

except Exception as e:
    st.warning("Please upload a DOCX file to analyze")
