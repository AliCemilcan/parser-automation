import pytest

from app import schemas

from .database import client, session


def test_root(client):
    res = client.get("/")
    res_message = res.json().get("message")
    assert res_message == "This is ACC speaking"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/user", json={"email": "user23@example.com", "password": "123asd12"}
    )
    response = res.json()
    new_user = schemas.UserOut(**response)

    assert new_user.email == "user23@example.com"
    assert res.status_code == 201


def test_login_user(client):
    res = client.post(
        "/login", data={"username": "user23@example.com", "password": "123asd12"}
    )
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user23@example.com", "123asd125", 403),
        ("user2344@example.com", "123asd12", 403),
        ("user2344@example.com", "123asd125", 403),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    assert res.json().get("detail") == "Invalid Credentials"
