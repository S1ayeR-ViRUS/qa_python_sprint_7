import allure
from scooter_api import CourierMethods, OrderMethods


@allure.title('Ручка /api/v1/orders/')
class TestAcceptOrder:
    @allure.description('Успешное принятие заказа курьером. Получаем код 200 и сообщение \'ок\': true')
    def test_accept_order_success(self, create_and_delete_account_courier):
        id_order = OrderMethods.accept_order_and_take_id()
        login_courier = CourierMethods.create_and_login_courier(create_and_delete_account_courier)
        id_courier = login_courier.json()['id']
        response = OrderMethods.accept_order(id_order, id_courier)
        assert response.status_code == 200 and response.json() == {"ok": True}

    @allure.description('Проверка невозможности принятия заказа, если его уже взяли в работу. '
                        'Получаем код 409 и сообщение \'Этот заказ уже в работе\'')
    def test_accept_order_twice_error(self, create_and_delete_account_courier):
        id_order = OrderMethods.accept_order_and_take_id()
        login_courier = CourierMethods.create_and_login_courier(create_and_delete_account_courier)
        id_courier = login_courier.json()['id']
        OrderMethods.accept_order(id_order, id_courier)
        response = OrderMethods.accept_order(id_order, id_courier)
        assert response.status_code == 409 and response.json()['message'] == "Этот заказ уже в работе"

    @allure.description('Проверка невозможности принятия заказа, если не передать ID курьера. '
                        'Получаем код 400 и  сообщение \'Недостаточно данных для поиска\'')
    def test_accept_order_without_id_courier_error(self):
        id_order = OrderMethods.accept_order_and_take_id()
        response = OrderMethods.accept_order(id_order, '')
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для поиска'

    @allure.description('Проверка невозможности принятия заказа, если передать несуществующий ID курьера. '
                        'Получаем код 404')
    def test_accept_order_with_non_existent_id_courier_error(self):
        id_order = OrderMethods.accept_order_and_take_id()
        response = OrderMethods.accept_order(id_order, '0')
        assert response.status_code == 404 and response.json()['message'] == 'Курьера с таким id не существует'

    @allure.description('Проверка невозможности принятия заказа, если передать несуществующий ID заказа. '
                        'Получаем код 404 и сообщение \'Заказа с таким id не существует\'')
    def test_accept_order_with_non_existent_id_order_error(self, create_and_delete_account_courier):
        login_courier = CourierMethods.create_and_login_courier(create_and_delete_account_courier)
        id_courier = login_courier.json()['id']
        response = OrderMethods.accept_order('0', id_courier)
        assert response.status_code == 404 and response.json()['message'] == 'Заказа с таким id не существует'

    @allure.description('Проверка невозможности принятия заказа, если не передать  ID заказа. '
                        'Получаем код 400 и  сообщение \'Недостаточно данных для поиска\'')
    def test_accept_order_with_without_id_order_error(self, create_and_delete_account_courier):
        login_courier = CourierMethods.create_and_login_courier(create_and_delete_account_courier)
        id_courier = login_courier.json()['id']
        response = OrderMethods.accept_order('', id_courier)
        assert response.status_code == 400 and response.json()['message'] == 'Недостаточно данных для поиска'
