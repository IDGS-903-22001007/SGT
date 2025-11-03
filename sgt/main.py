from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file
from sgt.usuarios_model import UsuarioModel
from sgt.reports import ReporteAbordajes, ReporteServiciosEspeciales
import os

# ---------------- CONFIGURACIÓN ----------------

# 🚨 CORRECCIÓN CLAVE: Usamos rutas relativas simples.
# Azure ejecuta Gunicorn desde la raíz del proyecto.
# TEMPLATE_DIR debe apuntar a la carpeta 'templates' en esa raíz.
# REPORTS_DIR debe apuntar a la carpeta 'reportes' en esa raíz.
TEMPLATE_DIR = 'templates'
REPORTS_DIR = 'reportes'

# Aseguramos que la carpeta de reportes exista en el entorno de ejecución
os.makedirs(REPORTS_DIR, exist_ok=True)

# Inicializamos Flask, usando la ruta relativa para templates
app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = "clave-secreta"

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Asumiendo que verificar_credenciales existe en tu modelo
        usuario = UsuarioModel.verificar_credenciales(email, password) 
        if usuario:
            # Almacena solo la información necesaria del usuario en la sesión
            session['usuario'] = usuario
            flash("✅ Inicio de sesión exitoso", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Usuario o contraseña incorrecta", "danger")

    return render_template('login.html')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', usuario=session.get('usuario'))

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for('login'))

# ---------------- REPORTE DE ABORDAJES COMPLETO ----------------
@app.route('/reporte_abordajes', methods=['GET', 'POST'])
def reporte_abordajes():
    # Verifica la sesión antes de procesar
    if 'usuario' not in session:
        return redirect(url_for('login'))

    fecha = request.form.get('fecha') if request.method == 'POST' else None
    unidad = request.form.get('unidad') if request.method == 'POST' else None
    
    # Asumiendo que ReporteAbordajes.obtener_abordajes existe y funciona
    datos = ReporteAbordajes.obtener_abordajes(fecha, unidad)
    return render_template('reporte_abordajes.html', datos=datos, fecha=fecha, unidad=unidad)

@app.route('/reporte_abordajes/excel', methods=['POST'])
def reporte_abordajes_excel():
    if 'usuario' not in session:
        flash("Sesión expirada.", "danger")
        return redirect(url_for('login'))

    fecha = request.form.get('fecha')
    unidad = request.form.get('unidad')
    datos = ReporteAbordajes.obtener_abordajes(fecha, unidad)

    # Usa la ruta corregida para guardar el archivo
    archivo_path = os.path.join(REPORTS_DIR, "reporte_abordajes.xlsx")
    archivo = ReporteAbordajes.exportar_excel(datos, nombre_archivo=archivo_path)
    
    if archivo:
        return send_file(archivo, as_attachment=True)
        
    flash("No hay datos para exportar", "danger")
    return redirect(url_for('reporte_abordajes'))

@app.route('/reporte_abordajes/pdf', methods=['POST'])
def reporte_abordajes_pdf():
    if 'usuario' not in session:
        flash("Sesión expirada.", "danger")
        return redirect(url_for('login'))

    fecha = request.form.get('fecha')
    unidad = request.form.get('unidad')
    datos = ReporteAbordajes.obtener_abordajes(fecha, unidad)

    # Usa la ruta corregida para guardar el archivo
    archivo_path = os.path.join(REPORTS_DIR, "reporte_abordajes.pdf")
    archivo = ReporteAbordajes.exportar_pdf(datos, nombre_archivo=archivo_path)
    
    if archivo:
        return send_file(archivo, as_attachment=True)
        
    flash("No hay datos para exportar", "danger")
    return redirect(url_for('reporte_abordajes'))

# ---------------- REPORTE DE SERVICIOS ESPECIALES COMPLETO ----------------
@app.route('/reporte_servicios_especiales', methods=['GET', 'POST'])
def reporte_servicios_especiales():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    fecha_inicio = request.form.get('fecha_inicio') if request.method == 'POST' else None
    fecha_fin = request.form.get('fecha_fin') if request.method == 'POST' else None
    nombre_servicio = request.form.get('nombre_servicio') if request.method == 'POST' else None

    datos = ReporteServiciosEspeciales.obtener_servicios(fecha_inicio, fecha_fin, nombre_servicio)
    return render_template(
        'reporte_servicios_especiales.html',
        datos=datos,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        nombre_servicio=nombre_servicio
    )

@app.route('/reporte_servicios_especiales/excel', methods=['POST'])
def reporte_servicios_especiales_excel():
    if 'usuario' not in session:
        flash("Sesión expirada.", "danger")
        return redirect(url_for('login'))
        
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    nombre_servicio = request.form.get('nombre_servicio')
    datos = ReporteServiciosEspeciales.obtener_servicios(fecha_inicio, fecha_fin, nombre_servicio)

    # Usa la ruta corregida para guardar el archivo
    archivo_path = os.path.join(REPORTS_DIR, "reporte_servicios_especiales.xlsx")
    archivo = ReporteServiciosEspeciales.exportar_excel(datos, nombre_archivo=archivo_path)
    
    if archivo:
        return send_file(archivo, as_attachment=True)
        
    flash("No hay datos para exportar", "danger")
    return redirect(url_for('reporte_servicios_especiales'))

@app.route('/reporte_servicios_especiales/pdf', methods=['POST'])
def reporte_servicios_especiales_pdf():
    if 'usuario' not in session:
        flash("Sesión expirada.", "danger")
        return redirect(url_for('login'))

    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    nombre_servicio = request.form.get('nombre_servicio')
    datos = ReporteServiciosEspeciales.obtener_servicios(fecha_inicio, fecha_fin, nombre_servicio)

    # Usa la ruta corregida para guardar el archivo
    archivo_path = os.path.join(REPORTS_DIR, "reporte_servicios_especiales.pdf")
    archivo = ReporteServiciosEspeciales.exportar_pdf(datos, nombre_archivo=archivo_path)
    
    if archivo:
        return send_file(archivo, as_attachment=True)
        
    flash("No hay datos para exportar", "danger")
    return redirect(url_for('reporte_servicios_especiales'))

# ---------------- RUN ----------------
if __name__ == '__main__':
    # Usar puerto 5000 por defecto de Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
