from starlette.testclient import TestClient 

from app.main import app

# client = TestClient(app) # use Pytest Fixture instead

def test_ping(test_app):
    #  response = client.get("/ping")
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping":"pong"}

