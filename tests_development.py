## test production
import pytest
from fastapi.testclient import TestClient
# from main import application as app


# client = TestClient(app)

if __name__ == "__main__":
    pytest.main(args=[ "--cov=tests","tests/development","-s","--disable-warnings"])