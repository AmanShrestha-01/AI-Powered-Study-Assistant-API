import json
from app import app, db

def get_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    with app.app_context():
        db.create_all()
    return app.test_client()

def get_token(client):
    client.post("/signup",
        data=json.dumps({"username": "testuser", "password": "testpass123"}),
        content_type="application/json"
    )
    response = client.post("/login",
        data=json.dumps({"username": "testuser", "password": "testpass123"}),
        content_type="application/json"
    )
    data = json.loads(response.data)
    return data["token"]

def test_home():
    client = get_client()
    response = client.get("/")
    assert response.status_code == 200
    print("PASS: Home route works")

def test_signup():
    client = get_client()
    response = client.post("/signup",
        data=json.dumps({"username": "newuser", "password": "pass123"}),
        content_type="application/json"
    )
    assert response.status_code == 201
    print("PASS: Signup works")

def test_login():
    client = get_client()
    client.post("/signup",
        data=json.dumps({"username": "loginuser", "password": "pass123"}),
        content_type="application/json"
    )
    response = client.post("/login",
        data=json.dumps({"username": "loginuser", "password": "pass123"}),
        content_type="application/json"
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "token" in data
    print("PASS: Login works")

def test_create_note():
    client = get_client()
    token = get_token(client)
    response = client.post("/notes",
        data=json.dumps({"title": "Test Note", "content": "Some test content here"}),
        content_type="application/json",
        headers={"Authorization": token}
    )
    assert response.status_code == 201
    print("PASS: Note creation works")

def test_notes_require_login():
    client = get_client()
    response = client.get("/notes")
    assert response.status_code == 401
    print("PASS: Notes reject unauthenticated users")

def test_usage():
    client = get_client()
    token = get_token(client)
    response = client.get("/usage", headers={"Authorization": token})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["remaining"] == 50
    print("PASS: Usage tracking works")

if __name__ == "__main__":
    test_home()
    test_signup()
    test_login()
    test_create_note()
    test_notes_require_login()
    test_usage()
    print("\nAll tests passed!")
