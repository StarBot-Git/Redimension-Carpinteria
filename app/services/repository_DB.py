import pyodbc, pandas as pd
from sqlalchemy import create_engine
from PySide6.QtWidgets import QMessageBox, QApplication
import sys

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
        try:
            with engine.connect() as cn:
                df = pd.read_sql("SELECT DISTINCT tipo_producto FROM dbo.productos ORDER BY tipo_producto;", cn)

            return df['tipo_producto'].tolist()
        except:
            self.mostrar_error("Error al conectar con la base de datos.", "Verifica tu conexión a internet o contacta al administrador.") 

            raise RuntimeError("No se pudo conectar con la base de datos")

    def fetch_models_by_type(self, model_type: str):
        try:
            with engine.connect() as cn:
                df = pd.read_sql(f"SELECT DISTINCT nombre_producto FROM dbo.productos WHERE tipo_producto = '{model_type}' ORDER BY nombre_producto;", cn)
            
            return df['nombre_producto'].tolist()
        except:
            self.mostrar_error("Error al conectar con la base de datos.", "Verifica tu conexión a internet o contacta al administrador.") 

            raise RuntimeError("No se pudo conectar con la base de datos")
        
    def fetch_materials(self):
        try:
            with engine.connect() as cn:
                df = pd.read_sql(f"SELECT DISTINCT color FROM dbo.tableros;", cn)
            
            return df['color'].tolist()
        except:
            self.mostrar_error("Error al conectar con la base de datos.", "Verifica tu conexión a internet o contacta al administrador.") 

            raise RuntimeError("No se pudo conectar con la base de datos")
        
    def fetch_edges(self):
        # try:
        #     with engine.connect() as cn:
        #         df = pd.read_sql(f"SELECT DISTINCT nombre_producto FROM dbo.productos WHERE tipo_producto = '{model_type}' ORDER BY nombre_producto;", cn)
        #         pass
            
        #     return df['nombre_producto'].tolist()
        # except:
        #     self.mostrar_error("Error al conectar con la base de datos.", "Verifica tu conexión a internet o contacta al administrador.") 

        #     raise RuntimeError("No se pudo conectar con la base de datos")
        pass
    
    def mostrar_error(self, mensaje, detalle=None):
        app = QApplication.instance() or QApplication(sys.argv)  # Reusar app si existe
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(mensaje)
        if detalle:
            msg.setInformativeText(detalle)
        msg.exec()   # Bloquea hasta que el usuario cierre
    
