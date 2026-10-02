import os

os.environ["MOCK_AI"] = "true"

os.environ["DATABASE_URL"] = (
    "sqlite:///./test_fitbuddy.db"
)

os.environ["ADMIN_KEY"] = "test-key"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_create_plan():

    payload = {

        "user_id": "TEST001",

        "name": "Test User",

        "age": 20,

        "weight_kg": 60,

        "goal": "general wellness",

        "intensity": "medium"
    }


    response = client.post(

        "/api/plans",

        json=payload
    )


    assert response.status_code == 200


    data = response.json()


    assert data["user_id"] == "TEST001"

    assert "DAY 1" in data["workout_plan"]


def test_feedback_update():

    payload = {

        "user_id": "TEST001",

        "feedback":
        "Add more mobility work and one recovery day."
    }


    response = client.post(

        "/api/plans/TEST001/feedback",

        json=payload
    )


    assert response.status_code == 200

    assert response.json()["updated"] is True


def test_get_user():

    response = client.get(
        "/api/users/TEST001"
    )


    assert response.status_code == 200

    assert response.json()["updated"] is True


def test_minor_guard():

    payload = {

        "user_id": "MINOR01",

        "name": "Young User",

        "age": 16,

        "weight_kg": 55,

        "goal": "weight loss",

        "intensity": "medium"
    }


    response = client.post(

        "/api/plans",

        json=payload
    )


    assert response.status_code == 422