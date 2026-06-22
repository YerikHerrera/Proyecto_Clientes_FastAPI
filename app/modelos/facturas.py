from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship
from .clientes import Cliente
from .transacciones import Transaccion
from datetime import datetime






#Crear el modelo transacciones(id, fecha, vr_total, cliente)
class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now())
    #cliente: Cliente
    #transacciones: list[Transaccion] = []
    
    @computed_field
    @property
    def vr_total(self) -> float:
        #Calcular (cantidad * vr_unitario)
        #Consultar el id actual de factura
        #factura_id_actual = getattr(self, "id", None)
        #total_factura = 0.0
        #if not factura_id_actual or not self.transacciones:
        #    return total_factura
        #Recorrer la lista de transacciones, según el facutra id
        #for transaccion in self.transacciones:
        #    if transaccion.factura_id == factura_id_actual:
        #        total_factura += transaccion.vr_unitario * transaccion.cantidad

        return 0.0
        

class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table = True):
    id: int | None = Field(default=None, primary_key = True)
    cliente_id: int = Field(default=None, foreign_key = "cliente.id")
    