from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Reemplaza estos datos según tu configuración
DATABASE_URL = "mysql+pymysql://root:123456@localhost/tiendadb"

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Sesión para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()
