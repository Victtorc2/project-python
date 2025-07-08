from sqlalchemy.orm import Session
from app.models.categoria import Categoria  # archivo renombrado
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


def get_all(db: Session):
    return db.query(Categoria).all()

def get_by_id(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()

def create(db: Session, categoria: CategoriaCreate):
    nueva = Categoria(**categoria.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def update(db: Session, categoria_id: int, datos: CategoriaUpdate):
    categoria = get_by_id(db, categoria_id)
    if categoria:
        for key, value in datos.dict().items():
            setattr(categoria, key, value)
        db.commit()
        db.refresh(categoria)
    return categoria

def delete(db: Session, categoria_id: int):
    categoria = get_by_id(db, categoria_id)
    if categoria:
        db.delete(categoria)
        db.commit()
    return categoria
