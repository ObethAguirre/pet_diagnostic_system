import json
from pathlib import Path

class PetRegistry:
    def __init__(self, filepath=Path('data/pets.json')):
        self.filepath = filepath
        self.pets = self.load_pets()

    def load_pets(self):
        if self.filepath.exists():
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_pets(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.pets, f, indent=4)

    def add_pet(self, pet_info):
        self.pets.append(pet_info)
        self.save_pets()

    def get_pets(self):
        return self.pets
