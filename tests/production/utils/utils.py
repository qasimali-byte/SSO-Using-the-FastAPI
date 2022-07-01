from test_production import client

def get_superuser_token_headers():
    login_data = {
        "email": "umair@gmail.com",
        "password": "admin",
    }
    r = client.post("/api/v1/login", json=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers