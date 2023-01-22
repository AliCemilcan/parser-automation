import pytest
from config import settings
from database import Base, get_db
from fastapi.testclient import TestClient
from oauth2 import create_access_token
from repo import models

# from repo.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app

SQLALCHEMY_DATABASE_URL_ = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/fastapi_test"
print(SQLALCHEMY_DATABASE_URL_)
# responsible of sqlalchemy connecting to postgresql
engine = create_engine(SQLALCHEMY_DATABASE_URL_)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# models.Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/user", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev1@gmail.com", "password": "password123"}
    res = client.post("/user", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorize_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def create_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user["id"]},
        {"title": "4th title", "content": "4th content", "owner_id": test_user["id"]},
        {"title": "5th title", "content": "5th content", "owner_id": test_user2["id"]},
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
