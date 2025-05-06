import zipfile
import os

def extract_xml(uploaded_file):
    extract_to = "extracted_docx"
    extract_docx(uploaded_file, extract_to)
    xml_content = read_document_xml(extract_to)
    return xml_content


def extract_docx(docx_path, extract_to):
    with zipfile.ZipFile(docx_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def read_document_xml(extract_dir):
    xml_path = os.path.join(extract_dir, "word", "document.xml")
    with open(xml_path, "r", encoding="utf-8") as f:
        return f.read()