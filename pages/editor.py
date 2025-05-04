import zipfile
from lxml import etree
import streamlit as st
import pandas as pd

def extract_tracked_changes_with_formatting(docx_path):
    with zipfile.ZipFile(docx_path) as docx:
        document_xml = docx.read("word/document.xml")
        tree = etree.fromstring(document_xml)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        changes = []

        for tag in tree.findall(".//w:ins", namespaces=ns):
            changes.append({'type': 'insertion'})

        for tag in tree.findall(".//w:del", namespaces=ns):
            changes.append({'type': 'deletion'})

        for tag in tree.findall(".//w:rPrChange", namespaces=ns):
            changes.append({'type': 'formatting change (run)'})

        for tag in tree.findall(".//w:pPrChange", namespaces=ns):
            changes.append({'type': 'formatting change (paragraph)'})

        return changes


st.title("Tracked Changes Summary")

uploaded_file = st.file_uploader("Upload a DOCX file", type="docx")

rank = st.selectbox("Select Rank", ["Рядовий", "Старшина"])

if uploaded_file:
    with open("temp.docx", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Count tracked changes
    changes = extract_tracked_changes_with_formatting("temp.docx")
    df = pd.DataFrame(changes)
    summary = df['type'].value_counts().reset_index()
    summary.columns = ['Change Type', 'Count']
    st.dataframe(summary)

    with zipfile.ZipFile("temp.docx") as docx:
        try:
            document_xml = docx.read("word/document.xml")
            document_tree = etree.fromstring(document_xml)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            paragraphs = document_tree.findall(".//w:p", namespaces=ns)
            sections = document_tree.findall(".//w:sectPr", namespaces=ns)
            tables = document_tree.findall(".//w:tbl", namespaces=ns)
            images = document_tree.findall(".//w:drawing", namespaces=ns)
            
            text_elements = document_tree.findall(".//w:t", namespaces=ns)
            total_text_length = sum(len(elem.text or "") for elem in text_elements)
            
            chars_per_page = 3000
            paragraphs_per_page = 13
            
            text_based_pages = max(1, total_text_length // chars_per_page)
            paragraph_based_pages = max(1, len(paragraphs) // paragraphs_per_page)
            
            table_pages = len(tables) * 0.5
            image_pages = len(images) * 0.33
            
            section_pages = len(sections)
            
            estimated_pages = max(
                text_based_pages,
                paragraph_based_pages,
                section_pages,
                int(text_based_pages + paragraph_based_pages + table_pages + image_pages) // 2
            )
            
            num_pages = f"~{estimated_pages} (estimated from {len(paragraphs)} paragraphs, {len(sections)} sections, {len(tables)} tables, {len(images)} images, {total_text_length} chars)"
            
        except Exception as e:
            print(f"Error estimating page count: {e}")
            num_pages = "Unknown"


    st.markdown(f"**Total Pages:** {num_pages}")
    st.markdown(f"**Selected Rank:** {rank}")

    

