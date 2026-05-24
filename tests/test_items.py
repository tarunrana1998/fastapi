from fastapi.testclient import TestClient


def test_unauthenticated_item_creation_fails(client: TestClient):
    payload = {
        "name": "Item Pro",
        "description": "Fails without token",
        "price": 49.99,
        "tax": 5.0
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 401


def test_authenticated_item_creation_and_retrieval(client: TestClient):
    # Register & Login to get token
    client.post("/auth/register", json={
        "username": "itemcreator",
        "email": "creator@example.com",
        "password": "creatorpassword"
    })
    login_response = client.post("/auth/token", data={
        "username": "itemcreator",
        "password": "creatorpassword"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create item
    item_payload = {
        "name": "Super Item",
        "description": "Created successfully",
        "price": 12.34,
        "tax": 1.23
    }
    response = client.post("/items/", json=item_payload, headers=headers)
    assert response.status_code == 200
    item_data = response.json()
    assert item_data["name"] == "Super Item"
    assert "id" in item_data

    # Retrieve item publicly
    item_id = item_data["id"]
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    retrieved_data = get_response.json()
    assert retrieved_data["name"] == "Super Item"


def test_item_not_found(client: TestClient):
    response = client.get("/items/99999")
    assert response.status_code == 404
