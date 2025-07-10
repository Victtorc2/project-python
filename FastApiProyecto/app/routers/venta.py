from fastapi import APIRouter, Depends, HTTPException
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

@router.post("/", response_model=VentaOut)
def crear_venta(data: VentaCreate, db: Session = Depends(get_db)):
    try:
        venta = crud.create(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return VentaOut(
        id=venta.id,
        cliente=venta.cliente,
        vendedor=venta.vendedor,
        total=venta.total,
        fecha=venta.fecha,
        detalles=[
            VentaDetalleOut(
                id=detalle.id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
                subtotal=detalle.subtotal,
                producto_nombre=detalle.producto.nombre
            ) for detalle in venta.detalles
        ]
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
