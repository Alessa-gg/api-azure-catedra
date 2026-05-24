from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modifica con los datos reales de tu Paso 1
DB_HOST = "://azure.com" 
DB_NAME = "postgres"
DB_USER = "admin_user"
DB_PASS = "Catedra2026*"

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, sslmode="require")

class Estudiante(BaseModel):
    nombres: str; apellidos: str; numero_carnet: str; edad: int

@app.get("/estudiantes")
def obtener_estudiantes():
    conn = get_db_connection(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT nombres, apellidos, numero_carnet, edad FROM estudiantes;")
    data = cur.fetchall(); cur.close(); conn.close()
    return data

@app.post("/estudiantes")
def crear_estudiante(estudiante: Estudiante):
    try:
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO estudiantes (nombres, apellidos, numero_carnet, edad) VALUES (%s, %s, %s, %s);",
                    (estudiante.nombres, estudiante.apellidos, estudiante.numero_carnet, estudiante.edad))
        conn.commit(); cur.close(); conn.close()
        return {"mensaje": "Estudiante registrado con éxito"}
    except Exception as e: raise HTTPException(status_code=400, detail=str(e))

@app.delete("/estudiantes/{carnet}")
def borrar_estudiante(carnet: str):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM estudiantes WHERE numero_carnet = %s;", (carnet,))
    conn.commit(); filas = cur.rowcount; cur.close(); conn.close()
    if filas == 0: raise HTTPException(status_code=404, detail="El carnet no existe")
    return {"mensaje": "Estudiante eliminado correctamente"}
