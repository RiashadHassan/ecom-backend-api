from faker.providers import BaseProvider


class CustomDataGenerator(BaseProvider):
    def generate_phone_number(self):
        sim = str(self.random_element(["17", "18", "19", "16", "15"]))
        suffix = str(self.random_int(min=10000000, max=99999999))
        return "+880" + sim + suffix


import random
import string


def generate_random_order_no():
    digits = random.randint(100000, 999999)
    letters = ""

    for i in range(4):
        char = random.choice(string.ascii_uppercase)
        letters += char

    return "#" + str(digits) + str(letters)
