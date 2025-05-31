from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class PetRegistrationView(QWidget):
    def __init__(self, viewmodel, main_app):
        super().__init__()
        self.viewmodel = viewmodel
        self.main_app = main_app

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Registro de Mascota"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre")
        layout.addWidget(self.name_input)

        self.species_input = QLineEdit()
        self.species_input.setPlaceholderText("Especie")
        layout.addWidget(self.species_input)

        self.breed_input = QLineEdit()
        self.breed_input.setPlaceholderText("Raza")
        layout.addWidget(self.breed_input)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Edad")
        layout.addWidget(self.age_input)

        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("Propietario")
        layout.addWidget(self.owner_input)

        self.save_button = QPushButton("Registrar Mascota")
        self.save_button.clicked.connect(self.register_pet)
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Volver al Menú")
        self.back_button.clicked.connect(lambda: self.main_app.navigate_to(1))
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def register_pet(self):
        nombre = self.name_input.text()
        especie = self.species_input.text()
        breed = self.breed_input.text()
        edad = self.age_input.text()
        propietario = self.owner_input.text()

        success, message = self.viewmodel.agregar_mascota(nombre, especie, breed, edad, propietario)
        if success:
            QMessageBox.information(self, "Éxito", message)
            self.clear_fields()
        else:
            QMessageBox.warning(self, "Error", message)

    def clear_fields(self):
        self.name_input.clear()
        self.species_input.clear()
        self.breed_input.clear()
        self.age_input.clear()
        self.owner_input.clear()
