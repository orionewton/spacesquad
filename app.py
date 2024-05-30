from flask import Flask, render_template, abort
import os
from convert import convert_files

app = Flask(__name__)

# Convertir les fichiers lors du démarrage de l'application
convert_files()


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
