import zipfile
from lxml import etree
import streamlit as st
import pandas as pd
from utils.utils import (
    count_words,
    extract_docx,
    get_visible_text,
    read_document_xml,
    count_change_tags,
)

st.title("Tracked Changes Summary")

uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")

if uploaded_file:
    extract_to = "extracted_docx"
    extract_docx(uploaded_file, extract_to)
    xml_content = read_document_xml(extract_to)
    change_counts = count_change_tags(xml_content)

    visible_text = get_visible_text(xml_content)
    word_count = count_words(visible_text)

    all_counts = dict(change_counts[0])
    
    for tag, count in sorted(all_counts.items(), key=lambda x: -x[1]):
        st.write(f"{tag}: {count} occurrence(s)")

    st.write(word_count)