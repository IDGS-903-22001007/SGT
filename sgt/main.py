from flask import Flask, render_template

# Configuramos la app para que busque plantillas en el directorio actual ('.')
# Esto debe coincidir con la ubicación de login.html
app = Flask(__name__, template_folder='.') 

@app.route('/')
def index():
    # Renderizamos el archivo login.html
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
