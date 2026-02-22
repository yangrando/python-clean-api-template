def register_user(client):
    return client.post(
        "/register",
        json={"email": "dev@example.com", "password": "strong-password"},
    )


def login_user(client):
    return client.post(
        "/login",
        json={"email": "dev@example.com", "password": "strong-password"},
    )


def test_register_success(client):
    response = register_user(client)
    assert response.status_code == 201

    body = response.json()
    assert body["email"] == "dev@example.com"
    assert body["id"]


def test_login_success(client):
    register_user(client)
    response = login_user(client)

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_failure(client):
    response = client.post(
        "/login",
        json={"email": "dev@example.com", "password": "invalid-password"},
    )
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/me")
    assert response.status_code == 401


def test_ai_generate_success(client):
    register_user(client)
    login_response = login_user(client)
    token = login_response.json()["access_token"]

    response = client.post(
        "/generate",
        json={"prompt": "Write a short deployment checklist."},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["provider"] == "fake"
    assert "Simulated response" in data["response"]
