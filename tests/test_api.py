import httpx
import pytest

from app.models import Store, store as _store

BASE = "http://test"


@pytest.fixture()
def client() -> httpx.Client:
    from app.main import app
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c


def test_health(client: httpx.Client) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_list_tasks(client: httpx.Client) -> None:
    r = client.get("/api/tasks")
    assert r.status_code == 200
    tasks = r.json()
    assert len(tasks) >= 4
    assert all("reward" in t for t in tasks)


def test_filter_category(client: httpx.Client) -> None:
    r = client.get("/api/tasks", params={"category": "data"})
    assert r.status_code == 200
    assert all(t["category"] == "data" for t in r.json())


def test_claim_submit_approve_flow(client: httpx.Client) -> None:
    r = client.post("/api/tasks/claim", json={"userId": "u1", "taskId": "t1"})
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"

    r = client.post("/api/tasks/submit", json={"userId": "u1", "taskId": "t1", "result": "a=car,b=truck"})
    assert r.status_code == 200
    assert r.json()["status"] == "submitted"

    r = client.post("/api/tasks/t1/approve")
    assert r.status_code == 200
    assert r.json()["status"] == "paid"

    r = client.get("/api/users/u1")
    assert r.json()["balance"] == pytest.approx(2.5)


def test_claim_twice_fails(client: httpx.Client) -> None:
    client.post("/api/tasks/claim", json={"userId": "u1", "taskId": "t2"})
    r = client.post("/api/tasks/claim", json={"userId": "u1", "taskId": "t2"})
    assert r.status_code == 409
