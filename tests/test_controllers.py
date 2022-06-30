import requests

from src.apis.v1.core.project_settings import Settings

url = Settings().BASE_URL + "api/v1/user/profile_image/"

file = {'file': open('image.jpg', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.json())

file = {'file': open('image.png', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.json())