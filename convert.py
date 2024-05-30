import os

SOURCE_DIR = 'source_documents'
DEST_DIR = 'templates/wiki'


class Content:
    def __init__(self, source):
        self.author = None
        self.title = None
        self.intro = None
        self.parag = []
        self.read_file(source)

    def read_file(self, source):
        f = open(source, "r", encoding="utf-8")
        self.author = f.readline().replace("\n", '')
        self.title = f.readline().replace("\n", '')
        title = None
        parag = ""
        for line in f:
            if line.startswith("//"):
                self.intro = line.replace("//", "").replace("\n", "")

            elif line.startswith("**"):
                if title is not None:
                    self.parag.append((title, parag))
                    parag = ""
                title = line.replace("**", "").replace("\n", "")

            else:
                parag += line
        self.parag.append((title, parag))


def process_files():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for filename in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, filename)
        content = Content(file_path)


if __name__ == '__main__':
    process_files()
