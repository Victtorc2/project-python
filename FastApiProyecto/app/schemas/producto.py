from pydantic import BaseModel ##es como una clase json, parsea automatico, es un modelo
from typing import Optional

class ProductoBase(BaseModel): ##entran json aca, con este payload
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    unidad_medida: str
    stock: int
    categoria_id: int  # Referencia a la tabla Categoria
    imagen : Optional[str] = None  # URL de la imagen del producto

class ProductoCreate(ProductoBase): ##heredan
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    precio: Optional[float]
    unidad_medida: Optional[str]
    stock: Optional[int]
    categoria_id: Optional[int]
    imagen : Optional[str] = None 

class ProductoOut(ProductoBase): ##devolvemos un orm de producto
    id: int
    categoria_nombre: str

    class Config:
        from_attributes = True ##aceptar objetos tipo orm, un objeto tipo pydantic, no un diccionario