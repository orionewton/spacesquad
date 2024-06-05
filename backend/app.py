from flask import Flask, jsonify, send_from_directory, request, abort
import os
from odf.opendocument import load
from odf.text import H, P
from odf.draw import Frame, Image

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'source_documents'
HTML_FOLDER = 'html_documents'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HTML_FOLDER'] = HTML_FOLDER


@app.route('/api/wiki/<filename>', methods=['GET'])
def get_article(filename):
    file_path = os.path.join(app.config['HTML_FOLDER'], f'{filename}.html')
    if os.path.exists(file_path):
        return send_from_directory(app.config['HTML_FOLDER'], f'{filename}.html')
    else:
        abort(404, description="Resource not found")


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        convert_odt_to_html(filename)
        return jsonify({"success": "File successfully uploaded"}), 201


def convert_odt_to_html(odt_file):
    doc = load(odt_file)
    body = doc.getElementsByType(H) + doc.getElementsByType(P) + doc.getElementsByType(Frame)
    html_content = "<html><body>"
    for element in body:
        if isinstance(element, H):
            html_content += f"<h{element.attributes['text:outline-level']}>{element.firstChild.data}</h{element.attributes['text:outline-level']}>"
        elif isinstance(element, P):
            html_content += f"<p>{element.firstChild.data}</p>"
        elif isinstance(element, Frame):
            image = element.getElementsByType(Image)[0]
            image_href = image.attributes['xlink:href']
            html_content += f'<img src="{image_href}" alt="{image_href}">'
    html_content += "</body></html>"

    html_filename = os.path.join(app.config['HTML_FOLDER'], os.path.splitext(os.path.basename(odt_file))[0] + '.html')
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(HTML_FOLDER):
        os.makedirs(HTML_FOLDER)
    app.run(debug=True)
