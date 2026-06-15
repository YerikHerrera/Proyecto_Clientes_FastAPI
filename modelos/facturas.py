from pydantic import BaseModel
from 
from .clientes import Cliente
from datetime import datetime

#Crear el modelo transacciones(id, fecha, vr_total, cliente)
class FacturaBase(BaseModel):
    fecha: str = datetime.now()
    vr_total: float
    cliente: Cliente
    transacciones: list[Transaccion] = []
    
    @computed_field
    @property
    def vr_total(self) -> float:
        #Calcular (cantidad * vr_unitario)
        return 222
        


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase)
    id: int | None = None