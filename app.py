from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

app = Flask(__name__)

# ... Code pour la gestion des exceptions et du système de logs ...

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'ods'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'Fichier {filename} uploadé avec succès !'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wiki/<page>')
def wiki(page):
    try:
        return render_template(f'wiki/{page}.html')
    except FileNotFoundError:
        app.logger.error(f"Page {page} non trouvée")
        return "Page non trouvée", 404
    except Exception as e:
        app.logger.error(f"Erreur: {str(e)}")
        return "Une erreur est survenue", 500


if __name__ == '__main__':
    app.run(debug=True)
