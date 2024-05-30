import os

import pytest

from convert import Content

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'doc_tests',
)


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'Modele.txt'),
)
def test_read_file():
    content = Content(os.path.join(FIXTURE_DIR, "Modele.txt"))
    assert content.author == "Auteur"
    assert content.title == "Titre"
    assert content.intro == "Introduction"
    assert content.parag == [("Sous-titre", "Paragraphe\n\n@phrase à link@Titre du lien@\n\n#Logo.png#")]
