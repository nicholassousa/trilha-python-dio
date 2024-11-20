from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

app = Blueprint('auth', __name__, url_prefix='/auth')

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar() # busca no banco com username
    if not user or password != password:
        return ({"massege": "Bad username or password"}), HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}