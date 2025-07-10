from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String(100), nullable=False)
    vendedor = Column(String(100), nullable=False)
    total = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    detalles = relationship("VentaDetalle", back_populates="venta", cascade="all, delete-orphan")
