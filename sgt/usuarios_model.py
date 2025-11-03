from sgt.db_config import get_connection

class UsuarioModel:
    @staticmethod
    def verificar_credenciales(email, password):
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        query = "SELECT id_usuario, nombre, correo, contraseña FROM usuarios WHERE correo=? AND contraseña=?"
        cursor.execute(query, (email, password))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {"id": row[0], "nombre": row[1], "correo": row[2]}
        return None
