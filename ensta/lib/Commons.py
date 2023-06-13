import string
import requests
import requests.cookies
import random
from .Exceptions import NetworkError


def update_app_id(self) -> None:
    app_id_occurrence_string = "\"APP_ID\":\""
    app_id_first_occurrence = self.homepage_source.index(app_id_occurrence_string)
    app_id_raw_text = self.homepage_source[
                      app_id_first_occurrence + len(app_id_occurrence_string): app_id_first_occurrence + 30]
    self.insta_app_id = app_id_raw_text[: app_id_raw_text.index("\"")]


def refresh_csrf_token(self) -> None:
    self.csrf_token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    cookie_object = requests.cookies.create_cookie(domain="instagram.com", name="csrftoken", value=self.csrf_token)
    self.request_session.cookies.set_cookie(cookie_object)


def update_session(self) -> None:
    self.request_session = requests.Session()


def update_homepage_source(self) -> None:
    temp_homepage_source = requests.get("https://www.instagram.com").text.strip()

    if temp_homepage_source != "":
        self.homepage_source = temp_homepage_source
    else:
        raise NetworkError("Couldn't load instagram homepage.")


def format_username(username: str) -> str:
    return username.replace(" ", "").lower()


def format_uid(uid: str) -> str:
    return uid.replace(" ", "")


def format_identifier(identifier: str | int) -> str:
    return str(identifier).lower().replace(" ", "")
