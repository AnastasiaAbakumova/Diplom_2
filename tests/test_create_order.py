import requests
import pytest
import allure
from conftest import BASE_URL

@allure.feature("Создание заказов")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и корректными ингредиентами")
    def test_create_order_with_ingredients(self, auth_token, ingredients_list):
        with allure.step("Формируем заголовки с токеном авторизации"):
            headers = {"Authorization": auth_token}
            data = {"ingredients": ingredients_list[:2]}  # берем 2 ингредиента

        with allure.step("Отправляем POST-запрос на создание заказа"):
            resp = requests.post(f"{BASE_URL}/orders", json=data, headers=headers)
            resp_json = resp.json()

        with allure.step("Проверяем, что заказ создан успешно"):
            assert resp.status_code == 200, "Сервер не вернул 200 OK"
            assert resp_json["success"] is True, "Заказ не был успешным"
            assert "order" in resp_json, "В ответе отсутствует ключ 'order'"
            assert "number" in resp_json["order"], "В ответе отсутствует номер заказа"

    @allure.title("Попытка создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self, auth_token):
        with allure.step("Формируем заголовки с токеном авторизации"):
            headers = {"Authorization": auth_token}
            data = {"ingredients": []}

        with allure.step("Отправляем POST-запрос на создание заказа без ингредиентов"):
            resp = requests.post(f"{BASE_URL}/orders", json=data, headers=headers)
            resp_json = resp.json()

        with allure.step("Проверяем, что сервер вернул 400 Bad Request"):
            assert resp.status_code == 400, "Сервер не вернул 400 Bad Request"
            assert resp_json["success"] is False, "Сервер вернул успех, хотя ингредиентов нет"
            assert resp_json["message"] == "Ingredient ids must be provided", "Сообщение об ошибке не соответствует документации"

    @allure.title("Попытка создать заказ с невалидным хешем ингредиента")
    def test_create_order_invalid_ingredient(self, auth_token):
        with allure.step("Формируем заголовки с токеном авторизации и невалидный хеш ингредиента"):
            headers = {"Authorization": auth_token}
            data = {"ingredients": ["invalid_hash"]}

        with allure.step("Отправляем POST-запрос"):
            resp = requests.post(f"{BASE_URL}/orders", json=data, headers=headers)
            resp_json = resp.json()

        with allure.step("Проверяем, что сервер вернул ошибку"):
            assert resp.status_code in [400, 500], f"Сервер вернул неожиданный код: {resp.status_code}"
            assert resp_json["success"] is False, "Сервер вернул успех при невалидном ингредиенте"
            assert any(keyword in resp_json["message"].lower() for keyword in ["ingredient", "ids"]), "Сообщение об ошибке не содержит ключевых слов 'ingredient' или 'ids'"
