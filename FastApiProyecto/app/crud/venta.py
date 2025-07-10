from sqlalchemy.orm import Session, joinedload
from app.models.Venta import Venta
from app.models.VentaDetalle import VentaDetalle
from app.models.Producto import Producto
from app.schemas.venta import VentaCreate

def create(db: Session, data: VentaCreate):
    total = 0.0
    detalles = []

    for item in data.productos:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not producto:
            raise ValueError(f"Producto ID {item.producto_id} no encontrado")

        if producto.stock < item.cantidad:
            raise ValueError(f"Stock insuficiente para el producto '{producto.nombre}' (disponible: {producto.stock}, requerido: {item.cantidad})")

        # Descontar stock
        producto.stock -= item.cantidad

        subtotal = item.cantidad * item.precio_unitario
        detalle = VentaDetalle(
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            subtotal=subtotal
        )
        total += subtotal
        detalles.append(detalle)

    nueva_venta = Venta(
        cliente=data.cliente,
        vendedor=data.vendedor,
        total=total,
        detalles=detalles,
        comentario = data.comentario
    )

    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta

def get_all(db: Session):
    return db.query(Venta).options(joinedload(Venta.detalles).joinedload(VentaDetalle.producto)).all()

def get_by_id(db: Session, venta_id: int):
    return db.query(Venta).options(joinedload(Venta.detalles).joinedload(VentaDetalle.producto)).filter(Venta.id == venta_id).first()
