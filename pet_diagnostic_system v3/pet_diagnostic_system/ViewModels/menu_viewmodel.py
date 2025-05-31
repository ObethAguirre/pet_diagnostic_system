class MenuViewModel:
    def __init__(self, main_app=None):
        self.main_app = main_app

    def navigate_to(self, index):
        if self.main_app:
            self.main_app.navigate_to(index)

    def logout(self):
        if self.main_app:
            self.main_app.logout()
