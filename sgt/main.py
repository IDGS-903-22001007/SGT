from flask import Flask, render_template

# 🔥 CORRECCIÓN CLAVE: Le decimos a Flask que busque archivos HTML (plantillas)
# en el mismo directorio donde está main.py (que es la carpeta /sgt)
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    # Renderiza el archivo login.html que está en la misma carpeta que main.py
    return render_template('login.html')

if __name__ == '__main__':
    # Este bloque es solo para pruebas locales
    app.run(debug=True)
