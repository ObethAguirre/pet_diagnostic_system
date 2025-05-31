from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginView(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Iniciar Sesión"))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Ingresar")
        self.login_button.clicked.connect(self.validate_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def validate_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "1234":  # Simulación
            self.main_app.navigate_to(1)  # Ir al menú principal
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
