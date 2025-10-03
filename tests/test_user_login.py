import requests
import pytest
import allure
from conftest import BASE_URL

@allure.feature("Авторизация пользователей")
class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        with allure.step(f"Пытаемся войти пользователем: {registered_user['email']}"):
            resp = requests.post(f"{BASE_URL}/auth/login", json={
                "email": registered_user["email"],
                "password": registered_user["password"]
            })
            data = resp.json()

        with allure.step("Проверяем статус ответа и успешность входа"):
            assert resp.status_code == 200, "Сервер не вернул 200 OK"
            assert data["success"] is True
            assert "accessToken" in data

    @pytest.mark.parametrize("email,password", [
        ("wrong_email@yandex.ru", "password"),
        ("wrong_email@yandex.ru", "wrong_password"),
        ("", "password"),
        ("user@example.com", "")
    ])
    @allure.title("Попытка входа с неверным логином или паролем")
    def test_login_invalid_credentials(self, email, password):
        with allure.step(f"Пытаемся войти с email: '{email}' и паролем: '{password}'"):
            resp = requests.post(f"{BASE_URL}/auth/login", json={
                "email": email,
                "password": password
            })
            data = resp.json()

        with allure.step("Проверяем, что сервер вернул 401 и сообщение об ошибке"):
            assert resp.status_code == 401, "Сервер не вернул 401 Unauthorized"
            assert data["success"] is False, "Успешный вход при неверных данных"
            assert data["message"] == "email or password are incorrect", "Сообщение об ошибке не соответствует ожиданию"
