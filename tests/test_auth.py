from fastapi.testclient import TestClient


def test_user_registration(client: TestClient):
    payload = {
        "username": "tester",
        "email": "tester@example.com",
        "password": "testerpassword"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "tester"
    assert data["email"] == "tester@example.com"
    assert "id" in data
    assert "hashed_password" not in data


def test_duplicate_registration(client: TestClient):
    payload = {
        "username": "tester",
        "email": "tester@example.com",
        "password": "testerpassword"
    }
    # First registration
    client.post("/auth/register", json=payload)
    # Duplicate registration
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_user_login(client: TestClient):
    # Register
    client.post("/auth/register", json={
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "loginpassword"
    })
    # Login
    response = client.post("/auth/token", data={
        "username": "loginuser",
        "password": "loginpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client: TestClient):
    response = client.post("/auth/token", data={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_current_user_profile(client: TestClient):
    # Register & Login
    client.post("/auth/register", json={
        "username": "profileuser",
        "email": "profileuser@example.com",
        "password": "profilepassword"
    })
    login_response = client.post("/auth/token", data={
        "username": "profileuser",
        "password": "profilepassword"
    })
    token = login_response.json()["access_token"]

    # Get Profile
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "profileuser"
