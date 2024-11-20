from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from sqlalchemy import inspect
from src.controllers.role import Role
from sqlalchemy.orm import selectinload
from flask_jwt_extended import jwt_required
from src.utils import requires_role

app = Blueprint('user', __name__, url_prefix='/users')

def _create_user():  # Vamos criar as funções CRUD na nossa API
    data = request.json

    # Pegando a Role do banco de dados
    role = db.get_or_404(Role, data["role_id"])

    # Criando o usuário e associando a role
    user = User(
        username=data["username"],
        password=data["password"],
        role=role  # Associando a role diretamente, não apenas o role_id
    )
    
    # Adicionando o usuário ao banco
    db.session.add(user)
    db.session.commit()

def _list_users():
    query = db.select(User).options(selectinload(User.role))  # Usando selectinload
    users = db.session.execute(query).scalars().all()
    return [
        {
            "id":user.id,
            "username":user.username,
            "role_id": user.role_id,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            }
        }
        for user in users
    ]

@app.route('/', methods=['GET', 'POST'])
@jwt_required()
@requires_role("admin")
def list_or_create_user():
    if request.method == 'POST':
        _create_user()
        return {'message': 'User Created!'}, HTTPStatus.CREATED
    else:
        return {"message": _list_users()}, HTTPStatus.OK


    
@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }

@app.route('/<int:user_id>', methods=["PATCH"]) 
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
        db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }

@app.route('/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT