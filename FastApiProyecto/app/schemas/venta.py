from pydantic import BaseModel
from typing import List
from datetime import datetime

class VentaItem(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class VentaCreate(BaseModel):
    cliente: str
    vendedor: str
    productos: List[VentaItem]

class VentaDetalleOut(VentaItem):
    id: int
    producto_nombre: str
    subtotal: float

class VentaOut(BaseModel):
    id: int
    cliente: str
    vendedor: str
    total: float
    fecha: datetime
    detalles: List[VentaDetalleOut]

    class Config:
        from_attributes = True
