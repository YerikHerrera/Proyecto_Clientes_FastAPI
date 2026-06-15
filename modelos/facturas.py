from pydantic import BaseModel
from clientes import Cliente


#Crear el modelo transacciones(id, fecha, vr_total, cliente)
class FacturaBase(BaseModel):
    fecha: str
    vr_total: float
    cliente: Cliente


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase)
    id: int | None = None