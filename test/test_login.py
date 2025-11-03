# test/test_login.py

import pytest
from unittest.mock import patch, MagicMock

# Importa tu clase de modelo.
# ¡Esta es la línea que fallaba antes!
from sgt.usuarios_model import UsuarioModel 

# Definimos datos de prueba
USUARIO_VALIDO = "testuser"
PASS_CORRECTA = "password123"
PASS_INCORRECTA = "malapass"

# ----------------------------------------------------------------------
# Configuramos un Mock para la dependencia de la base de datos.
# Esto asegura que la prueba no toque la base de datos real.
# ----------------------------------------------------------------------

@pytest.fixture
def mock_db_connector():
    """Fixture que simula el conector de la base de datos."""
    # Aquí puedes simular cualquier objeto que 'UsuarioModel' dependa.
    # Si UsuarioModel inicializa la base de datos, usamos un mock de la clase.
    return MagicMock()

@pytest.fixture
@patch('sgt.usuarios_model.DatabaseConfig') # Reemplaza 'DatabaseConfig' con el nombre de tu clase de conexión a DB real
def usuario_model(MockDBConfig, mock_db_connector):
    """Fixture que crea una instancia de UsuarioModel con el DB mockeado."""
    # Aseguramos que la instancia de la DB devuelva nuestro mock_db_connector
    MockDBConfig.return_value.get_connection.return_value = mock_db_connector
    return UsuarioModel()

# ----------------------------------------------------------------------
# PRUEBAS UNITARIAS
# ----------------------------------------------------------------------

def test_login_success(usuario_model, mock_db_connector):
    """Prueba si el login funciona con credenciales válidas."""
    
    # ARRANGE: Simula que la DB encuentra al usuario con la contraseña correcta
    # Asume que tu método busca un usuario y lo devuelve (o True/False)
    
    # Puedes mockear el método que busca el usuario y hacerlo devolver un objeto usuario
    mock_user_data = {"username": USUARIO_VALIDO, "password_hash": "el_hash_de_la_password"}
    mock_db_connector.execute_query.return_value = [mock_user_data] 
    
    # ACT: Llama al método a probar
    # ASUME que tu método es 'validar_credenciales(username, password)'
    login_result = usuario_model.validar_credenciales(USUARIO_VALIDO, PASS_CORRECTA)
    
    # ASSERT: Verifica el resultado
    assert login_result is True
    
    # Opcional: Verifica que se llamó al conector
    mock_db_connector.execute_query.assert_called_once()


def test_login_failure_bad_password(usuario_model, mock_db_connector):
    """Prueba si el login falla con una contraseña incorrecta."""
    
    # ARRANGE: Simula que la DB encuentra al usuario (pero el modelo internamente comparará mal el hash)
    mock_user_data = {"username": USUARIO_VALIDO, "password_hash": "un_hash_diferente"}
    mock_db_connector.execute_query.return_value = [mock_user_data]
    
    # ACT
    login_result = usuario_model.validar_credenciales(USUARIO_VALIDO, PASS_INCORRECTA)
    
    # ASSERT
    assert login_result is False


def test_login_failure_user_not_found(usuario_model, mock_db_connector):
    """Prueba si el login falla cuando el usuario no existe."""
    
    # ARRANGE: Simula que la DB no devuelve resultados (lista vacía)
    mock_db_connector.execute_query.return_value = []
    
    # ACT
    login_result = usuario_model.validar_credenciales("usuario_inexistente", PASS_CORRECTA)
    
    # ASSERT
    assert login_result is False
