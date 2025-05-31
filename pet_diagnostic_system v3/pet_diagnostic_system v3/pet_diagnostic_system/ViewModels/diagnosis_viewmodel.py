import os
import json
from datetime import datetime
from api import get_pets, delete_pet, add_pet

class DiagnosisViewModel:
    def __init__(self, main_app=None):
        self.main_app = main_app
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.diseases_file = os.path.join(base_path, 'data', 'diseases.json')
        self.diagnosis_folder = os.path.join(base_path, 'diagnosticos')

        if not os.path.exists(self.diagnosis_folder):
            os.makedirs(self.diagnosis_folder)

    def load_pets(self):
        try:
            pets_data = get_pets()
            pets = [f"{pet['nombre']} ({pet['especie']})" for pet in pets_data]
            return pets
        except Exception as e:
            print(f"Error al cargar mascotas: {e}")
            return []

    def load_symptoms(self):
        symptoms = set()
        if os.path.exists(self.diseases_file):
            with open(self.diseases_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                diseases_data = data.get('diseases', {})
                for disease_info in diseases_data.values():
                    symptoms.update(disease_info.get('symptoms', []))
        return sorted(list(symptoms))

    def save_diagnosis(self, pet_name_raw, selected_symptoms):
        # Separar nombre y especie
        pet_name = pet_name_raw.split(" (")[0]

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"diagnostico_{pet_name}_{timestamp}.txt"
        filepath = os.path.join(self.diagnosis_folder, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("===== REPORTE DE DIAGNÓSTICO VETERINARIO =====\n\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Nombre: {pet_name}\n")
                f.write("Síntomas: " + ', '.join(selected_symptoms) + "\n\n")

                # Procesar diagnóstico con lógica
                diseases_results = self.analyze_diagnosis(selected_symptoms)
                for disease, info in diseases_results.items():
                    f.write(f"🦠 {disease.upper()} ({info['probabilidad']}%)\n")
                    f.write(f"Gravedad: {info['gravedad']} | Contagioso: {info['contagioso']}\n")
                    f.write(f"Tratamiento: {info['tratamiento']}\n\n")

            if self.main_app:
                self.main_app.refresh_history()

            return True, f"Diagnóstico guardado en '{filename}'."
        except Exception as e:
            return False, f"Error al guardar diagnóstico: {str(e)}"

    def analyze_diagnosis(self, selected_symptoms):
        results = {}
        if os.path.exists(self.diseases_file):
            with open(self.diseases_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                diseases_data = data.get('diseases', {})
                for disease_name, disease_info in diseases_data.items():
                    disease_symptoms = set(disease_info.get('symptoms', []))
                    match_count = len(disease_symptoms.intersection(selected_symptoms))
                    total_symptoms = len(disease_symptoms)
                    probability = int((match_count / total_symptoms) * 100) if total_symptoms > 0 else 0
                    if probability > 0:
                        results[disease_name] = {
                            'probabilidad': probability,
                            'gravedad': disease_info.get('severity', 'desconocida'),
                            'contagioso': 'Sí' if disease_info.get('contagious', False) else 'No',
                            'tratamiento': disease_info.get('treatment', 'N/A')
                        }
        return results

    def delete_pet(self, pet_name_raw):
        pet_name = pet_name_raw.split(" (")[0]
        try:
            pets_data = get_pets()
            for pet in pets_data:
                if pet['nombre'] == pet_name:
                    pet_id = pet['id']
                    delete_pet(pet_id)
                    return True, f"Mascota '{pet_name}' eliminada correctamente."
            return False, f"Mascota '{pet_name}' no encontrada."
        except Exception as e:
            return False, f"Error al eliminar mascota: {str(e)}"

    def load_diagnoses_files(self):
        if os.path.exists(self.diagnosis_folder):
            return [f for f in os.listdir(self.diagnosis_folder) if f.endswith('.txt')]
        return []

    def read_diagnosis(self, filename):
        filepath = os.path.join(self.diagnosis_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
