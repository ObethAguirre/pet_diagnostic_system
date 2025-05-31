import requests

API_URL = "http://127.0.0.1:8000"

def get_pets():
    response = requests.get(f"{API_URL}/pets")
    response.raise_for_status()
    return response.json()

def add_pet(pet_data):
    response = requests.post(f"{API_URL}/pets", json=pet_data)
    response.raise_for_status()
    return response.json()

def delete_pet(pet_id):
    response = requests.delete(f"{API_URL}/pets/{pet_id}")
    response.raise_for_status()
    return response.json()
