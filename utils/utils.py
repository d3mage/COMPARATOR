import re


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
