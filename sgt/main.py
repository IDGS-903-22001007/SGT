import os
from flask import Flask, render_template

# Obtenemos la ruta absoluta de la carpeta donde reside main.py (que es /sgt en el servidor)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuramos la aplicación Flask para que busque las plantillas
# dentro de la subcarpeta 'templates' que debe estar en el mismo lugar que main.py
# Por ejemplo: /home/site/wwwroot/sgt/templates
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates')) 

@app.route('/')
def index():
    # Esta función busca login.html dentro de la carpeta 'templates'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
