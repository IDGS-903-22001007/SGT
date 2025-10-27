# Archivo: sgt/main.py
from flask import Flask, render_template

# Esta es la instancia de la aplicación que Gunicorn necesita encontrar
# La llamamos 'app'
# Nota: Flask busca automáticamente la carpeta 'templates' en el mismo nivel que este archivo.
app = Flask(__name__)

# Define la ruta raíz para servir el HTML
@app.route("/")
def login_page():
    # Renderiza el archivo login.html que debe estar en sgt/templates/
    return render_template("login.html")

# Este bloque es solo para ejecutar localmente, Gunicorn lo ignora
if __name__ == "__main__":
    app.run(debug=True)
