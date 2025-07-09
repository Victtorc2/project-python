from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routers import categoria 

from app.routers import producto

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Categorías", version="1.0.0")

# Incluir rutas
app.include_router(categoria.router)
app.include_router(producto.router)



