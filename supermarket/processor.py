from database import Database
from flask_bcrypt import Bcrypt



bcrypt = Bcrypt()

class Processor:
    def __init__(self):
        self.db = Database()
        self.bcrypt = Bcrypt()

    def signup(self, data):
        try:
            # Map incoming data to the correct fields in the model
            user_data = {
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "age": data.get("age"),
                "sex": data.get("sex"),
                "contact_number": data.get("contact_number"),
                "email_id": data.get("email_id"),
                "normal_password": data.get("password"),  # Map 'password' to 'normal_password'
                "encrypted_password": self.bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
            }
            # Save the user to the database
            self.db.add_user(user_data)
            return {"message": "User registered successfully!", "status_code": 201}
        except Exception as e:
            return {"message": "Error registering user!", "error": str(e), "status_code": 500}


    def login(self, data):
        try:
            user = self.db.get_user_by_email(data['email_id'])
            if user and self.bcrypt.check_password_hash(user.encrypted_password, data['password']):
                return {"message": "Login successful!", "status_code": 200}
            return {"message": "Invalid credentials!", "status_code": 401}
        except Exception as e:
            return {"message": "Error logging in!", "error": str(e), "status_code": 500}

    def add_product(self, data):
        try:
            self.db.add_product(data)
            return {"message": "Product added successfully!", "status_code": 201}
        except Exception as e:
            return {"message": "Error adding product!", "error": str(e), "status_code": 500}

    def delete_product(self, product_id):
        try:
            self.db.delete_product(product_id)
            return {"message": "Product deleted successfully!", "status_code": 200}
        except Exception as e:
            return {"message": "Error deleting product!", "error": str(e), "status_code": 500}

    def update_product_rate(self, product_id, data):
        try:
            self.db.update_product_rate(product_id, data['rate'])
            return {"message": "Product rate updated successfully!", "status_code": 200}
        except Exception as e:
            return {"message": "Error updating product rate!", "error": str(e), "status_code": 500}

    def get_purchases(self, start_date, end_date):
        try:
            purchases = self.db.get_purchases(start_date, end_date)
            return {"total_purchases": len(purchases), "status_code": 200}
        except Exception as e:
            return {"message": "Error getting purchases!", "error": str(e), "status_code": 500}

    def get_users(self):
        try:
            users = self.db.get_users_with_high_purchase()
            return users
        except Exception as e:
            return {"message": "Error getting users!", "error": str(e), "status_code": 500}

    def get_shampoo_sales(self):
        try:
            sales = self.db.get_shampoo_sales()
            return {"total_sales": sales, "status_code": 200}
        except Exception as e:
            return {"message": "Error getting sales!", "error": str(e), "status_code": 500}
