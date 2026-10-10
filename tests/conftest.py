import pytest
from fastapi.testclient import TastClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

#use a separate SQLite database for testing
#so we never touch the real PostgreSQL data
SQLALCHEMY_TEST_DATABSE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABSE_URL,
    connect_args= {"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

def override_get_db():
    """
    replace the real databse with test database.
    FastAPI's Depends() will use this instead of get_db()
    during tests - so tests never touch real data.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_database():
    """
    Creates all tables before each test.
    Drops all tables after each test.
    This means every test starts with a clean state.
    """

    Base.metadata.create_all(bind = engine)
    app.dependency_overrides[get_db] = override_get_db
    yield 
    Base.metadata.drop_all(bind =engine)
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """
    Creates a test client that can make
    HTTP requests to your API without
    actually running a server.
    """
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    """
    Registers a user and returns their token.
    Used by tests that need an authenticated user.
    """

    response = client.post("/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    return response.json()["token"]