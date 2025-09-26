# Redimensionador de Inventor

Herramienta de escritorio construida con PySide6 para actualizar modelos parametricos de Inventor sin rehacer los planos originales. La aplicacion toma los datos existentes de una tabla, permite modificarlos mediante un formulario y luego sincroniza los valores con un modelo base para redimensionarlo y generar el despiece necesario.

## Proposito del proyecto
- Centralizar la informacion de medidas y materiales por modelo.
- Agilizar la configuracion de un modelo existente para nuevas necesidades de los arquitectos.
- Generar automaticamente el despiece actualizado una vez que se cambian los parametros.

## Estado actual
- Ventana principal con barra superior (titulo y breadcrumbs).
- Panel lateral de seleccion con campos placeholder para el flujo de configuracion.
- Hoja de estilos inicial para mantener coherencia visual.

## Requisitos
- Python 3.10 o superior.
- Dependencias listadas en equirements.txt (por ahora solo PySide6).

## Puesta en marcha rapida
`
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python main.py
`

## Estructura del proyecto
- main.py: punto de entrada y carga de estilos.
- pp/config/settings.py: constantes de aplicacion (nombres, tamanos, rutas base).
- pp/ui/main_window.py: contenedor principal, integra TopBar y panel lateral.
- pp/ui/panels/top_bar.py: barra superior con titulo y breadcrumbs.
- pp/ui/panels/selection_panel.py: formulario lateral placeholder para seleccionar modelos y opciones.
- ssets/styles/main.qss: estilos globales de la interfaz.

## Siguientes pasos sugeridos
- Conectar el panel de seleccion con los datos reales de la tabla de Inventor.
- Disenar el formulario para modificar dimensiones y materiales por componente.
- Integrar la logica que aplica los cambios al modelo parametrico y genera el despiece.
- Agregar pruebas automaticas para la logica de negocio y los validadores futuros.
