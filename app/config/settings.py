from dataclasses import dataclass
from pathlib import Path

# ======== IDENTIDAD VENTANA =========

APP_NAME = "Diseñador de Produccion"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 640

# ======== TEMA ==========

THEME = "light"  # Opciones: "light", "dark"

# ======== RUTAS =========

ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"

# Futuras opciones centralizadas:
# DB_URL = "sqlite:///carpentry.db"
# LOG_LEVEL = "INFO"