# test_login.py
from sgt.usuarios_model import UsuarioModel

def test_verificar_credenciales_validas():
    """Debe retornar un usuario válido si las credenciales existen."""
    usuario = UsuarioModel.verificar_credenciales("admin@example.com", "1234")
    assert usuario is not None
    assert "nombre" in usuario

def test_verificar_credenciales_invalidas():
    """Debe retornar None si las credenciales no existen."""
    usuario = UsuarioModel.verificar_credenciales("fake@example.com", "wrongpass")
    assert usuario is None
