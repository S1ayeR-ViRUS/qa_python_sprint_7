import allure
import pytest
from helpers import RandomCourierGeneration
from scooter_api import CourierMethods


@allure.feature('Ручка /api/v1/courier')
class TestCreateCourier:
    @allure.description('Создание курьера с корректными данными. Получаем код 200 и сообщение \'ок\': true')
    def test_create_courier_success(self, create_and_delete_account_courier):
        create_courier = CourierMethods.create_courier(create_and_delete_account_courier)
        assert create_courier.status_code == 201 and create_courier.text == '{"ok":true}'

    @allure.description('Проверка невозможности создании курьера с существующим логином. Получаем ошибку 409')
    def test_cant_create_double_courier(self, create_and_delete_account_courier):
        user_data = CourierMethods.create_duplicate_courier(create_and_delete_account_courier)
        assert user_data.status_code == 409 and user_data.json()[
            'message'] == 'Этот логин уже используется. Попробуйте другой.'

    @allure.description('Проверка невозможности создании курьера, когда одно из полей не заполнено. '
                        'Получаем ошибку 400')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_create_courier_empty_field_error(self, field):
        user_data = RandomCourierGeneration().generate_random_courier_data()
        payload = user_data
        payload.pop(field)
        response = CourierMethods.create_courier(payload)
        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для создания учетной записи'
