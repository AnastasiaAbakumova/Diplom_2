import requests
import pytest
import allure
from conftest import BASE_URL, unique_user

@allure.feature("Регистрация пользователей")
class TestUserRegistration:

    @allure.title("Создание уникального пользователя должно проходить успешно")
    def test_create_unique_user(self, unique_user):
        with allure.step("Берём данные уникального пользователя, созданного через фикстуру"):
            response = unique_user["response"]
        
        with allure.step("Проверяем, что сервер вернул код 200 и success=True"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
        
        with allure.step("Проверяем, что email и имя совпадают с ожидаемыми"):
            assert data["user"]["email"] == unique_user["email"]
            assert data["user"]["name"] == unique_user["name"]

    @allure.title("Попытка создать пользователя с уже существующим email должна вернуть ошибку")
    def test_create_existing_user(self, unique_user):
        with allure.step("Формируем данные для регистрации с уже существующим email"):
            payload = {
                "email": unique_user["email"],
                "password": unique_user["password"],
                "name": unique_user["name"]
            }
        
        with allure.step("Отправляем POST-запрос на регистрацию"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        
        with allure.step("Проверяем, что сервер вернул код 403 и сообщение об ошибке"):
            assert response.status_code == 403
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "User already exists"

    @pytest.mark.parametrize(
        "payload, missing_field",
        [
            ({"password": "password", "name": "TestUser"}, "email"),
            ({"email": "test@example.com", "name": "TestUser"}, "password"),
            ({"email": "test@example.com", "password": "password"}, "name"),
        ]
    )
    @allure.title("Попытка создать пользователя без одного из обязательных полей")
    def test_create_user_missing_field(self, payload, missing_field):
        with allure.step(f"Формируем данные для регистрации без поля {missing_field}"):
            pass  # payload уже передан через параметризацию

        with allure.step("Отправляем POST-запрос на регистрацию"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)

        with allure.step("Проверяем, что сервер вернул код 403 и сообщение о недостающих полях"):
            assert response.status_code == 403
            data = response.json()
            assert data["success"] is False
            assert "required fields" in data["message"]
