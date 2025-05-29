import os
import re

import nltk
import pandas as pd
from lxml import etree
from streamlit.runtime.uploaded_file_manager import UploadedFile

from utils.xml_extract import extract_xml


def extract_comments(xml_content):
    rPrChange_count = extract_formatting(xml_content)
    del_texts = extract_tag(xml_content, "del")
    ins_texts = extract_tag(xml_content, "ins")

    return (
        {
            "w:rPrChange": rPrChange_count,
            "w:del": count_words(del_texts) if del_texts else 0,
            "w:ins": count_words(ins_texts) if ins_texts else 0,
        },
        del_texts,
        ins_texts,
    )


def extract_formatting(xml_content):
    paragraphs = re.findall(r"<w:p[^>]*>.*?</w:p>", xml_content, re.DOTALL)
    paragraphs_with_changes = 0

    for p in paragraphs:
        if re.search(r"<w:rPrChange[^>]*>.*?</w:rPrChange>", p, re.DOTALL):
            paragraphs_with_changes += 1

    return paragraphs_with_changes


def extract_tag(xml_content, tag_name):
    pattern = rf"<w:{tag_name}[^>]*?>(.*?)</w:{tag_name}>"
    matches = re.findall(pattern, xml_content, re.DOTALL)

    texts = []
    for match in matches:
        if tag_name == "ins":
            inner_texts = re.findall(r"<w:t[^>]*?>(.*?)</w:t>", match)
        elif tag_name == "del":
            inner_texts = re.findall(r"<w:delText[^>]*?>(.*?)</w:delText>", match)
        if inner_texts:
            texts.append("".join(inner_texts))
    return " ".join(texts)


def extract_text(xml_content):
    xml_content = re.sub(r"<w:del\b.*?</w:del>", "", xml_content, flags=re.DOTALL)

    texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml_content)
    return " ".join(texts)


def count_words(text):
    return len([word for word in re.split(r"\s+", text) if word.strip()])


def processed_tag(node: etree.Element) -> str:
    tag = re.match(r"({.*})(\w*)", node.tag).group(2)
    return "del" if tag == "delText" else "ins"


def processed_w_id(node: etree.Element) -> str:
    w_id_key = f"{{{node.nsmap["w"]}}}id"  # w:id
    w_id = None
    parent = node
    while parent is not None:
        if w_id := parent.attrib.get(w_id_key):
            break
        parent = parent.getparent()
    return w_id


def extract_edits(xml_root: etree.Element) -> tuple[dict[str, dict[str, list]], list[list[str]]]:
    """
    Extracts edits from xml document of Google Docs document

    :param xml_root: lxml etree root of whole xml document
    :return: dict of edits and list of text entries left as in original.
    Dict of edits format:
    {
        "id": {
            "ins": ["Words", "after", "edit", "split", "by", "whitespaces"]
            "del": ["Words", "before", "edit", "split", "by", "whitespaces"]
        },
        ...
    }
    List of unedited entries:
    [
        ["Words", "split", "by", "whitespaces"],
        ...
    ]
    """
    text_nodes = xml_root.xpath('//*[@xml:space="preserve"]')

    edit_entries = {}
    unedited_entries = []
    for node in text_nodes:
        tag = processed_tag(node)
        w_id = processed_w_id(node)

        if w_id:
            edit_entries.setdefault(w_id, {"ins": [], "del": []})[tag] = node.text.split()
        else:
            unedited_entries.append(node.text.split())

    return edit_entries, unedited_entries


def calculate_edit_stats(uploaded_file: UploadedFile, file_name: str) -> dict[str, int]:
    xml_content = extract_xml(uploaded_file, file_name)
    xml_bytes = xml_content.encode('utf-8')
    xml_root = etree.fromstring(xml_bytes)

    edit_entries, unedited_entries = extract_edits(xml_root)

    total_words = 0
    for entry in unedited_entries:
        total_words += len(entry)
    for entry in edit_entries.values():
        total_words += len(entry["del"])

    edit_distance = 0
    for entry in edit_entries.values():
        # We want Levenstein distance on words, not letters
        edit_distance += nltk.edit_distance(entry["ins"], entry["del"])

    formatting_changes = extract_formatting(xml_content)  # Maybe redo to use lxml

    return {"Total Words": total_words, "Edit Distance": edit_distance, "Formatting Changes": formatting_changes}


def total_edit_stats(uploaded_file: UploadedFile) -> pd.DataFrame:
    document_stats = calculate_edit_stats(uploaded_file, file_name="document.xml")
    if os.path.isfile("footnotes.xml"):
        footnote_stats = calculate_edit_stats(uploaded_file, file_name="footnotes.xml")
    else:
        footnote_stats = {"Total Words": 0, "Edit Distance": 0, "Formatting Changes": 0}

    total_stats = {}
    for key in document_stats:
        total_stats[key] = document_stats[key] + footnote_stats[key]

    stats_df = pd.DataFrame({"Metric": list(total_stats.keys()), "Value": list(total_stats.values())})
    return stats_df
