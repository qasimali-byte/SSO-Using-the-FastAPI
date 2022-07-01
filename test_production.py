## test production

import pytest
from fastapi.testclient import TestClient
from main import application as app
from tests.production.api_v1.db import override_get_db
from src.apis.v1.db.session import get_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

if __name__ == "__main__":
    pytest.main(args=[ "--cov=tests","tests/production","-s","--disable-warnings"])