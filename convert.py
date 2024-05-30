import os
import re

SOURCE_DIR = 'source_documents'
DEST_DIR = 'templates/wiki'
BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "static", "images")


class Content:
    def __init__(self, source):
        self.author = None
        self.title = None
        self.intro = None
        self.parag = []
        self.read_file(source)

    def read_file(self, source):
        f = open(source, "r", encoding="utf-8")
        self.author = f.readline().strip()
        self.title = f.readline().strip()
        title = None
        parag = ""
        for line in f:
            if line.startswith("//"):
                self.intro = line.replace("//", "").strip()

            elif line.startswith("**"):
                if title is not None:
                    self.parag.append([title, parag])
                    parag = ""
                title = line.replace("**", "").strip()
            elif line.startswith("#"):
                line = line.strip()
                image_name = line.replace("#", "")
                parag += f'<img src="{os.path.join(IMG_DIR, image_name)}" alt="{image_name}">\n'
            else:
                parag += line
        self.parag.append([title, parag])

    @staticmethod
    def process_links(texte):
        def remplacement(match):
            mot = match.group(1)
            lien = match.group(2)
            lien_formatte = f'<a href="/{DEST_DIR}/{lien.replace(" ", "%20")}.html">{mot}</a>'
            return lien_formatte

        pattern = r'@([^@]+)@([^@]+)@'
        texte_transforme = re.sub(pattern, remplacement, texte)

        return texte_transforme
        # link_pattern = r'@([^@]+)@([^@]+)@'
        # return re.sub(link_pattern, rf'<a href="/{DEST_DIR}/\2">\1</a>', text)

    def convert_link(self):
        for text in self.parag:
            text[1] = self.process_links(text[1])
        if self.intro:
            self.intro = self.process_links(self.intro)

    def generate_html(self):
        html_content = f'<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="UTF-8">\n<title>{self.title}</title>\n'
        html_content += ('<style>header { display: flex; align-items: center; padding: 10px; } '
                         'header img { height: 50px; margin-right: 10px; } </style>\n')
        html_content += '</head>\n<body>\n'
        html_content += '<header>\n'
        html_content += f'<a href="/"><img src="/{IMG_DIR}/Logo.png" alt="Logo"></a>\n'
        html_content += '<h1>Space Squad</h1>\n'
        html_content += '</header>\n'
        html_content += f'<h1>{self.title}</h1>\n<p><em>Par {self.author}</em></p>\n'
        if self.intro:
            html_content += f'<p>{self.intro}</p>\n'
        for title, paragraph in self.parag:
            if title:
                html_content += f'<h2>{title}</h2>\n'
            html_content += f'<p>{paragraph}</p>\n'
        html_content += '\n</body>\n</html>'
        return html_content


def convert_files():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith('.txt'):
            content = Content(os.path.join(SOURCE_DIR, filename))
            content.convert_link()
            html_content = content.generate_html()
            html_file = os.path.join(DEST_DIR, f'{content.title.replace(" ", "_")}.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)


if __name__ == '__main__':
    convert_files()
