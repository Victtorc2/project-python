from fastapi import FastAPI
from database import SessionLocal

app = FastAPI(title="Sistema de Caja", version="1.0.0")

@app.get("/conexion")
def test_conexion():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")  # Consulta simple para probar conexión
        return {"mensaje": "Conexión exitosa a la base de datos"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()




