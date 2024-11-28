import pytest
from http import HTTPStatus
from src.app import Role ,User, db

def test_get_user_success(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="jhon-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # When
    response = client.get(f"/users/{user.id}")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"id": user.id,"username": user.username}

def test_get_user_fail(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user_id = 4 # modei para 4 pq já tinhamos usuarios com id 1 e 2

    # When
    response = client.get(f"/users/{user_id}")

    # Then

    assert response.status_code == HTTPStatus.NOT_FOUND

def test_list_users(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    
    user = User(username="jhon-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # When
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK