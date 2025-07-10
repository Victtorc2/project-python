from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VentaDetalleItem(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class VentaCreate(BaseModel):
    cliente: str
    vendedor: str
    comentario: Optional[str] = None
    productos: List[VentaDetalleItem]

class VentaDetalleOut(VentaDetalleItem):
    id: int
    producto_nombre: str
    subtotal: float

class VentaOut(BaseModel):
    id: int
    cliente: str
    vendedor: str
    total: float
    fecha: datetime
    comentario: Optional[str] = None
    detalles: List[VentaDetalleOut]

    class Config:
        from_attributes = True
