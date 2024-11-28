import os
import sys
from unittest.mock import patch #  mock serve para testar trechos de codigo com depedencias
import pytest
from http import HTTPStatus
from src.utils import eleva_quadrado, requires_role

@pytest.mark.parametrize("test_input, expected", [(2, 4), (10, 100), (3, 9)]) # são 2 elementos par nosso teste, test_input e expected
# test_input = operação que vamos realizar, expected = o resultado CORRETO que deve ser alcançado.
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input) # tornamos a função dinamica, respondendo a todos os resultados
    assert resultado == expected # 

@pytest.mark.parametrize(
        "test_input, exc_class, msg", 
        [
            ("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'" ),
            (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'"), 
        ]
    )
def test_eleva_quadrado_falha(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
    assert str(exc.value) == msg

def test_requile_role_success(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = 'admin'
    mocker.patch('src.utils.get_jwt_identity'), mocker.patch('src.utils.db.get_or_404', return_value=mock_user)

    decorated_function = requires_role('admin')(lambda: "success") # lambda é uma função anonima apenas para retornar success caso o usuario
    # tenha a role de 'admin'

    # When
    result = decorated_function()
    
    # Then
    assert result == "success"

def test_requile_role_fail(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = 'normal'
    mocker.patch('src.utils.get_jwt_identity'), mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    
    # When
    decorated_function = requires_role('admin')(lambda: "success")
    result = decorated_function()
    
    # Then
    assert result == ({'message': "User doesn't have access."}, HTTPStatus.FORBIDDEN)