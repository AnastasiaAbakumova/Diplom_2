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
    """Возвращает только данные нового уникального пользователя (без регистрации)"""
    return {
        "email": random_email(),
        "password": "password",
        "name": "TestUser"
    }

@pytest.fixture
def registered_user(unique_user):
    """Создаёт пользователя через API и возвращает его данные"""
    response = requests.post(f"{BASE_URL}/auth/register", json=unique_user)
    return {**unique_user, "response": response}

@pytest.fixture
def auth_token(registered_user):
    """Возвращает accessToken зарегистрированного пользователя"""
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    return resp.json().get("accessToken")

@pytest.fixture
def ingredients_list():
    """Возвращает список ID всех ингредиентов"""
    resp = requests.get(f"{BASE_URL}/ingredients")
    return [item["_id"] for item in resp.json()["data"]]
