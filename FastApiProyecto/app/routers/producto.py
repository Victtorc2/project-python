from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.producto import ProductoCreate, ProductoOut, ProductoUpdate
from app.crud import producto as crud
from app.database.connection import SessionLocal

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los productos
@router.get("/lista", response_model=list[ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    productos = crud.get_all(db)
    return [
        ProductoOut(
            id=p.id,
            nombre=p.nombre,
            descripcion=p.descripcion,
            precio=p.precio,
            unidad_medida=p.unidad_medida,
            stock=p.stock,
            categoria_id=p.categoria_id,
            categoria_nombre=p.categoria.nombre,
            imagen=p.imagen if p.imagen else None  # Manejo de imagen opcional
        )
        for p in productos
    ]

# Obtener producto por ID
@router.get("/{producto_id}", response_model=ProductoOut)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)): ##pasale el
    producto = crud.get_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return ProductoOut(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        unidad_medida=producto.unidad_medida,
        stock=producto.stock,
        categoria_id=producto.categoria_id,
        categoria_nombre=producto.categoria.nombre,
        imagen=producto.imagen if producto.imagen else None  # Manejo de imagen opcional
    )

@router.post("/")
def crear_producto(producto_data: ProductoCreate, db: Session = Depends(get_db)):
    crud.create(db, producto_data)
    return {
        "success": True,
        "message": "Producto creado correctamente"
    }

@router.put("/{producto_id}")
def actualizar_producto(producto_id: int, producto_data: ProductoUpdate, db: Session = Depends(get_db)):
    actualizado = crud.update(db, producto_id, producto_data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {
        "success": True,
        "message": "Producto actualizado correctamente"
    }

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete(db, producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {
        "success": True,
        "message": "Producto eliminado correctamente"
    }