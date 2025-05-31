import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pet(BaseModel):
    id: int | None = None
    nombre: str
    especie: str
    breed: str
    edad: int
    propietario: str

# Construir ruta absoluta de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

print(f"Ruta de la base de datos: {db_path}")

def init_db():
    try:
        # Comprobar si el directorio base existe
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

        # Forzar permisos de escritura en la base de datos (Windows)
        if not os.access(BASE_DIR, os.W_OK):
            raise PermissionError(f"No se tienen permisos de escritura en {BASE_DIR}")

        # Conectar a la base de datos
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                especie TEXT,
                breed TEXT,
                edad INTEGER,
                propietario TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada correctamente.")
    except Exception as e:
        print(f"⚠️ Error al inicializar la base de datos: {e}")

init_db()

@app.get("/pets")
def get_pets():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pets")
    pets = cursor.fetchall()
    conn.close()
    return [{"id": p[0], "nombre": p[1], "especie": p[2], "breed": p[3], "edad": p[4], "propietario": p[5]} for p in pets]

@app.post("/pets")
def add_pet(pet: Pet):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pets (nombre, especie, breed, edad, propietario) VALUES (?, ?, ?, ?, ?)",
                   (pet.nombre, pet.especie, pet.breed, pet.edad, pet.propietario))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"message": "Mascota agregada", "id": new_id}

@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
    conn.commit()
    conn.close()
    return {"message": "Mascota eliminada"}
