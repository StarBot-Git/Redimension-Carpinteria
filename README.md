# Carpentry Configurator

Plantilla mínima para arrancar una aplicación de escritorio usando PySide6.

## Configuración rápida

`ash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python main.py
`

## Estructura

`
carpentry_configurator/
├── main.py
├── app/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_window.py
│   ├── widgets/
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── validators.py
│   │   └── utils.py
│   └── controllers/
│       └── __init__.py
├── assets/
│   ├── icons/
│   │   └── .gitkeep
│   └── styles/
│       └── main.qss
├── tests/
│   └── __init__.py
├── requirements.txt
└── README.md
`

Los módulos de widgets y controllers quedan listos para que agregues tus propias implementaciones. Solo se incluye main_window.py con una ventana básica para verificar que la aplicación inicia correctamente.
