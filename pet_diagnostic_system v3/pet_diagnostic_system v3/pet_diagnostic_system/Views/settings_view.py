from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox

class SettingsView(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Configuración"))

        # Checkbox para tema oscuro
        self.theme_checkbox = QCheckBox("Tema Oscuro")
        self.theme_checkbox.setChecked(self.main_app.theme == "dark")
        self.theme_checkbox.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_checkbox)

        self.back_button = QPushButton("Volver al Menú")
        self.back_button.clicked.connect(lambda: self.main_app.navigate_to(1))
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def toggle_theme(self):
        theme = "dark" if self.theme_checkbox.isChecked() else "light"
        self.main_app.apply_theme(theme)
