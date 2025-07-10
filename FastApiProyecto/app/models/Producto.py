from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship ##el orm
from app.database.connection import Base

class Producto(Base): ##heredan
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    precio = Column(Float, nullable=False)
    unidad_medida = Column(String(50), nullable=False)
    stock = Column(Integer, nullable=False)
    imagen = Column(String(500), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    categoria = relationship("Categoria", backref="productos")