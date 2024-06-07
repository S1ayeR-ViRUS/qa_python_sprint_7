import random
import string
from faker import Faker
import json


class RandomCourierGeneration:

    @staticmethod
    def generate_random_courier_data():
        login = RandomCourierGeneration.generate_random_string(10)
        password = RandomCourierGeneration.generate_random_string(10)
        first_name = RandomCourierGeneration.generate_random_string(10)
        payload = {
            'login': login,
            'password': password,
            'firstName': first_name
        }
        return payload

    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string


class OrderDataGeneration:
    @staticmethod
    def generate_order_data(color):
        fake = Faker(locale='ru_RU')
        payload = {
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'address': fake.address(),
            'metroStation': random.randrange(10),
            'phone': fake.phone_number(),
            'rentTime': random.randrange(6),
            'deliveryDate': fake.date(),
            'color': color,
            'comment': fake.text(10)
        }
        return json.dumps(payload)
