from api import get_pets, add_pet, delete_pet

class PetRegistrationViewModel:
    def __init__(self, main_app=None):
        self.main_app = main_app

    def listar_mascotas(self):
        try:
            return get_pets()
        except Exception as e:
            print(f"Error al listar mascotas: {e}")
            return []

    def agregar_mascota(self, nombre, especie, breed, edad, propietario):
        if not nombre or not especie or not breed or not edad or not propietario:
            return False, "Por favor completa todos los campos."

        data = {
            "nombre": nombre.strip(),
            "especie": especie.strip(),
            "breed": breed.strip(),
            "edad": int(edad.strip()),
            "propietario": propietario.strip()
        }

        try:
            result = add_pet(data)
            return True, f"Mascota '{nombre}' registrada correctamente. ID: {result.get('id')}"
        except Exception as e:
            return False, f"Error al agregar mascota: {str(e)}"

    def eliminar_mascota(self, pet_id):
        try:
            result = delete_pet(pet_id)
            return True, f"Mascota eliminada correctamente. ID: {pet_id}"
        except Exception as e:
            return False, f"Error al eliminar mascota: {str(e)}"

    def navigate_to(self, index):
        if self.main_app:
            self.main_app.navigate_to(index)
