import zipfile
import os
import re


def extract_docx(docx_path, extract_to):
    with zipfile.ZipFile(docx_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def read_document_xml(extract_dir):
    xml_path = os.path.join(extract_dir, "word", "document.xml")
    with open(xml_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_change_text(xml_content, tag_name):
    pattern = rf"<w:{tag_name}[^>]*?>(.*?)</w:{tag_name}>"
    matches = re.findall(pattern, xml_content, re.DOTALL)

    texts = []
    for match in matches:
        if tag_name == "ins":
            inner_texts = re.findall(r"<w:t[^>]*?>(.*?)</w:t>", match)
        elif tag_name == "del":
            inner_texts = re.findall(r"<w:delText[^>]*?>(.*?)</w:delText>", match)
        else:
            inner_texts = []
        if inner_texts:
            texts.append("".join(inner_texts))
    return texts


def count_change_tags(xml_content):
    rPrChange_count = len(re.findall(r"<w:rPrChange\b", xml_content))
    del_texts = extract_change_text(xml_content, "del")
    ins_texts = extract_change_text(xml_content, "ins")

    return (
        {
            "w:rPrChange": rPrChange_count,
            "w:del": len(del_texts),
            "w:ins": len(ins_texts),
        },
        del_texts,
        ins_texts,
    )


def get_visible_text(xml_content):
    xml_content = re.sub(r"<w:del\b.*?</w:del>", "", xml_content, flags=re.DOTALL)

    texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml_content)
    return " ".join(texts)


def count_words(text):
    return len([word for word in re.split(r"\s+", text) if word.strip()])


uploaded_file = "tmp.docx"
extract_to = "extracted_docx"
extract_docx(uploaded_file, extract_to)
xml_content = read_document_xml(extract_to)

change_counts, deleted_texts, inserted_texts = count_change_tags(xml_content)

visible_text = get_visible_text(xml_content)
word_count = count_words(visible_text)

for tag, count in sorted(change_counts.items(), key=lambda x: -x[1]):
    print(f"{tag}: {count} occurrence(s)")

# # Print extracted text
# print("\nDeleted Texts:")
# for text in deleted_texts:
#     print(f"- {text}")

# print("\nInserted Texts:")
# for text in inserted_texts:
#     print(f"- {text}")

print(f"Word count (excluding deleted text): {word_count}")
