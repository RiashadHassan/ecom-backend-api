from core.models import *
from product.models import *
from django.http import request
from cart.models import *
from order.models import *
from faker import Faker
from core.rest.tests.custom_data_generator import CustomOrderNo

faker = Faker()
import random, string


def generate_order_no():
    digits = random.randint(100000, 999999)
    letters = ""

    for i in range(4):
        char = random.choice(string.ascii_uppercase)
        letters += char

    return "#" + str(digits) + str(letters)

    # base_case:


def run():
    hah = generate_order_no()
    print(hah)
