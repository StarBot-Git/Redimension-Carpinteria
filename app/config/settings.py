from dataclasses import dataclass
from pathlib import Path

# ======== IDENTIDAD VENTANA =========

APP_NAME = "Star Lift"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# ======== TEMA ==========

THEME = "light"  # Opciones: "light", "dark"

# ======== RUTAS =========

ROOT_DIR = Path(__file__).parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"

LOGO_DIR = str(ASSETS_DIR / "icons" / "all_star_logo.svg")

ONEDRIVE_CARPENTRY_DIR = str(Path.home() / "OneDrive" / "Carpintería")
ONEDRIVE_MODELS_DIR = str(Path.home() / "OneDrive" / "Carpintería" / "Modelos Produccion")
ONEDRIVE_PROJECTS_DIR = str(Path.home() / "OneDrive" / "Carpintería" / "Proyectos")

# Futuras opciones centralizadas:
# DB_URL = "sqlite:///carpentry.db"
# LOG_LEVEL = "INFO"