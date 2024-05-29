import os
from odf.opendocument import load
from odf.text import H, P, Span
import fitz  # PyMuPDF

SOURCE_DIR = 'source_documents'
DEST_DIR = 'templates/wiki'


def convert_odt_to_html(file_path):
    doc = load(file_path)
    html_content = ''
    title = ''

    for elem in doc.getElementsByType(H):
        if elem.getAttribute('outline-level') == '1':
            title = elem.firstChild.data
            html_content += f'<h1>{title}</h1>\n'
        else:
            html_content += f'<h{elem.getAttribute("outline-level")}>{elem.firstChild.data}</h{elem.getAttribute("outline-level")}>'

    for elem in doc.getElementsByType(P):
        text_content = ''
        for child in elem.childNodes:
            if isinstance(child, Span):
                text_content += child.firstChild.data
            else:
                text_content += child.data
        html_content += f'<p>{text_content}</p>\n'

    html_file = os.path.join(DEST_DIR, f'{title.replace(" ", "_")}.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(
            f'<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="UTF-8">\n<title>{title}</title>\n</head>\n<body>\n')
        f.write(html_content)
        f.write('\n</body>\n</html>')


def convert_pdf_to_html(file_path):
    doc = fitz.open(file_path)
    html_content = ''
    title = ''

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text")
        lines = text.split('\n')
        if page_num == 0:
            title = lines[0].strip()
            html_content += f'<h1>{title}</h1>\n'
        for line in lines:
            if line.strip():
                html_content += f'<p>{line.strip()}</p>\n'

    html_file = os.path.join(DEST_DIR, f'{title.replace(" ", "_")}.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(
            f'<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="UTF-8">\n<title>{title}</title>\n</head>\n<body>\n')
        f.write(html_content)
        f.write('\n</body>\n</html>')


def process_files():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for filename in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, filename)
        if filename.endswith('.odt'):
            convert_odt_to_html(file_path)
        elif filename.endswith('.pdf'):
            convert_pdf_to_html(file_path)


if __name__ == '__main__':
    process_files()
