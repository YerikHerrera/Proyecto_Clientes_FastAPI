from fastapi import FastAPI, HTTPException, status
from .enrutadores.clientes import rutas_clientes
from .enrutadores.facturas import rutas_facturas
from .enrutadores.transacciones import rutas_transacciones
from .conexion_bd import crear_tablas

app = FastAPI(lifespan=crear_tablas)


#Incluir la ruta de clientes
app.include_router(rutas_clientes, tags=["Clientes"])
app.include_router(rutas_facturas, tags=["Facturas"])
app.include_router(rutas_transacciones, tags=["Transacciones"])
