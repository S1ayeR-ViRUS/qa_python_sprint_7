import requests
import pytest
from urls import Urls
from helpers import RandomCourierGeneration


@pytest.fixture(scope='function')
def create_and_delete_account_courier():
    data_payload = RandomCourierGeneration.generate_random_courier_data()
    yield data_payload
    requests.post(Urls.URL_MAIN + Urls.URL_CREATE_COURIER, data=data_payload)
    login = requests.post(Urls.URL_MAIN + Urls.URL_LOGIN_COURIER, data=data_payload)
    id_courier = login.json()['id']
    requests.delete(Urls.URL_MAIN + Urls.URL_CREATE_COURIER + str(id_courier))
