from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- IMPORTANTE

from app.database.connection import Base, engine
from app.routers import categoria, producto, venta

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Categorías", version="1.0.0")

# === CONFIGURACIÓN DE CORS ===
origins = [
    "http://localhost:3000",     # React local (create-react-app)
    "http://localhost:5173",     # React con Vite
    "https://tu-frontend.railway.app",  # <-- Reemplaza por tu dominio real en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Puedes poner ["*"] solo para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(categoria.router)
app.include_router(producto.router)
app.include_router(venta.router)
