import zipfile
from lxml import etree

def extract_tracked_changes_with_formatting(docx_path):
    with zipfile.ZipFile(docx_path) as docx:
        document_xml = docx.read("word/document.xml")
        tree = etree.fromstring(document_xml)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        changes = []
        
        

        def format_details(change_tag):
            # Find the child <w:rPr> or <w:pPr> inside the change tag
            fmt_tag = change_tag.find("w:rPr", namespaces=ns) or change_tag.find("w:pPr", namespaces=ns)
            if fmt_tag is None:
                return ""

            parts = []
            for elem in fmt_tag:
                tag = etree.QName(elem).localname
                attrs = [f"{etree.QName(k).localname}: {v}" for k, v in elem.attrib.items()]
                if attrs:
                    parts.append(f"{tag} ({', '.join(attrs)})")
                else:
                    parts.append(tag)
            return "; ".join(parts)

        for tag in tree.findall(".//w:ins", namespaces=ns):
            author = tag.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author')
            date = tag.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}date')
            text = ''.join(tag.itertext()).strip()
            changes.append({'type': 'insertion', 'author': author, 'date': date, 'text': text})

        for tag in tree.findall(".//w:del", namespaces=ns):
            author = tag.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author')
            date = tag.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}date')
            text = ''.join(tag.itertext()).strip()
            changes.append({'type': 'deletion', 'author': author, 'date': date, 'text': text})

        # for tag in tree.findall(".//w:rPrChange", namespaces=ns):
            # author = tag.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author')
            # date = tag.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}date')
            # formatting = format_details(tag)
            # changes.append({'type': 'formatting change (run)', 'author': author, 'date': date, 'text': formatting})

        # for tag in tree.findall(".//w:pPrChange", namespaces=ns):
            # author = tag.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author')
            # date = tag.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}date')
            # formatting = format_details(tag)
            # changes.append({'type': 'formatting change (paragraph)', 'author': author, 'date': date, 'text': formatting})

        return changes

# Example usage
changes = extract_tracked_changes_with_formatting("./sparte.docx")
for c in changes:
    print(f"{c['type'].title()} by {c['author']} on {c['date']}:  {c['text']}")


# with open("./sparte.docx", "rb") as f:
#     with zipfile.ZipFile(f) as docx:
#         try:
#             document_xml = docx.read("word/document.xml")
#             document_tree = etree.fromstring(document_xml)
#             ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
#             paragraphs = document_tree.findall(".//w:p", namespaces=ns)
#             sections = document_tree.findall(".//w:sectPr", namespaces=ns)
#             tables = document_tree.findall(".//w:tbl", namespaces=ns)
#             images = document_tree.findall(".//w:drawing", namespaces=ns)
            
#             text_elements = document_tree.findall(".//w:t", namespaces=ns)
#             total_text_length = sum(len(elem.text or "") for elem in text_elements)
            
#             chars_per_page = 2000
#             paragraphs_per_page = 13
            
#             text_based_pages = max(1, total_text_length // chars_per_page)
#             paragraph_based_pages = max(1, len(paragraphs) // paragraphs_per_page)
            
#             table_pages = len(tables) * 0.5
#             image_pages = len(images) * 0.33
            
#             section_pages = len(sections)
            
#             estimated_pages = max(
#                 text_based_pages,
#                 paragraph_based_pages,
#                 section_pages,
#                 int(text_based_pages + paragraph_based_pages + table_pages + image_pages) // 2
#             )
            
#             num_pages = f"~{estimated_pages} (estimated from {len(paragraphs)} paragraphs, {len(sections)} sections, {len(tables)} tables, {len(images)} images, {total_text_length} chars)"
            
#         except Exception as e:
#             print(f"Error estimating page count: {e}")
#             num_pages = "Unknown"
        
#         print(f"Number of pages: {num_pages}")
