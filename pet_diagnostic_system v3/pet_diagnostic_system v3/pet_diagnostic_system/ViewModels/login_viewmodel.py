class LoginViewModel:
    def __init__(self, main_app=None):
        self.main_app = main_app

    def validate_login(self, username, password):
        return username == "admin" and password == "admin"
