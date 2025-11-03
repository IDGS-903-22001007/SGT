from sgt.db_config import get_connection
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# ------------------------- HU-02: Reporte de Abordajes Completo Actualizado -------------------------
class ReporteAbordajes:
    @staticmethod
    def obtener_abordajes(fecha=None, unidad=None):
        """Consulta los abordajes filtrando por fecha y unidad si se proporcionan."""
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
            SELECT servicio, unidad, fecha_abordaje, usuarios_abordados
            FROM abordajes
            WHERE 1=1
        """
        params = []

        # ✅ Solo agrega filtro si hay valor
        if fecha and fecha.strip():
            query += " AND CONVERT(date, fecha_abordaje) = CONVERT(date, ?)"
            params.append(fecha)
        if unidad and unidad.strip() and unidad.lower() != "none":
            query += " AND unidad = ?"
            params.append(unidad)

        query += " ORDER BY fecha_abordaje;"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append({
                "servicio": row[0],
                "unidad": row[1],
                "fecha": row[2].strftime("%Y-%m-%d"),
                "usuarios_abordados": row[3]
            })
        return result

    @staticmethod
    def exportar_excel(datos, nombre_archivo="reporte_abordajes.xlsx"):
        """Genera un archivo Excel con los datos del reporte."""
        if not datos:
            return None
        df = pd.DataFrame(datos)
        df.to_excel(nombre_archivo, index=False)
        return nombre_archivo

    @staticmethod
    def exportar_pdf(datos, nombre_archivo="reporte_abordajes.pdf"):
        """Genera un archivo PDF con los datos del reporte."""
        if not datos:
            return None

        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        ancho, alto = letter
        y = alto - 50

        # Título
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Reporte de Abordajes por Servicio")
        y -= 30

        # Encabezado
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Servicio | Unidad | Fecha | Usuarios Abordados")
        y -= 20

        # Datos
        c.setFont("Helvetica", 12)
        for fila in datos:
            texto = f"{fila['servicio']} | {fila['unidad']} | {fila['fecha']} | {fila['usuarios_abordados']}"
            c.drawString(50, y, texto)
            y -= 20
            if y < 50:
                c.showPage()
                y = alto - 50

        c.save()
        return nombre_archivo


# ------------------------- HU-03: Reporte de Servicios Especiales Completo  -------------------------
class ReporteServiciosEspeciales:
    @staticmethod
    def obtener_servicios(fecha_inicio=None, fecha_fin=None, nombre_servicio=None):
        """Consulta los servicios especiales filtrando por rango de fechas y nombre del servicio (opcional)."""
        conn = get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        query = """
            SELECT nombre_servicio, unidad, fecha_servicio, estado
            FROM servicios_especiales
            WHERE 1=1
        """
        params = []

        # ✅ Verificación robusta de valores antes de aplicar filtros
        def es_fecha_valida(valor):
            try:
                if valor and valor.strip():
                    pd.to_datetime(valor, errors='raise')  # valida que sea interpretable como fecha
                    return True
            except Exception:
                return False
            return False

        if es_fecha_valida(fecha_inicio):
            query += " AND CONVERT(DATE, fecha_servicio) >= CONVERT(DATE, ?)"
            params.append(fecha_inicio)

        if es_fecha_valida(fecha_fin):
            query += " AND CONVERT(DATE, fecha_servicio) <= CONVERT(DATE, ?)"
            params.append(fecha_fin)

        if nombre_servicio and nombre_servicio.strip() and nombre_servicio.lower() != "none":
            query += " AND nombre_servicio LIKE ?"
            params.append(f"%{nombre_servicio}%")

        query += " ORDER BY fecha_servicio;"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append({
                "nombre_servicio": row[0],
                "unidad": row[1],
                "fecha": row[2].strftime("%Y-%m-%d"),
                "estado": row[3]
            })
        return result

    @staticmethod
    def exportar_excel(datos, nombre_archivo="reporte_servicios_especiales.xlsx"):
        """Genera un archivo Excel con los datos de servicios especiales."""
        if not datos:
            return None
        df = pd.DataFrame(datos)
        df.to_excel(nombre_archivo, index=False)
        return nombre_archivo

    @staticmethod
    def exportar_pdf(datos, nombre_archivo="reporte_servicios_especiales.pdf"):
        """Genera un archivo PDF con los datos de servicios especiales."""
        if not datos:
            return None

        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        ancho, alto = letter
        y = alto - 50

        # Título
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Reporte de Servicios Especiales")
        y -= 30

        # Encabezado
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Nombre del Servicio | Unidad | Fecha | Estado")
        y -= 20

        # Datos
        c.setFont("Helvetica", 12)
        for fila in datos:
            texto = f"{fila['nombre_servicio']} | {fila['unidad']} | {fila['fecha']} | {fila['estado']}"
            c.drawString(50, y, texto)
            y -= 20
            if y < 50:
                c.showPage()
                y = alto - 50

        c.save()
        return nombre_archivo
