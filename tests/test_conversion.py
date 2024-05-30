import os
import pytest
from convert import Content, convert_files

SOURCE_DIR = 'source_documents'
DEST_DIR = 'templates/wiki'
IMAGE_DIR = 'source_images'


@pytest.fixture(scope="module")
def setup_files():
    # Création des répertoires nécessaires
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(DEST_DIR, exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)

    # Exemple de fichier .txt pour les tests
    test_content = '''Auteur
Titre
//Introduction Un lien vers un autre @article@link.html@//
**Sous-titre 1**
Paragraphe 1 avec une image
#image1.png#
et un lien @ici@ici.html@
**Sous-titre 2**
Paragraphe 2 avec un autre lien @là@link2.html@
'''

    with open(os.path.join(SOURCE_DIR, 'test.txt'), 'w', encoding='utf-8') as f:
        f.write(test_content)

    yield

    # Nettoyage après tests
    for dir_path in [SOURCE_DIR, DEST_DIR, IMAGE_DIR]:
        for filename in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, filename))
        os.rmdir(dir_path)


def test_content_parsing(setup_files):
    content = Content(os.path.join(SOURCE_DIR, 'test.txt'))
    assert content.author == 'Auteur'
    assert content.title == 'Titre'
    assert content.intro == 'Introduction Un lien vers un autre @article@link.html@'
    assert len(content.parag) == 2
    assert content.parag[0] == ['Sous-titre 1',
                                'Paragraphe 1 avec une image\n'
                                '<img src="/source_images/image1.png" alt="image1.png">\n'
                                'et un lien @ici@ici.html@\n']
    assert content.parag[1] == ['Sous-titre 2', 'Paragraphe 2 avec un autre lien @là@link2.html@\n']

    content.convert_link()
    assert content.intro == 'Introduction Un lien vers un autre <a href="/templates/wiki/link.html">article</a>'
    assert content.parag[0] == ['Sous-titre 1',
                                'Paragraphe 1 avec une image\n'
                                '<img src="/source_images/image1.png" alt="image1.png">\n'
                                'et un lien <a href="/templates/wiki/ici.html">ici</a>\n']
    assert content.parag[1] == ['Sous-titre 2', 'Paragraphe 2 avec un autre lien '
                                                '<a href="/templates/wiki/link2.html">là</a>\n']


def test_html_generation(setup_files):
    convert_files()
    html_file = os.path.join(DEST_DIR, 'Titre.html')
    assert os.path.exists(html_file)
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '<h1>Titre</h1>' in content
        assert '<em>Par Auteur</em>' in content
        assert '<p>Introduction Un lien vers un autre <a href="/templates/wiki/link.html">article</a></p>' in content
        assert '<h2>Sous-titre 1</h2>' in content
        assert '<img src="/source_images/image1.png" alt="image1.png">' in content
        assert '<a href="/templates/wiki/ici.html">ici</a>' in content
        assert '<h2>Sous-titre 2</h2>' in content
        assert '<a href="/templates/wiki/link2.html">là</a>' in content
