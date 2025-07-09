from sqlalchemy.orm import Session, joinedload
from app.models.Producto import Producto 
from app.schemas.producto import ProductoCreate, ProductoUpdate

def get_all(db: Session):
    return db.query(Producto).options(joinedload(Producto.categoria)).all() ##carga con el joined, con  categoria incluida

def get_by_id(db: Session, producto_id: int):
    return (
        db.query(Producto)
        .options(joinedload(Producto.categoria)).filter(Producto.id == producto_id).first()
    )

def create(db: Session, producto_data: ProductoCreate): ##un createmodel si los campos coinciden se crearan con normalidad
    nuevo = Producto(**producto_data.dict()) ##a diccionario
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update(db: Session, producto_id: int, producto_data: ProductoUpdate):
    producto = get_by_id(db, producto_id)
    if producto:
        for key, value in producto_data.dict(exclude_unset=True).items(): ##solo si hay campos q se enviaron
            setattr(producto, key, value) ##setea los atributos
        db.commit()
        db.refresh(producto)
    return producto


def delete(db: Session, producto_id: int):
    producto = get_by_id(db, producto_id)
    if producto:
        db.delete(producto)
        db.commit()
    return producto