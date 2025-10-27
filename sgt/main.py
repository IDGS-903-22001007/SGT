from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "clave-secreta"  # Necesario para los mensajes flash

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # No importa el usuario o contraseña, siempre éxito
        flash("✅ Inicio de sesión exitoso", "success")
        return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
