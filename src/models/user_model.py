from src import db

class User:
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def save(self):
        db.users.insert_one({
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "password": self.password
        })

    @staticmethod
    def find_by_email(email):
        return db.users.find_one({"email": email})
