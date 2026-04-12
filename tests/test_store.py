import allure
import jsonschema
import requests
import pytest

from .conftest import create_pet
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3/"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_add_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

            with allure.step("Отправка запроса на размещение заказа"):
                response = requests.post(url=f"{BASE_URL}store/order", json=payload)
                response_json = response.json()

            with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
                assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
                jsonschema.validate(response_json, STORE_SCHEMA)

            with allure.step("Проверка параметров заказа в ответе"):
                assert response_json['id'] == payload['id'], "id заказа не совпадает с ожидаемым"
                assert response_json['petId'] == payload['petId'], "petId заказа не совпадает с ожидаемым"
                assert response_json['quantity'] == payload['quantity'], "quantity заказа не совпадает с ожидаемым"
                assert response_json['status'] == payload['status'], "status заказа не совпадает с ожидаемым"
                assert response_json['complete'] == payload['complete'], "complete заказа не совпадает с ожидаемым"


    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == 1

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self):
        with allure.step("Отправка запроса на удаление информации о питомце по ID"):
            response = requests.delete(url=f"{BASE_URL}store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации об удаленном заказе по ID"):
            response = requests.get(url=f"{BASE_URL}store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"


    @allure.title("Полуение информации о несуществующем заказе по ID")
    def test_get_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе по ID"):
            response = requests.get(url=f"{BASE_URL}store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"


    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение информации об инвентаре магазина"):
            response = requests.get(url=f"{BASE_URL}store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка параметров инвентаря в ответе"):
            assert response_json['approved'] == 57, "approved инвентаря не совпадает с ожидаемым"
            assert response_json['delivered'] == 50, "delivered инвентаря не совпадает с ожидаемым"

