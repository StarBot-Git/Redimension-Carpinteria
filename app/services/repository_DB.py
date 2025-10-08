import sys
import time
import pandas as pd
from sqlalchemy import create_engine, text
from PySide6.QtWidgets import QMessageBox, QApplication, QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QEventLoop, QTimer
from PySide6.QtGui import QIcon

# ====== Librerias propias ======

from app.config import settings

# === Motores de conexión (mantenemos tu cadena, sin .env por ahora) ===
DB_URL = (
    "mssql+pyodbc://AutomationAllStar:Allstar2025_*@databaseazuresqlserverallstar.database.windows.net:1433/CarpinteriaDB"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
)
MASTER_URL = (
    "mssql+pyodbc://AutomationAllStar:Allstar2025_*@databaseazuresqlserverallstar.database.windows.net:1433/master"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
)

class RepositoryDB:
    def __init__(self):
        # ======== Crear | Engines de conexion y variable conexion ========

        self.engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
        self.engine_master = create_engine(MASTER_URL, pool_pre_ping=True, future=True)
        self.cn = None

        # ======== Esperar a que la DB este 'ONLINE' ========
        try:
            self._wait_until_online_with_dialog(timeout_sec=180, poll_sec=2)
        except Exception as e:
            pass

        # ======== Realiza la conexion con base de datos ========
        try:
            self.cn = self.engine.connect()
        except Exception as e:
            self.mostrar_error("Error al conectar con la base de datos.", f"No fue posible abrir la conexión inicial.\nDetalle: {e}")
            raise RuntimeError("No se pudo conectar con la base de datos") from e


    # -------- Consultas a la Base de datos --------
    
    """
        fetch_activate_projects():
            Consulta los proyectos aun activos en la base de datos
    """
    def fetch_activate_projects(self):
        try:
            self._ensure_connection()

            df = pd.read_sql(text("SELECT * FROM dbo.proyectos WHERE estado <> 'Entregado';"), self.cn)
            return df['nombre_proyecto'].dropna().tolist()
        except Exception as e:
            self.mostrar_error(
                "Error al conectar con la base de datos.",
                "Verifica tu conexión a internet o contacta al administrador."
            )
            raise RuntimeError("No se pudo conectar con la base de datos") from e

    """
        fetch_model_types():
            Consulta los tipo de modelos/productos que ofrece All Star para sus proyectos.
    """
    def fetch_model_types(self):
        try:
            self._ensure_connection()

            df = pd.read_sql(text("SELECT DISTINCT tipo_producto FROM dbo.productos ORDER BY tipo_producto;"), self.cn)
            return df['tipo_producto'].dropna().tolist()
        except Exception as e:
            self.mostrar_error(
                "Error al conectar con la base de datos.",
                "Verifica tu conexión a internet o contacta al administrador."
            )
            raise RuntimeError("No se pudo conectar con la base de datos") from e

    """
        fetch_models_by_type():
            Consulta los modelos disponibles para un 'Tipo de modelo' seleccionado.

            - model_type: Variable que contiene el 'Tipo de modelo' que se quiere consultar.
    """
    def fetch_models_by_type(self, model_type: str):
        try:
            self._ensure_connection()
            df = pd.read_sql(text("SELECT DISTINCT nombre_producto FROM dbo.productos WHERE tipo_producto = :tp ORDER BY nombre_producto;"),self.cn,params={"tp": model_type})
            
            return df['nombre_producto'].dropna().tolist()
        except Exception as e:
            self.mostrar_error("Error al conectar con la base de datos.", "Verifica tu conexión a internet o contacta al administrador.")

            raise RuntimeError("No se pudo conectar con la base de datos") from e

    """
        fetch_materials():
            Consulta los materiales disponibles para la empresa.
    """
    def fetch_materials(self):
        try:
            self._ensure_connection()
            df = pd.read_sql(text("SELECT DISTINCT color FROM dbo.tableros;"), self.cn)

            return df['color'].dropna().tolist()
        except Exception as e:
            self.mostrar_error("Error al conectar con la base de datos.", "Verifica tu conexión a internet o contacta al administrador.")

            raise RuntimeError("No se pudo conectar con la base de datos") from e

    """
        fetch_edges()
        Consulta los materiales de los tipos de cantos brindados por la empresa
    """
    def fetch_edges(self):
        # Mantengo tu placeholder
        pass

    # -------- utilidades --------

    """
        _ensure_connection():
            Funcion encargada de verificar que la conexion con la DB sea estable
    """
    def _ensure_connection(self):
        """Asegura que self.cn esté usable (reabre si se cayó)."""
        if self.cn is None:
            self.cn = self.engine.connect()
            return
        try:
            # ping barato
            self.cn.exec_driver_sql("SELECT 1;")
        except Exception:
            try:
                self.cn.close()
            except Exception:
                pass
            self.cn = self.engine.connect()

    """
        _get_db_state():
            Lee state_desc desde master.sys.databases para 'CarpinteriaDB'.
            Retorna por ejemplo: 'ONLINE', 'OFFLINE', 'RECOVERING'...
            Retorna None si no se pudo consultar.
    """
    def _get_db_state(self) -> str | None:
        try:
            with self.engine_master.connect() as cm:
                state = cm.execute(text("SELECT state_desc FROM sys.databases WHERE name = :db;"),{"db": "CarpinteriaDB"}).scalar()

            return state
        except Exception:

            return None

    """
        _wait_until_online_with_dialog():
            Muestra un QDialog modal con QProgressBar indeterminado y espera hasta que la base esté ONLINE o se cumpla el timeout.

            - timeout_sec: es el tiempo de espera
            - poll_sec:

    """
    def _wait_until_online_with_dialog(self, timeout_sec=120, poll_sec=2):
        # ======== Instancia de la app ========

        app = QApplication.instance() or QApplication(sys.argv)

        # ======== Creacion y configuracion | Ventana 'dialogo' ========

        dlg = QDialog()
        dlg.setWindowTitle("Conectando")

        try:
            dlg.setWindowIcon(QIcon(settings.LOGO_DIR))
        except Exception:
            pass

        dlg.setModal(True)
        dlg.resize(360, 120)

        # ======== Layout principal ========
        layout = QVBoxLayout(dlg)

        # ======== Etiqueta principal ========
        lbl = QLabel("Esperando base de datos...")
        lbl.setAlignment(Qt.AlignLeft)

        # ======== Barra de carga ========
        bar = QProgressBar()
        bar.setRange(0, 0) # indeterminado

        layout.addWidget(lbl)
        layout.addWidget(bar)

        # --- Loop local para bloquear solo este diálogo sin congelar la UI ---
        loop = QEventLoop(dlg)

        start_ts = time.time()
        unknown_streak = 0

        # ======== FSM | Estados de la conexion ========
        def tick():
            nonlocal unknown_streak
            state = self._get_db_state()
            if state:
                unknown_streak = 0
                lbl.setText(f"Esperando base de datos... (estado: {state})")
            else:
                unknown_streak += 1
                lbl.setText("Esperando base de datos... (verificando estado)")

            # ¿ya está online?
            if (state or "").upper() == "ONLINE":
                timer.stop()
                loop.quit()
                return

            # ¿sin permisos/estado repetidamente?
            if unknown_streak >= 3:
                timer.stop()
                loop.quit()
                return

            # ¿timeout?
            if time.time() - start_ts >= timeout_sec:
                timer.stop()
                loop.quit()
                return

        # ======== Funcion 'Timer' ========
        timer = QTimer(dlg)
        timer.timeout.connect(tick)
        timer.start(int(poll_sec * 1000))

        dlg.show()
        loop.exec()

        dlg.accept()

    """
        mostrat_error():
            Funcion encarga de mostrar mensaje de error en la conexion a la base de datos.

            - mensaje: Contiene el mensaje principal de error
            - detalle: Contiene el detalle del mensaje producido
    """
    def mostrar_error(self, mensaje:str|None = None, detalle:str|None = None):
        # ======== Instancia de la app ========
        app = QApplication.instance() or QApplication(sys.argv)

        # ======== Ventana 'Mensaje de error' ========
        msg = QMessageBox()

        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(mensaje)

        if detalle:
            msg.setInformativeText(detalle)
        
        msg.exec()   # Bloquea hasta que el usuario cierre

    """
        close():
            Funcion encargada de cerrar todos los elementos relacionados con la base de datos.
    """
    def close(self):
        try:
            if self.cn is not None:
                self.cn.close()
                self.cn = None
        except Exception:
            pass

        try:
            self.engine.dispose()
        except Exception:
            pass

        try:
            self.engine_master.dispose()
        except Exception:
            pass
