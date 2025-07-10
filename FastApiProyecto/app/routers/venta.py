from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.schemas.venta import VentaCreate, VentaOut, VentaDetalleOut
from app.crud import venta as crud

router = APIRouter(prefix="/ventas", tags=["Ventas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=201)
def crear_venta(data: VentaCreate, db: Session = Depends(get_db)):
    try:
        crud.create(db, data)
        return {
            "success": True,
            "message": "Venta creada correctamente"
        }
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(e)
            }
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error interno al crear la venta"
            }
        )
    


@router.get("/", response_model=list[VentaOut])
def listar_ventas(db: Session = Depends(get_db)):
    ventas = crud.get_all(db)
    return [
        VentaOut(
            id=v.id,
            cliente=v.cliente,
            vendedor=v.vendedor,
            total=v.total,
            fecha=v.fecha,
            comentario = v.comentario,
            detalles=[
                VentaDetalleOut(
                    id=d.id,
                    producto_id=d.producto_id,
                    cantidad=d.cantidad,
                    precio_unitario=d.precio_unitario,
                    subtotal=d.subtotal,
                    producto_nombre=d.producto.nombre
                ) for d in v.detalles
            ]
        ) for v in ventas
    ]

@router.get("/{venta_id}", response_model=VentaOut)
def obtener_venta(venta_id: int, db: Session = Depends(get_db)):
    v = crud.get_by_id(db, venta_id)
    if not v:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    return VentaOut(
        id=v.id,
        cliente=v.cliente,
        vendedor=v.vendedor,
        total=v.total,
        fecha=v.fecha,
        comentario = v.comentario,
        detalles=[
            VentaDetalleOut(
                id=d.id,
                producto_id=d.producto_id,
                cantidad=d.cantidad,
                precio_unitario=d.precio_unitario,
                subtotal=d.subtotal,
                producto_nombre=d.producto.nombre
            ) for d in v.detalles
        ]
    )
