from PySide6.QtCore import QObject
from app.services.repository_DB import RepositoryDB
import os

class SelectionPanelController(QObject):

    _EDGES = [
        "ABS 0.45 mm", 
        "PVC 1.0 mm", 
        "PVC 2.0 mm"
    ]

    def __init__(self, window, repository: RepositoryDB):
        super().__init__(window)
        self.win = window           # MainWindow
        self.repo = repository      # RepositoryDB
        self.sp = window.sidebar    # SelectionPanel

        # === Inicializacion | Conexion | Tipo de modelo ===
        self.sp._model_Type.currentTextChanged.connect(self.on_model_type_changed)

        # === Inicializacion | Conexion | Modelos ===
        self.sp._model.currentTextChanged.connect(self.update_model_selection)

    def Start_SP(self):

        # === Carga inicial | Tipo de modelos ===
        types = self.repo.fetch_model_types()
        self._load_comboBox(self.sp._model_Type, ["Select type"] + types)

        # === Carga inicial | modelos ===
        self._load_comboBox(self.sp._model, ["Select model"]) # Vacio

        # === Carga inicial | Materiales ===
        materials = self.repo.fetch_materials()
        self._load_comboBox(self.sp._material, ["Select material"] + materials)

        # === Carga inicial | Cantos ===
        self._load_comboBox(self.sp._edge, ["Select edge"] + self._EDGES)
        
    # ---------- Dinámicos ----------
    """
        on_model_type_changed:

        Cuando el usuario cambia el tipo de modelo, actualizar la lista de modelos disponibles.
    """

    def on_model_type_changed(self, text: str):

        # === Inicializacion ===
        if not text or text.startswith("Select"):

            self._load_comboBox(self.sp._model, ["Select model"])
        else: # === Carga de modelos ===

            models = self.repo.fetch_models_by_type(text) # Carga de modelos
            #models = ["Model A", "Model B", "Model C"] # Simulación de carga de modelos
            self._load_comboBox(self.sp._model, ["Select model"] + models)
        
        # === Actualziacion de breadcrumbs | TopBar ===

        self.update_model_selection()

    """
        update_model_selection:

        Actualiza todos los elementos dependientes de la selección del modelo:
            - Breadcrumbs en la TopBar
            - Título en MetricsEditorView
            - Habilita/Deshabilita botones en MetricsEditorView
            - Carga el modelo en MetricsEditorView
    """

    def update_model_selection(self):

        # === Texto inicial ===
        parts = ["Products"]

        # === Verificacion | Tipo de modelo y modelo ===
        t = self._clean_piece(self.sp._model_Type.currentText())
        m = self._clean_piece(self.sp._model.currentText())

        # === Anexacion de partes ===
        if t:
            parts.append(t)
        if m:
            parts.append(m)
        
        # === Actualizacion de breadcrumbs | TopBar ===
        self.win.topbar.set_breadcrumbs(parts)

        # === Actualizacion de titulo | MetricsEditorView ===
        self._Update_MetricsView_Title()

        # === Desbloqueo de botones | MetricsEditorView ===
        self.win.metrics_view.btn_Model.setEnabled(bool(m))
        #self.win.metrics_view.btn_Drawings.setEnabled(bool(m))
        self.win.metrics_view.btn_Import.setEnabled(bool(m))
        self.win.metrics_view.btn_Load.setEnabled(bool(m))
        self.win.metrics_view.btn_Save.setEnabled(bool(m))

        # === Busqueda y carga del modelo | MetricsEditorView ===

        if m:
            if self.sp._model.currentText() == "COMODA 3 CAJONES":
                model_Path = f"C:\\Users\\autom\\Desktop\\CARPINTERIA\\Inventor - Modelos - Prueba\\{self.sp._model.currentText()}" # Ruta base de modelos
            else:
                model_Path = f"C:\\Users\\autom\\OneDrive\\Carpintería\\Modelos Produccion\\{self.sp._model_Type.currentText()}\\{self.sp._model.currentText()}" # Ruta base de modelos

            if os.path.exists(model_Path):
                rows = self.win.metrics_view.load_inventor_model(model_Path) # Cargar modelo en MetricsEditorView

                self.win.metrics_view.set_rows(rows) 
            else:
                print(f"❌ La ruta {model_Path} no existe")


    """
        _load_comboBox:

        Carga los elementos en un QComboBox dado.
    """

    # ---------- Utilidades ----------

    def _load_comboBox(self, combo, items):
        combo.blockSignals(True)
        combo.clear()
        combo.addItems(items)
        combo.blockSignals(False)

    """
        _clean_piece:

        Limpia el texto de una pieza del breadcrumb.
    """
    @staticmethod
    def _clean_piece(text: str) -> str:
        if not text:
            return ""
        
        return "" if text.lower().startswith(("select","tipo","modelo","material")) else text

    """
        _Update_MetricsView_Title:

        Actualiza el título del MetricsEditorView con el nombre del modelo seleccionado.
    """

    def _Update_MetricsView_Title(self):
        model_name = self._clean_piece(self.sp._model.currentText())
        self.win.metrics_view.set_model_name(model_name)