from src.apis.v1.validators.user_validator import UserInfoValidator, UserSPPracticeRoleValidatorOut, UserValidatorOut
from test_production import client

def test_update_user_image(superuser_token_headers):
    file = files = [('image', ('capsule.jpg', open('capsule.jpg', 'rb'), 'image/jpeg'))]
    response = client.put("api/v1/user/profile-image",files=file,headers=superuser_token_headers)
    assert response.status_code == 201



def test_get_user_image(superuser_token_headers):

    response = client.get("api/v1/user/get-profile-image",headers=superuser_token_headers)
    assert response.status_code == 201


def test_serve_image():

    response = client.get("http://localhost:8088/api/v1/user/profile-image/NqQQrAi9_dp.jpeg")
    assert response.status_code == 200