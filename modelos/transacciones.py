from pydantic import BaseModel


#Crear el modelo Transaccion(id, cantidad, vr_unitario, id_factura)
class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    id_factura: int


class TransaccionCrear(TransaccionBase):
    pass


class Transaccion(TransaccionBase):
    id: int | None = None