import nltk
import streamlit as st
import pandas as pd
import math

from lxml import etree

from utils.utils import extract_edits, extract_formatting
from utils.xml_extract import extract_xml


# TODO: Рахувати самостійно кількість сторінок.

st.title("Оплата редагування")

BASE = 200
PER_PAGE = 20

pages = st.number_input("Кількість сторінок", min_value=1, value=1, step=1)

uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")

try:
    xml_content = extract_xml(uploaded_file)
    xml_bytes = xml_content.encode('utf-8')
    xml_root = etree.fromstring(xml_bytes)

    edit_entries, unedited_entries = extract_edits(xml_root)

    original_word_count = 0
    for entry in unedited_entries:
        original_word_count += len(entry)
    for entry in edit_entries.values():
        original_word_count += len(entry["del"])

    edit_distance = 0
    for entry in edit_entries.values():
        # We want Levenstein distance on words, not letters
        edit_distance += nltk.edit_distance(entry["ins"], entry["del"])

    formatting_changes = extract_formatting(xml_content)  # Maybe redo to use lxml
    redacted_percentage = (edit_distance + 0.25*formatting_changes) / original_word_count * 100

    st.subheader("Statistics")
    stats_df = pd.DataFrame(
        {
            "Metric": ["Total Words", "Edit Distance (additions + deletions + substitutions)", "Formatting Changes"],
            "Count": [
                original_word_count,
                edit_distance,
                formatting_changes,
            ],
        }
    )
    st.dataframe(stats_df, hide_index=True)
    st.write(f"Redacted Percentage: {redacted_percentage:.2f}%")

    base_pay = BASE + pages * PER_PAGE
    redact_pay = math.ceil(redacted_percentage) * 20
    result = base_pay + redact_pay

    pay_table = {"Base Pay": base_pay, "Redact Pay": redact_pay, "Result": result}
    st.table(pay_table)

except Exception as e:
    st.warning("Please upload a DOCX file to analyze")
