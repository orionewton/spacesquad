import os

from convert import Content


def test_read_file():
    content = Content("Modele.txt")
    assert content.author == "Auteur"
    assert content.title == "Titre"
    assert content.intro == "Introduction"
    assert content.parag == [("Sous-titre", "Paragraphe\n\n@phrase à link@Titre du lien@\n\n#Logo.png#")]
