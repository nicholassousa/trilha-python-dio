from flask import Blueprint, request
from src.app import User, db, Role
from http import HTTPStatus


app = Blueprint('role', __name__, url_prefix='/roles')


@app.route("/", methods=['POST'])
def create_role():
        data = request.json
        role = Role(name=data['name'])
        db.session.add(role)
        db.session.commit()
        return {'messege': 'role Created!'}, HTTPStatus.CREATED # 201 é o estatus para created ok , ous seja, o estatus para dizer que deu certo