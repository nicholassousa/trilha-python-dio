import os
import sys
import pytest

import sys
import os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.app import create_app, db

@pytest.fixture()
def app():
    app = create_app({
        "SECRET_KEY": "test",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///blog.sqlite",
        "JWT_SECRET_KEY": "test",
    })
    # other setup can go here
    with app.app_context():
        db.create_all()
        yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()

print(f"este é o cmainho do src: {sys.path}", )