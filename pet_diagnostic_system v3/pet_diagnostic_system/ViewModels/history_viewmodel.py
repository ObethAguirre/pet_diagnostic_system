import os
import glob

class HistoryViewModel:
    def __init__(self, main_app=None):
        self.main_app = main_app
        self.diagnosis_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'diagnosticos')
        )

    def navigate_to(self, index):
        if self.main_app:
            self.main_app.navigate_to(index)

    def load_diagnoses(self):
        diagnoses = []
        if os.path.exists(self.diagnosis_folder):
            for file in glob.glob(os.path.join(self.diagnosis_folder, "*.txt")):
                diagnoses.append(os.path.basename(file))
        return sorted(diagnoses)

    def read_diagnosis_file(self, filename):
        file_path = os.path.join(self.diagnosis_folder, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error al leer el archivo: {str(e)}"
