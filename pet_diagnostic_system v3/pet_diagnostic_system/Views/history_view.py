from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox

class DiagnosisHistoryView(QWidget):
    def __init__(self, viewmodel, main_app):
        super().__init__()
        self.viewmodel = viewmodel
        self.main_app = main_app

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Historial de Diagnósticos"))

        self.diagnosis_list = QListWidget()
        self.diagnosis_list.itemClicked.connect(self.show_diagnosis_detail)
        layout.addWidget(self.diagnosis_list)

        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.refresh_history)
        layout.addWidget(self.refresh_button)

        self.back_button = QPushButton("Volver al Menú")
        self.back_button.clicked.connect(lambda: self.main_app.navigate_to(1))
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.refresh_history()

    def refresh_history(self):
        self.diagnosis_list.clear()
        diagnoses = self.viewmodel.load_diagnoses_files()
        if diagnoses:
            for diag_file in diagnoses:
                self.diagnosis_list.addItem(diag_file)
        else:
            self.diagnosis_list.addItem("No hay diagnósticos registrados.")

    def show_diagnosis_detail(self, item):
        selected_file = item.text()
        if selected_file == "No hay diagnósticos registrados.":
            return

        try:
            content = self.viewmodel.read_diagnosis(selected_file)
            QMessageBox.information(self, f"Diagnóstico: {selected_file}", content)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el diagnóstico: {str(e)}")
