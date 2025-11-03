import pyodbc

def get_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=RANGEL019\\MSSQLSERVER01;'
            'DATABASE=SGT_DB;'
            'UID=sa;'
            'PWD=root;'
        )
        return conn
    except Exception as e:
        print("Error de conexión a SQL Server:", e)
        return None
