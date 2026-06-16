from fastapi import FastAPI, Depends
from typing import Annotated 
from sqlmodel import Session, SQLModel, create_engine

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

#Motor de bd
motor_bd = create_engine(url_bd)


#Definir el metodo para crear las tablas
def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield #No hay nada para retornar o ejecutar

#Definir el metodo para la sesion
def obtener_sesion():
    with Session(motor_bd) as mi_sesion:
        yield mi_sesion #retorna la sesion

#Denominando inyección de dependencias
#Registrar la sesion como dependencia, utilizada en nuestros endpoint
Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]
