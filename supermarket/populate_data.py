import string
import random
import bcrypt
from flask_bcrypt import generate_password_hash
from faker import Faker
from database import *
from initiator import app

fake = Faker()

def populate_user_details():
    for _ in range(50):
        # Generate random email
        email = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@gmail.com'

        # Generate random password
        password = fake.password()

        user = UserDetails(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            age=fake.random_int(min=18, max=65),
            sex=fake.random_element(elements=('Male', 'Female')),
            contact_number=fake.random_number(digits=10),
            email_id=email,
            normal_password=password,
            encrypted_password=generate_password_hash(password).decode('utf-8')
        )

        store_user = StoreUserDetails(
            first_name=user.first_name,
            last_name=user.last_name,
            age=user.age,
            sex=user.sex,
            contact_number=user.contact_number,
            email_id=user.email_id,
            normal_password=user.normal_password,
            encrypted_password=user.encrypted_password,
            designation=random.choice(["Manager", "Salesman"])
        )

        db.session.add(user)
        db.session.add(store_user)

        # purchases = Purchases(
        #     user_id=user.user_id,
        #     item_name=fake.random_element(elements=('Soap', 'Shampoo', 'Toothpaste', 'Facewash', 'Bodywash', 'Perfume')),
        #     quantity=fake.random_int(min=1, max=10),
        #     rate=fake.random_int(min=10, max=100),
        #     purchase_date=fake.date()
        # )

        
        # db.session.add(purchases)
    db.session.commit()


# def populate_store_user_details():
#     for _ in range(20):
#         # Get the email from the UserDetails table
#         user = UserDetails.query.first()

#         store_user = StoreUserDetails(
#             first_name=user.first_name,
#             last_name=user.last_name,
#             age=user.age,
#             sex=user.sex,
#             contact_number=user.contact_number,
#             email_id=user.email_id,
#             normal_password=user.normal_password,
#             encrypted_password=user.encrypted_password,
#             designation=random.choice(["Manager", "Salesman"])
#         )

#         db.session.add(store_user)
#     db.session.commit()


def populate_purchases():
    for _ in range(50):
        # Get the email from the UserDetails table
        users = UserDetails.query.all()
        user = random.choice(users)
        purchase = Purchases(
            user_id=user.user_id,
            item_name=fake.random_element(elements=('Soap', 'Shampoo', 'Toothpaste', 'Facewash', 'Bodywash', 'Perfume')),
            quantity=fake.random_int(min=1, max=10),
            rate=fake.random_int(min=10, max=100),
            purchase_date = fake.date_between(start_date=datetime(2024, 11, 21), end_date=datetime.now())
        )

        db.session.add(purchase)
    db.session.commit()


def populate_products():
    for _ in range(50):
        product = Products(
            product_name=fake.random_element(elements=('Soap', 'Shampoo', 'Toothpaste', 'Facewash', 'Bodywash', 'Perfume')),
            rate=fake.random_int(min=10, max=100),
            stock=fake.random_int(min=10, max=100)
        )
        db.session.add(product)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        populate_user_details()
        populate_purchases()
        populate_products()
