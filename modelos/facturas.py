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
        #Consultar el id actual de factura
        factura_id_actual = getattr(self, "id", None)
        total_factura = 0.0
        if not factura_id_actual or not self.transacciones:
            return total_factura
        #Recorrer la lista de transacciones, según el facutra id
        for transaccion in self.transacciones:
            if transaccion.factura_id == factura_id_actual:
                total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura
        


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase)
    id: int | None = None