from fastapi import FastAPI, HTTPException, status
from .modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from .modelos.facturas import Factura, FacturaCrear, FacturaEditar
from .modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from .enrutadores import clientes, facturas, transacciones

app = FastAPI()


lista_clientes: list[Cliente] = []
lista_facturas: list[Factura] = []
lista_transacciones : list[Transaccion] = []


#Incluir la ruta de clientes
app.include_router(clientes.rutas_clientes, tags=["Clientes"])
app.include_router(facturas.rutas_facturas, tags=["Facturas"])
app.include_router(transacciones.rutas_transacciones, tags=["Transacciones"])