import pyodbc, pandas as pd
from sqlalchemy import create_engine

# Cadena de conexión a la base de datos SQL Server
engine = create_engine(
    "mssql+pyodbc://AutomationAllStar:Allstar2025_*@databaseazuresqlserverallstar.database.windows.net:1433/CarpinteriaDB"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
)

class RepositoryDB:
    def __init__(self):
        # Inicialización de la conexión a la base de datos
        pass

    def fetch_model_types(self):
        with engine.connect() as cn:
            df = pd.read_sql("SELECT DISTINCT tipo_producto FROM dbo.productos ORDER BY tipo_producto;", cn)

        return df['tipo_producto'].tolist()

    def fetch_models_by_type(self, model_type: str):
        with engine.connect() as cn:
            df = pd.read_sql(f"SELECT DISTINCT nombre_producto FROM dbo.productos WHERE tipo_producto = '{model_type}' ORDER BY nombre_producto;", cn)
        
        return df['nombre_producto'].tolist()
    
# repo = RepositoryDB()
# print(repo.fetch_model_types())
# print(repo.fetch_models_by_type("Mueble de bar"))