import pytest
from config import settings
from database import Base, get_db
from fastapi.testclient import TestClient
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


@pytest.fixture(scope="module")
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
