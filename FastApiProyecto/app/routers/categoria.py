from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaOut
from app.crud import categoria as crud
from app.database.connection import SessionLocal

router = APIRouter(prefix="/categorias", tags=["Categorías"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[CategoriaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_all(db)

@router.get("/{categoria_id}", response_model=CategoriaOut)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.get_by_id(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.post("/", status_code=201)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    try:
        crud.create(db, categoria)
        return {
            "success": True,
            "message": "Categoría creada correctamente"
        }
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Error al crear la categoría"
            }
        )

@router.put("/{categoria_id}")
def actualizar_categoria(categoria_id: int, categoria: CategoriaUpdate, db: Session = Depends(get_db)):
    try:
        actualizada = crud.update(db, categoria_id, categoria)
        if not actualizada:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "Categoría no encontrada"
                }
            )
        return {
            "success": True,
            "message": "Categoría actualizada correctamente"
        }
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Error al actualizar la categoría"
            }
        )


@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    try:
        eliminada = crud.delete(db, categoria_id)
        if not eliminada:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "Categoría no encontrada"
                }
            )
        return {
            "success": True,
            "message": "Categoría eliminada correctamente"
        }

    except IntegrityError:
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": "No se puede eliminar la categoría porque está asociada a uno o más productos"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error inesperado al eliminar la categoría"
            }
        )