# Archivo: main.py
from flask import Flask

# Esta es la instancia de la aplicación que Gunicorn necesita encontrar
# La llamamos 'app'
app = Flask(__name__)

# Define una ruta simple para probar la conexión
@app.route("/")
def hello_world():
    # El mensaje final para verificar que la Actividad 15 fue exitosa
    return "<p>✅ ¡Despliegue CI/CD Exitoso! La Actividad 15 funciona.</p>"

# Este bloque es solo para ejecutar localmente, Gunicorn lo ignora
if __name__ == "__main__":
    app.run(debug=True)
