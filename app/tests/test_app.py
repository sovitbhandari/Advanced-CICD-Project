from app.app import app
def test_health():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
