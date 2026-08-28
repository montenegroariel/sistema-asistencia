from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict

app = FastAPI(
    title="API de Alumnos - Programación III",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# 1. MODELOS DE DATOS (Pydantic Schemas)
# ------------------------------------------------------------------------------

# Esquema base para las propiedades comunes de un Alumno
class AlumnoBase(BaseModel):
    nombre: str = Field(..., example="Juan Perez")
    dni: str = Field(..., min_length=7, max_length=8, example="40123456")
    asistencias: int = Field(default=0, ge=0, example=5)

# Esquema para crear un alumno (POST)
class AlumnoCreate(AlumnoBase):
    pass

# Esquema para actualización parcial (PATCH)
# Todos los campos son opcionales para permitir modificar solo lo necesario
class AlumnoUpdatePartial(BaseModel):
    nombre: Optional[str] = Field(None, example="Juan Carlos Perez")
    dni: Optional[str] = Field(None, min_length=7, max_length=8, example="40123456")
    asistencias: Optional[int] = Field(None, ge=0, example=6)

# Esquema de respuesta para el cliente (GET, POST, PUT, PATCH)
class AlumnoResponse(AlumnoBase):
    id: int


# ------------------------------------------------------------------------------
# 2. BASE DE DATOS EN MEMORIA Y CONTADOR AUTOINCREMENTAL
# ------------------------------------------------------------------------------
db_alumnos: Dict[int, dict] = {
    1: {"id": 1, "nombre": "Carlos Gomez", "dni": "38999111", "asistencias": 12},
    2: {"id": 2, "nombre": "Maria Rodriguez", "dni": "41222333", "asistencias": 10}
}
current_id = 2


# ------------------------------------------------------------------------------
# 3. ENDPOINTS DE LA API (CRUD)
# ------------------------------------------------------------------------------

# GET - Obtener todos los alumnos
@app.get("/alumnos", response_model=Dict[str, dict], status_code=status.HTTP_200_OK)
def get_todos_los_alumnos():
    return {"data": db_alumnos}


# GET - Obtener un alumno específico por ID
@app.get("/alumnos/{alumno_id}", response_model=AlumnoResponse, status_code=status.HTTP_200_OK)
def get_alumno_por_id(alumno_id: int):
    if alumno_id not in db_alumnos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con ID {alumno_id} no encontrado"
        )
    return db_alumnos[alumno_id]


# POST - Crear un nuevo alumno
@app.post("/alumnos", response_model=AlumnoResponse, status_code=status.HTTP_201_CREATED)
def crear_alumno(alumno: AlumnoCreate):
    global current_id
    current_id += 1
    
    nuevo_alumno = {
        "id": current_id,
        "nombre": alumno.nombre,
        "dni": alumno.dni,
        "asistencias": alumno.asistencias
    }
    
    db_alumnos[current_id] = nuevo_alumno
    return nuevo_alumno


# PUT - Reemplazo COMPLETO de un alumno
@app.put("/alumnos/{alumno_id}", response_model=AlumnoResponse, status_code=status.HTTP_200_OK)
def reemplazar_alumno(alumno_id: int, alumno_data: AlumnoCreate):
    if alumno_id not in db_alumnos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con ID {alumno_id} no encontrado para actualizar"
        )
    
    # PUT exige sobrescribir el objeto entero con los datos enviados
    alumno_reemplazado = {
        "id": alumno_id,
        "nombre": alumno_data.nombre,
        "dni": alumno_data.dni,
        "asistencias": alumno_data.asistencias
    }
    
    db_alumnos[alumno_id] = alumno_reemplazado
    return alumno_reemplazado


# PATCH - Actualización PARCIAL de un alumno
@app.patch("/alumnos/{alumno_id}", response_model=AlumnoResponse, status_code=status.HTTP_200_OK)
def actualizar_parcial_alumno(alumno_id: int, alumno_data: AlumnoUpdatePartial):
    if alumno_id not in db_alumnos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con ID {alumno_id} no encontrado para actualizar"
        )
    
    alumno_existente = db_alumnos[alumno_id]
    # Extraemos solo los campos recibidos en el request body que NO sean None
    datos_a_actualizar = alumno_data.model_dump(exclude_unset=True)
    
    # Se actualizan únicamente las llaves provistas sin borrar las demás
    alumno_existente.update(datos_a_actualizar)
    db_alumnos[alumno_id] = alumno_existente
    
    return alumno_existente


# DELETE - Eliminar un alumno
@app.delete("/alumnos/{alumno_id}", status_code=status.HTTP_200_OK)
def eliminar_alumno(alumno_id: int):
    if alumno_id not in db_alumnos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con ID {alumno_id} no encontrado para eliminar"
        )
    
    alumno_eliminado = db_alumnos.pop(alumno_id)
    return {
        "mensaje": "Alumno eliminado exitosamente",
        "alumno": alumno_eliminado
    }