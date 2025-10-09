import os
from PySide6.QtCore import QObject, Qt
from pathlib import Path
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

# ====== Librerias propias ======

from app.services.repository_DB import RepositoryDB
from app.config import settings

class SelectionPanelController(QObject):
    _EDGES = ["ABS 0.45 mm", "PVC 1.0 mm", "PVC 2.0 mm"]

    """
        class SelectionPanelController():
            Controlador logico de eventos en el panel de seleccion de elementos
    """
    def __init__(self, window, repository: RepositoryDB):
        super().__init__(window)

        # ====== Variables heredadas ======

        self.win = window           # MainWindow()
        self.repo = repository      # RepositoryDB
        self.sp = window.sidebar    # SelectionPanel

        # === Conexion logica | Proyectos ===
        self.sp._project.currentTextChanged.connect(self.update_project_selection)

        # === Conexion logica | Tipo de modelo ===
        self.sp._model_Type.currentTextChanged.connect(self.on_model_type_changed)

        # === Conexion logica | Modelos ===
        self.sp._model.currentTextChanged.connect(self.update_model_selection)

        # === Conexion logica | Materiales ===
        self.sp._material.currentTextChanged.connect(self.update_material_selection)

        # === Conexion logica | Material de canto ===
        self.sp._edge.currentTextChanged.connect(self.update_edge_selection)


    """
        Start_SP():
            Funcion que inicializa los comboBox en el seleccionPanel
    """
    def Start_SP(self):
        # === Carga inicial | Proyectos ===
        projects = self.repo.fetch_activate_projects()
        self._load_comboBox(self.sp._project, ["select project"] + projects)

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

        # ===== Inicialmente | ComboBox desactivados =====
        self.sp._model_Type.setEnabled(False)
        self.set_valid_comboBox(self.sp._model_Type, "disabled")
        self.sp._model.setEnabled(False)
        self.set_valid_comboBox(self.sp._model, "disabled")
        self.sp._material.setEnabled(False)
        self.set_valid_comboBox(self.sp._material, "disabled")
        self.sp._edge.setEnabled(False)
        self.set_valid_comboBox(self.sp._edge, "disabled")
    
    # ---------- Metodos dinámicos ----------

    """
        update_project_selection():
            Funcion encargada de activar y crear o retomar el estado actual de un proyecto
    """
    def update_project_selection(self):
        current_option = self._clean_piece(self.sp._project.currentText())

        if current_option:
            self.set_valid_comboBox(self.sp._project, "valid")
            self.win.topbar._title.setText(current_option)

            self.proceed_CurrentProject(current_option)
            self.win.metrics_view.NOMBRE_PROYECTO = current_option

            self.sp._model_Type.setEnabled(True)
            self.set_valid_comboBox(self.sp._model_Type, "void")
            self.sp._model.setEnabled(True)
            self.set_valid_comboBox(self.sp._model, "void")

            self.win.topbar.button_quote.setEnabled(True)
            self.win.topbar.button_CutSaw.setEnabled(True)
            self.win.topbar.button_Information.setEnabled(True)

            self.win.topbar.TP_Controller.project = current_option
        else:
            self.set_valid_comboBox(self.sp._project, "void")
            self.win.topbar._title.setText(settings.APP_NAME)

            self.sp._model_Type.setEnabled(False)
            self.set_valid_comboBox(self.sp._model_Type, "disabled")
            self.sp._model.setEnabled(False)
            self.set_valid_comboBox(self.sp._model, "disabled")
            self.sp._material.setEnabled(False)
            self.set_valid_comboBox(self.sp._material, "disabled")
            self.sp._edge.setEnabled(False)
            self.set_valid_comboBox(self.sp._edge, "disabled")

            self.win.topbar.button_quote.setEnabled(False)
            self.win.topbar.button_CutSaw.setEnabled(False)
            self.win.topbar.button_Information.setEnabled(False)

    """
        on_model_type_changed():
            Cuando el usuario cambia el tipo de modelo, actualizar la lista de modelos disponibles.
    """
    def on_model_type_changed(self, text: str):

        # === Seleccion de ningun modelo especifico ===
        if not text or text.startswith("Select"):

            self._load_comboBox(self.sp._model, ["Select model"])
            self.set_valid_comboBox(self.sp._model_Type, "void")
        else: # === Carga un tipo de modelo especifico ===

            models = self.repo.fetch_models_by_type(text) # Carga de modelos de ese tipo

            self._load_comboBox(self.sp._model, ["Select model"] + models)
            self.set_valid_comboBox(self.sp._model_Type, "valid")
        
        # === Actualizacion de datos de la UI | TopBar ===
        self.update_model_selection()

    """
        update_model_selection():

        Actualiza todos los elementos dependientes de la selección del modelo:
            - Breadcrumbs en el TopBar.
            - Título en MetricsEditorView.
            - Habilita/Deshabilita botones en MetricsEditorView.
            - Carga el modelo en MetricsEditorView.
    """
    def update_model_selection(self):
        n_Steps = 9 # Cantidad de pasos | Barra de progreso

        # === Texto inicial ===
        parts = ["Products"]

        # === Verificacion | 'Tipo de modelo' y 'Modelo' ===
        t = self._clean_piece(self.sp._model_Type.currentText())
        m = self._clean_piece(self.sp._model.currentText())

        # === Anexacion | Tipo de modelo seleccionado ===
        if t:
            parts.append(t)
        
        # === Verificacion de modelo seleccionado ===
        if m:
            # ---- Inicio | Barra de progreso ----
            self.win.sidebar.loading.set_Text("Actualizando interfaz...")
            self.win.sidebar.loading.set_Progress(0)
            self.win.sidebar.loading.n_Steps = n_Steps
            self.win.sidebar.loading.setVisible(True)

            # ---- Anexacion | Modelo seleccionado ----
            parts.append(m)

            # ---- Actualizacion de breadcrumbs | TopBar ----
            self.win.topbar.set_breadcrumbs(parts)
            self.win.sidebar.loading.set_Progress(1)

            # ---- Actualizacion de titulo | MetricsEditorView ----
            self._Update_MetricsView_Title()
            self.win.sidebar.loading.set_Progress(2)

            #_________________________________________________________
            # BORRAR ESTA COMPROBACION
            if self.sp._model.currentText() == "COMODA 3 CAJONES":
                model_Path = f"C:\\Users\\autom\\Desktop\\CARPINTERIA\\Inventor - Modelos - Prueba\\{self.sp._model.currentText()}" # Ruta base de modelos
            else:
                model_Path = f"{settings.ONEDRIVE_MODELS_DIR}\\{self.sp._model_Type.currentText()}\\{self.sp._model.currentText()}" # Ruta base de modelos
            #_________________________________________________________

            self.win.sidebar.loading.set_Text("Busqueda del modelo en OneDrive...")
            self.win.sidebar.loading.set_Progress(3)

            # ---- Busqueda | Modelo seleccionado en OneDrive ----
            if os.path.exists(model_Path):
                self.set_valid_comboBox(self.sp._model, "valid")

                # === Busqueda y carga del modelo | MetricsEditorView ===
                self.win.metrics_view.load_inventor_model(model_Path, self.win.sidebar.loading) # Cargar modelo en MetricsEditorView
                self.win.metrics_view.set_TableData(True) # Iniciar tabla | Modo: Metricas

                self.win.sidebar.loading.set_Progress(8)

                # === Desbloqueo de botones | MetricsEditorView ===
                self.win.metrics_view.btn_Model.setEnabled(bool(m))
                #self.win.metrics_view.btn_Drawings.setEnabled(bool(m))
                self.win.metrics_view.btn_Import.setEnabled(bool(m))
                self.win.metrics_view.btn_Load.setEnabled(bool(m))
                self.win.metrics_view.btn_Save.setEnabled(bool(m))
                self.win.metrics_view.btn_Table.setEnabled(bool(m))

                # === Fin de la barra de progreso ===
                self.win.sidebar.loading.set_Progress(9)
                self.win.sidebar.loading.stop()
                self.win.sidebar.loading.setVisible(False)

                self.sp._material.setEnabled(True)
                self.set_valid_comboBox(self.sp._material, "void")
                self.sp._edge.setEnabled(True)
                self.set_valid_comboBox(self.sp._edge, "void")

                return
            else:
                print(f"❌ La ruta '{model_Path}' no existe")
                self.set_valid_comboBox(self.sp._model, "problem")

                self.win.metrics_view.rows_metrics = []
                self.win.metrics_view.rows_props = []
            
        else:
            self.set_valid_comboBox(self.sp._model, "void")

            self.win.metrics_view.rows_metrics = []
            self.win.metrics_view.rows_props = []

        # === OPCION NO VALIDA | Vacie la tabla y desactive botones ===
        self.win.metrics_view.btn_Model.setEnabled(False)
        self.win.metrics_view.btn_Drawings.setEnabled(False)
        self.win.metrics_view.btn_Import.setEnabled(False)
        self.win.metrics_view.btn_Load.setEnabled(False)
        self.win.metrics_view.btn_Save.setEnabled(False)
        self.win.metrics_view.btn_Table.setEnabled(False)

        self.win.metrics_view.set_TableData(True)

        self.win.sidebar.loading.stop()
        self.win.sidebar.loading.setVisible(False)
    
    """
    """
    def update_material_selection(self):
        current_option = self._clean_piece(self.sp._material.currentText())

        # Solo aplica si estamos en vista Propiedades
        if current_option and (bool(self.win.metrics_view.btn_Table.property("State")) == False):
            piezas = []
            model = self.win.metrics_view.model

            finish = self.pick_finish(self.win)   # <-- aquí pedimos ST/RH/MDP/MDF
            if not finish:
                self.sp._material.setCurrentIndex(0)
                return  # usuario canceló

            # === Obtener piezas seleccionadas ===
            for r in range(model.rowCount()):
                idx_chk = model.index(r, 0)  # col "Ed"
                if model.data(idx_chk, Qt.CheckStateRole) == Qt.Checked:
                    idx_name = model.index(r, 1)  # col "Pieza"
                    piezas.append(model.data(idx_name, Qt.DisplayRole))

            print(f"🔹 Piezas seleccionadas: {piezas}")

            # === Actualizar 'Material' en rows_props ===
            rows_props = self.win.metrics_view.rows_props

            for fila in rows_props:
                if fila.get("Pieza") in piezas:
                    fila["Material"] = current_option
                    fila["Texturizado"] = finish
                    print(f"✅ {fila['Pieza']} → nuevo material: {current_option} | texturizado: {finish}")

            # === Refrescar tabla para reflejar cambios ===
            self.win.metrics_view.set_TableData(False)
            self.sp._material.setCurrentIndex(0)
        else:
            self.sp._material.setCurrentIndex(0)
    
    """
    """
    def update_edge_selection(self):
        current_option = self._clean_piece(self.sp._edge.currentText())

        # Solo aplica si estamos en vista Propiedades
        if current_option and (bool(self.win.metrics_view.btn_Table.property("State")) == False):
            piezas = []
            model = self.win.metrics_view.model

            # === Obtener piezas seleccionadas ===
            for r in range(model.rowCount()):
                idx_chk = model.index(r, 0)  # col "Ed"
                if model.data(idx_chk, Qt.CheckStateRole) == Qt.Checked:
                    idx_name = model.index(r, 1)  # col "Pieza"
                    piezas.append(model.data(idx_name, Qt.DisplayRole))

            print(f"🔹 Piezas seleccionadas: {piezas}")

            # === Actualizar 'Material' en rows_props ===
            rows_props = self.win.metrics_view.rows_props

            for fila in rows_props:
                if fila.get("Pieza") in piezas:
                    fila["Material Canto"] = current_option
                    print(f"✅ {fila['Pieza']} → nuevo material: {current_option}")

            # === Refrescar tabla para reflejar cambios ===
            self.win.metrics_view.set_TableData(False)
            self.sp._edge.setCurrentIndex(0)
        else:
            self.sp._edge.setCurrentIndex(0)
    
    # ---------- Utilidades ----------

    """
    """
    def pick_finish(self, parent=None) -> str | None:
        dlg = QDialog(parent)
        dlg.setWindowTitle("Selecciona texturizado")
        lay = QVBoxLayout(dlg)
        lay.setSpacing(12)
        lay.addWidget(QLabel("Confirma el texturizado del material:"), alignment=Qt.AlignLeft)

        row = QHBoxLayout()
        lay.addLayout(row)

        chosen = {"val": None}
        def choose(v):
            chosen["val"] = v
            dlg.accept()

        for v in ("ST", "RH", "MDP", "MDF"):
            b = QPushButton(v)
            b.clicked.connect(lambda _, x=v: choose(x))
            row.addWidget(b)

        # Botón Cancelar (opcional)
        cancel = QPushButton("Cancelar")
        cancel.clicked.connect(dlg.reject)
        lay.addWidget(cancel, alignment=Qt.AlignRight)

        return chosen["val"] if dlg.exec() == QDialog.Accepted else None

    """
        proceed_CurrentProject():
            Funcion que revisa si la carpeta del proyecto ya existe(si no la crea).
    """
    def proceed_CurrentProject(self, project_name:str = None):
        self.win.projects_folder_dir = f"{settings.ONEDRIVE_PROJECTS_DIR}\\{project_name}"

        self.win.breakdowns_folder_dir = f"{self.win.projects_folder_dir}\\Despieces"
        self.win.blueprints_folder_dir = f"{self.win.projects_folder_dir}\\Planos"
        
        print(self.win.projects_folder_dir)

        if Path(self.win.projects_folder_dir).exists():
            # Retome la carpeta
            print("No es necesario")
            pass
        else:
            print("Creando!!!!")
            # === Creacion de la carpeta del proyecto ===
            Path(self.win.projects_folder_dir).mkdir(parents=False, exist_ok=True)

            # === Creacion subcarpetas | Cotizacion y Produccion ===

            Path(self.win.breakdowns_folder_dir).mkdir(parents=False, exist_ok=True)
            Path(self.win.blueprints_folder_dir).mkdir(parents=False, exist_ok=True)

    """
        _load_comboBox():

        Carga los elementos en un QComboBox especificado.
    """
    def _load_comboBox(self, combo, items):
        combo.blockSignals(True)
        combo.clear()
        combo.addItems(items)
        combo.blockSignals(False)

    """
        _clean_piece():

        Limpia el texto de una pieza del breadcrumb.
    """
    @staticmethod
    def _clean_piece(text: str) -> str:
        if not text:
            return ""
        
        return "" if text.lower().startswith(("select","tipo","modelo","material")) else text

    """
        _Update_MetricsView_Title():

        Actualiza el título del MetricsEditorView con el nombre del modelo seleccionado.
    """
    def _Update_MetricsView_Title(self):
        model_name = self._clean_piece(self.sp._model.currentText())
        self.win.metrics_view.set_model_name(model_name)

    """
        set_valid_comboBox():

        Actualiza el color de un combox segun su estado:
            - valid | Verde: Es una eleccion valida o verificada.
            - problem | Naranja: Hubo un error al consultar el elemento.
            - void | azul: Estado 'base' de los comboBox
    """
    @staticmethod
    def set_valid_comboBox(cb, state: str):
        cb.setProperty("valid", state)
        cb.style().unpolish(cb)
        cb.style().polish(cb)
        cb.update()