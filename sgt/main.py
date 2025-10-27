from flask import Flask, render_template, send_from_directory
import os

# Flask automáticamente busca en la subcarpeta 'templates'
# Para evitar eso, usamos send_from_directory
app = Flask(__name__) 

@app.route('/')
def index():
    # 🔥 CORRECCIÓN PARA ESTRUCTURA PLANA:
    # 'os.path.dirname(__file__)' obtiene la ruta de la carpeta actual (/sgt).
    # 'login.html' es el nombre del archivo a servir.
    return send_from_directory(os.path.dirname(__file__), 'login.html')

if __name__ == '__main__':
    app.run(debug=True)
