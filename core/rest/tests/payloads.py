from faker import Faker

from .custom_data_generator import CustomDataGenerator

faker = Faker()
custom_generator = CustomDataGenerator(faker)


def user_create_payload():
    return {
        "phone_number": custom_generator.generate_phone_number(),
        "password": faker.password(),
        "username": faker.name(),
    }
