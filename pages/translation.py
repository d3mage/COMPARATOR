import nltk
from lxml import etree

import streamlit as st
import pandas as pd

from utils.utils import extract_edits, extract_formatting
from utils.xml_extract import extract_xml


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

    base_pay = pages * base_per_page
    penalty = (
        0 if redacted_percentage <= THRESHOLD else (redacted_percentage - THRESHOLD) * 2
    )
    result = base_pay - penalty

    pay_table = {"Base Pay": base_pay, "Penalty": penalty, "Result": result}
    st.table(pay_table)

except Exception as e:
    st.warning("Please upload a DOCX file to analyze")
