import os
import sys
import pytest
from src.app import create_app, db, User, Role 

@pytest.fixture(scope="module")
def app():
    app = create_app({
        "SECRET_KEY": "test",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "JWT_SECRET_KEY": "test",
    })
    # other setup can go here
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def access_token(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    # Remove o usuário "john-doe" existente, se houver
    db.session.query(User).filter_by(username="john-doe").delete()
    db.session.commit()

    # Remove o usuário "User2" existente, se houver
    db.session.query(User).filter_by(username="User2").delete()
    db.session.commit()

    user = User(username="john-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    
    response = client.post("/auth/login", json={"username": user.username, "password": user.password})
    return response.json["access_token"]