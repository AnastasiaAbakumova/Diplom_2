import pytest
import requests
import random
import string

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

def random_email():
    """Генерация уникального email для теста"""
    return "user_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6)) + "@yandex.ru"

@pytest.fixture
def unique_user():
    """Создаём уникального пользователя и возвращаем данные"""
    email = random_email()
    password = "password"
    name = "TestUser"
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": password,
        "name": name
    })
    return {"email": email, "password": password, "name": name, "response": response}

@pytest.fixture
def auth_token(unique_user):
    """Возвращает accessToken зарегистрированного пользователя"""
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": unique_user["email"],
        "password": unique_user["password"]
    })
    return resp.json().get("accessToken")

@pytest.fixture
def ingredients_list():
    """Возвращает список ID всех ингредиентов"""
    resp = requests.get(f"{BASE_URL}/ingredients")
    return [item["_id"] for item in resp.json()["data"]]
