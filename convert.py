import os
import re

SOURCE_DIR = 'source_documents'
DEST_DIR = 'templates/wiki'
IMAGE_DIR = 'source_images'


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
                parag += f'<img src="/{IMAGE_DIR}/{image_name}" alt="{image_name}">\n'
            else:
                parag += line
        self.parag.append([title, parag])

    @staticmethod
    def process_links(text):
        link_pattern = r'@([^@]+)@([^@]+)@'
        return re.sub(link_pattern, f'<a href="/{DEST_DIR}/' + r'\2">\1</a>', text)

    def convert_link(self):
        for text in self.parag:
            text[1] = self.process_links(text[1])
        if self.intro:
            self.intro = self.process_links(self.intro)

    def generate_html(self):
        html_content = (f'<!DOCTYPE html>\n<html lang="fr">\n'
                        f'<head>\n<meta charset="UTF-8">\n'
                        f'<title>{self.title}</title>\n</head>\n<body>\n')
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
