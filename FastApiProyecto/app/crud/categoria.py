from sqlalchemy.orm import Session # Importamos la clase Session de SQLAlchemy para manejar la sesión de la base de datos
from app.models.categoria import Categoria  # archivo renombrado
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


def get_all(db: Session):  #Metodo para obtener todas las categorías de la base de datos
    return db.query(Categoria).all() #devolvemos todas las categorías

def get_by_id(db: Session, categoria_id: int): #Metodo para obtener una categoría por su ID
    return db.query(Categoria).filter(Categoria.id == categoria_id).first() #devolvemos la categoría con el ID especificado filtando por el ID

def create(db: Session, categoria: CategoriaCreate): #Metodo para crear una nueva categoría
    nueva = Categoria(**categoria.dict()) #creamos una nueva categoría usando el modelo Categoria y los datos del esquema CategoriaCreate
    db.add(nueva)
    db.commit() #ejecutamos la transacción para guardar los cambios en la base de datos
    db.refresh(nueva) #actualizamos la instancia de la categoría con los datos de la base de datos
    return nueva #devolvemos la nueva categoría creada

def update(db: Session, categoria_id: int, datos: CategoriaUpdate):
    categoria = get_by_id(db, categoria_id)
    if categoria:
        for key, value in datos.dict().items(): # Iteramos sobre los datos del esquema CategoriaUpdate
            setattr(categoria, key, value) # Asignamos el valor al atributo correspondiente de la categoría
        db.commit()
        db.refresh(categoria)
    return categoria

def delete(db: Session, categoria_id: int):
    categoria = get_by_id(db, categoria_id) # Obtenemos la categoría por su ID
    if categoria:
        db.delete(categoria)
        db.commit()
    return categoria
