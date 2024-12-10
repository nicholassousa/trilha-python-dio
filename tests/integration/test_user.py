import pytest
from http import HTTPStatus
from sqlalchemy import func
from src.app import Role ,User, db

def test_get_user_success(client):
    # Given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    # Remove o usuário "john-doe" existente, se houver
    db.session.query(User).filter_by(username="john-doe").delete()
    db.session.commit()

    user = User(username="john-doe", password="test", role_id=role.id)
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

def test_create_user(client, access_token):
    
    # Given
    role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {"username": "User2", "password": "User2", "role_id": role_id}

    # When
    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"})
    
    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User Created!"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2

def test_list_users(client, access_token):
    # Given
    user = role_id = db.session.execute(db.select(User).where(User.username == "john-doe")).scalar()
    response = client.post("/auth/login", json={"username": user.username, "password": user.password})
    access_token = response.json["access_token"]

    # When
    response = client.get("/users/", headers={"Authorization": f"Bearer {access_token}"})

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == { 
        "users": [
        {
            "id":user.id,
            "username":user.username,
            "role_id": user.role_id,
            "role": {
                "id": user.role.id,
                "name": user.role.name,
            }
        }
    ]}  