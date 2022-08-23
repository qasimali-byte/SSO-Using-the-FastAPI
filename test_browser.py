# pip install pytest-playwright    # this will install Playwrite too.
# playwright install   # this will install chromium browser driver.

import re
from playwright.sync_api import Page, expect

from src.apis.v1.controllers.user_controller import UserController
from src.apis.v1.db.session import get_db


def test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(page: Page):

    class user_data():
        email = "umair@gmail.com"
        id = "230"
    uc = UserController(db=get_db())
    user_key = uc.send_email_to_user(uc, user_data=user_data)
    user_key = UserController.reset_password_through_email("umair@gmail.com")

    page.goto(f"http://127.0.0.1:8000/api/v1/verify-email/{user_key}")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

    # create a locator
    get_started = page.locator("text=Get Started")

    # Expect an attribute "to be strictly equal" to the value.
    expect(get_started).to_have_attribute("href", "/docs/intro")

    # Click the get started link.
    get_started.click()

    # Expects the URL to contain intro.
    expect(page).to_have_url(re.compile(".*intro"))