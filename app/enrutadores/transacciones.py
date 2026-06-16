from fastapi import APIRouter, HTTPException, status
from ..modelos.transacciones import Transaccion, TransaccionCrear, TransaccionEditar
from ..modelos.facturas import Factura
from ..listas import lista_facturas, lista_transacciones

rutas_transacciones = APIRouter()


#lista_facturas: list[Factura] = []
#lista_transacciones: list[Transaccion] = []


@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones():
    return lista_transacciones


@rutas_transacciones.get("/transacciones/{id_transaccion}", response_model=Transaccion)
async def listar_transaccion(id_transaccion: int):
    pass


@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear):
    #Buscar la factura
    factura_encontrada = None
    for factura in lista_facturas:
        if factura.id == factura_id:
            factura_encontrada = factura
    #Mensaje si no existe la factura
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La factura con id {factura_id}, no existe."
        )

    #Validar datos de la transaccion
    transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
    transaccion_val.factura_id = factura_id
    factura_encontrada.transacciones.append(transaccion_val)
    #Id de la transaccion
    transaccion_val.id = len(lista_transacciones)+1
    #Agregar a la lista las transacciones
    lista_transacciones.append(transaccion_val)
    return transaccion_val


@rutas_transacciones.patch("/transacciones/{id_transaccion}", response_model=Transaccion)
async def editar_transaccion(id_transaccion: int, datos_transaccion: Transaccion):
    pass


@rutas_transacciones.delete("/transacciones/{id_transaccion}", response_model=Transaccion)
async def eliminar_transaccion(id_transaccion: int):
    pass
