import os
import pytest
from convert import convert_odt_to_html, convert_pdf_to_html

SOURCE_DIR = 'source_documents'
DEST_DIR = 'templates/wiki'


@pytest.fixture(scope="module")
def setup_files():
    # Préparation des fichiers de test
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)

    # Exemple de fichier .odt pour les tests
    with open(os.path.join(SOURCE_DIR, 'test.odt'), 'w') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
        <office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
            xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
            <office:body>
                <office:text>
                    <text:h text:outline-level="1">Titre de l'article</text:h>
                    <text:h text:outline-level="2">Titre de paragraphe</text:h>
                    <text:p>Contenu du paragraphe.</text:p>
                </office:text>
            </office:body>
        </office:document-content>
        ''')

    # Exemple de fichier .pdf pour les tests
    with open(os.path.join(SOURCE_DIR, 'test.pdf'), 'w') as f:
        f.write(
            '%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n/Resources <<\n/Font <<\n/F1 5 0 R\n>>\n>>\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n( Titre de l\'article ) Tj\nET\nendstream\nendobj\n5 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000053 00000 n\n0000000103 00000 n\n0000000194 00000 n\n0000000314 00000 n\ntrailer\n<<\n/Root 1 0 R\n>>\nstartxref\n364\n%%EOF')

    yield

    # Nettoyage des fichiers après les tests
    for filename in os.listdir(SOURCE_DIR):
        os.remove(os.path.join(SOURCE_DIR, filename))
    os.rmdir(SOURCE_DIR)
    for filename in os.listdir(DEST_DIR):
        os.remove(os.path.join(DEST_DIR, filename))


def test_convert_odt_to_html(setup_files):
    file_path = os.path.join(SOURCE_DIR, 'test.odt')
    convert_odt_to_html(file_path)
    html_file = os.path.join(DEST_DIR, 'Titre_de_l_article.html')

    assert os.path.exists(html_file)
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '<h1>Titre de l\'article</h1>' in content
        assert '<h2>Titre de paragraphe</h2>' in content
        assert '<p>Contenu du paragraphe.</p>' in content


def test_convert_pdf_to_html(setup_files):
    file_path = os.path.join(SOURCE_DIR, 'test.pdf')
    convert_pdf_to_html(file_path)
    html_file = os.path.join(DEST_DIR, 'Titre_de_l_article.html')

    assert os.path.exists(html_file)
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '<h1>Titre de l\'article</h1>' in content
        assert '<p>' in content  # Assuming the paragraph will be in the HTML content
