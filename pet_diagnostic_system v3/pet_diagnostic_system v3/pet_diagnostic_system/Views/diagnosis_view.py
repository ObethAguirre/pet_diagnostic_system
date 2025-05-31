from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
    QPushButton, QMessageBox, QScrollArea, QHBoxLayout
)

class DiagnosisView(QWidget):
    def __init__(self, viewmodel, main_app):
        super().__init__()
        self.viewmodel = viewmodel
        self.main_app = main_app

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Diagnóstico de Mascota"))

        self.pet_selector = QComboBox()
        self.update_pet_selector()
        layout.addWidget(QLabel("Selecciona una mascota:"))
        layout.addWidget(self.pet_selector)

        layout.addWidget(QLabel("Selecciona los síntomas:"))

        self.symptom_checkboxes = []
        scroll_area = QScrollArea()
        symptom_container = QWidget()
        symptom_layout = QVBoxLayout()

        symptoms = self.viewmodel.load_symptoms()
        for symptom in symptoms:
            checkbox = QCheckBox(symptom)
            self.symptom_checkboxes.append(checkbox)
            symptom_layout.addWidget(checkbox)

        symptom_container.setLayout(symptom_layout)
        scroll_area.setWidget(symptom_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(200)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()

        self.diagnose_button = QPushButton("Diagnosticar")
        self.diagnose_button.clicked.connect(self.perform_diagnosis)

        self.delete_button = QPushButton("Eliminar Mascota")
        self.delete_button.clicked.connect(self.delete_selected_pet)

        self.back_button = QPushButton("Volver al Menú")
        self.back_button.clicked.connect(lambda: self.main_app.navigate_to(1))

        button_layout.addWidget(self.diagnose_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_pet_selector(self):
        self.pet_selector.clear()
        pets = self.viewmodel.load_pets()
        if pets:
            self.pet_selector.addItems(pets)
        else:
            QMessageBox.warning(self, "Error", "No se pudieron cargar las mascotas.")

    def perform_diagnosis(self):
        pet_name = self.pet_selector.currentText()
        selected_symptoms = [cb.text() for cb in self.symptom_checkboxes if cb.isChecked()]

        if not pet_name:
            QMessageBox.warning(self, "Error", "Por favor selecciona una mascota.")
            return

        if not selected_symptoms:
            QMessageBox.warning(self, "Error", "Por favor selecciona al menos un síntoma.")
            return

        success, message = self.viewmodel.save_diagnosis(pet_name, selected_symptoms)
        if success:
            QMessageBox.information(self, "Diagnóstico", message)
            for cb in self.symptom_checkboxes:
                cb.setChecked(False)
        else:
            QMessageBox.warning(self, "Error", message)

    def delete_selected_pet(self):
        pet_name = self.pet_selector.currentText()
        if not pet_name:
            QMessageBox.warning(self, "Error", "Por favor selecciona una mascota para eliminar.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar la mascota '{pet_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            success, message = self.viewmodel.delete_pet(pet_name)
            if success:
                QMessageBox.information(self, "Éxito", message)
                self.update_pet_selector()
            else:
                QMessageBox.warning(self, "Error", message)
