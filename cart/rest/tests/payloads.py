from faker import Faker

faker = Faker()


def cart_item_create_payload():
    return {
        "product_uuid": "",
        "quantity": faker.random_int(min=1, max=10),
    }


def order_item_review_payload():
    return {"rating": faker.random_int(min=1, max=5), "review": faker.sentence()}
