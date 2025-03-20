from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate
from app.db.database import get_db
from sqlalchemy.exc import IntegrityError
import pytest

client = TestClient(app)

@pytest.fixture
def mock_db(mocker):
    db = mocker.MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    yield db

def override_get_db(mock_db):
    yield mock_db

app.dependency_overrides[get_db] = override_get_db

def test_create_user(mock_db):
    user_data = {"name": "Alice", "email": "alice@example.com"}
    mock_user = User(**user_data)
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, "id", 1)
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"name": "Alice", "email": "alice@example.com", "id": 1}
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_create_user_duplicate_email(mock_db):
    user_data = {"name": "Alice", "email": "alice@example.com"}
    mock_db.add.side_effect = IntegrityError("mock", "mock", "mock")
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists"}

def test_get_users(mock_db):
    mock_users = [
        User(id=1, name="Alice", email="alice@example.com"),
        User(id=2, name="Bob", email="bob@example.com")
    ]
    mock_db.query.return_value.all.return_value = mock_users
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]

def test_get_user(mock_db):
    mock_user = User(id=1, name="Alice", email="alice@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice", "email": "alice@example.com"}

def test_get_user_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_update_user(mock_db):
    mock_user = User(id=1, name="Alice", email="alice@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    updated_data = {"name": "Alice Updated", "email": "alice.updated@example.com"}
    mock_db.commit.return_value = None
    def refresh_mock(user):
        user.name = updated_data["name"]
        user.email = updated_data["email"]
    mock_db.refresh.side_effect = refresh_mock
    response = client.put("/users/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice Updated", "email": "alice.updated@example.com"}
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_user)

def test_delete_user(mock_db):
    mock_user = User(id=1, name="Alice", email="alice@example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User 1 deleted"}
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()