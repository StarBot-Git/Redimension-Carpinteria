from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableView, QSizePolicy, QHeaderView
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import win32com.client
import os
import pandas as pd
from pathlib import Path

class MetricsEditorView(QFrame):
    # ======== Headers | Tabla metrica ========
    HEADERS = ["Parametro", "Valor", "Unidad"]

    # ======== Parametros de salida | Despiece ========
    PARAMETROS_SALIDA = ["Ancho", "Alto", "Espesor"]

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("MetricsCard")

        # ======== Elemento raiz ========

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # ======== Contenedor superior ========

        root_sup = QHBoxLayout()
        root_sup.setContentsMargins(16, 16, 16, 16)

        # - Titulo de modelo -
        self.title = QLabel("Editor de metricas")
        self.title.setObjectName("MetricsCardTitle")
        
        # - Boton | Modo metricas o propiedades -
        self.btn_Table = QPushButton("Metricas")
        
        root_sup.addWidget(self.title)
        root_sup.addStretch(1)
        root_sup.addWidget(self.btn_Table)

        root.addLayout(root_sup)

        # ======== Contenedor | buscador ========

        search_row = QHBoxLayout()
        search_row.setSpacing(8)

        # ======== Barra buscadora de metricas ========

        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar metrica...")
        self.search.setObjectName("SearchField")
        search_row.addWidget(self.search)

        root.addLayout(search_row)

        # ======== Botones | Funcionalidades varias ========

        actions = QHBoxLayout()
        self.btn_Model   = QPushButton(" Ver Modelo")
        self.btn_Model.clicked.connect(self.on_view_model)
        self.set_Button_Style(self.btn_Model, icon_path="assets/icons/eye.svg")

        self.btn_Drawings = QPushButton(" Planos")
        self.btn_Drawings.clicked.connect(self.on_view_drawings)
        self.set_Button_Style(self.btn_Drawings, icon_path="assets/icons/blueprint.svg")

        self.btn_Import= QPushButton(" Despiece CSV")
        self.btn_Import.clicked.connect(self.on_import_csv)
        self.set_Button_Style(self.btn_Import, icon_path="assets/icons/download.svg")

        self.btn_Load = QPushButton(" Cargar cambios")
        self.btn_Load.clicked.connect(self.on_load_changes)
        self.set_Button_Style(self.btn_Load, icon_path="assets/icons/upload.svg")

        self.btn_Save= QPushButton(" Guardar Cambios")
        self.btn_Save.clicked.connect(self.on_save_changes)
        self.set_Button_Style(self.btn_Save, icon_path="assets/icons/save.svg")

        actions.addWidget(self.btn_Model)
        actions.addWidget(self.btn_Drawings)
        actions.addWidget(self.btn_Import)
        actions.addStretch(1)
        actions.addWidget(self.btn_Load)
        actions.addWidget(self.btn_Save)

        root.addLayout(actions)

        # ======== Tabla de metricas ========

        self.view = QTableView(self)
        self.view.setObjectName("MetricsTable")
        self.view.setAlternatingRowColors(True) # Alternar colores de filas
        self.view.setSelectionBehavior(QTableView.SelectRows) # Seleccionar filas completas
        self.view.setSortingEnabled(False) # Deshabilitar permisos de ordenamiento
        root.addWidget(self.view, 1)

        # - Modelo | Tabla metrica -

        self.model = QStandardItemModel(0, len(self.HEADERS), self) # 0 filas, n columnas
        self.model.setHorizontalHeaderLabels(self.HEADERS) # Encabezados de columnas
        self.view.setModel(self.model)

        # Oculta header vertical y quita boton de esquina
        self.view.verticalHeader().setVisible(False)
        self.view.setCornerButtonEnabled(False)

        # La vista debe poder expandirse
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view.setMouseTracking(True)

        # Aplicar estilo base
        self._apply_header_bounds()
    
    
    """
        set_model_name():

        Actualiza el título del MetricsEditorView con el nombre del modelo seleccionado.
    """
    def set_model_name(self, model_name: str):
        if model_name:
            self.title.setText(f"Editor de metricas - {model_name}")
        else:
            self.title.setText("Editor de metricas")

    # ---------- Buttons ----------

    def set_Button_Style(self, button: QPushButton, icon_path: str = ""):

        # === Estilo base | Button ===
        button.setObjectName("Button_Style")
        button.setEnabled(False)
        button.setMinimumHeight(32)
        button.setCursor(Qt.PointingHandCursor)

        if icon_path:
            button.setIcon(QIcon(icon_path)) 
            button.setIconSize(QSize(16, 16))  

    def on_view_model(self):

        # === Verificacion | assembler document ===
        folder = Path(self.model_path)
        iam_files = list(folder.glob("*.iam"))

        if iam_files:
            asm_path = str(iam_files[0])  # primer .iam que encuentre
            print(f"✅ Ensamble encontrado: {asm_path}")
        else:
            asm_path = None
            print("❌ No se encontró ningún archivo .iam")
        
        if os.path.exists(asm_path):
            self.asmDoc = self.inventor.Documents.Open(asm_path)
            print("✅ Ensamble CUERPO abierto")
        else:

            print("❌ No se encontró el archivo de ensamble")
            return
        print("3")
        # === Mostrar Inventor ===
        self.inventor.Visible = True

    def on_view_drawings(self):
        print("Ver planos")

    def on_import_csv(self):
        data = [] # Tabla de salida

        # === Verificar | Ensamble abierto ===
        folder = Path(self.model_path)
        iam_files = list(folder.glob("*.iam"))

        if iam_files:
            asm_path = str(iam_files[0])  # primer .iam que encuentre
            print(f"✅ Ensamble encontrado: {asm_path}")
        else:
            asm_path = None
            print("❌ No se encontró ningún archivo .iam")

        if os.path.exists(asm_path):

            self.asmDoc = self.inventor.Documents.Open(asm_path)
            print("✅ Ensamble abierto para importar")
        else:

            print("❌ No se encontró el archivo de ensamble")
            return
        
        # === Extraccion de parametros por pieza ===
        for occ in self.asmDoc.ComponentDefinition.Occurrences:
            partDoc = occ.Definition.Document
            nombre = partDoc.DisplayName

            print(f"📦 Componente: {nombre}")

            fila = {"Componente": nombre}

            try:
                params = partDoc.ComponentDefinition.Parameters

                for clave in self.PARAMETROS_SALIDA:

                    try:
                        fila[clave] = params.Item(clave).Value*10  # Convertir cm a mm
                    except:
                        fila[clave] = None  # Si no existe, se deja vacio
            except:
                # Si no hay parámetros, se deja todo en None
                for clave in self.PARAMETROS_SALIDA:
                    fila[clave] = None
            
            data.append(fila)

        # === Conversion | Dataframe
        df = pd.DataFrame(data)
        output_csv = Path.home() / "Desktop" / "despiece.csv"
        print(output_csv)

        # === Reforzar de columnas vacias ===
        for clave in ["Componente"] + self.PARAMETROS_SALIDA:
            if clave not in df.columns:
                df[clave] = None

        df = df[["Componente"] + self.PARAMETROS_SALIDA]

        # === Exportar | Despiece ===
        df.to_excel(str(output_csv).replace(".csv", ".xlsx"), index=False)

        print(f"Archivo generado en: {output_csv}")

    def on_save_changes(self):
        if hasattr(self, "asmDoc") and self.asmDoc is not None:
            self.inventor.SilentOperation = True  
            self.asmDoc.Save()

            for ref in self.asmDoc.ReferencedDocuments:
                try:
                    if ref.Dirty:
                        ref.Save()
                except Exception as e:
                    print(f"No se pudo guardar {ref.FullFileName}: {e}")
            print("💾 Cambios guardados en ensamble y dependencias")

            self.inventor.SilentOperation = False

    def on_load_changes(self):
        # Asegurarnos que el ensamble está abierto
        folder = Path(self.model_path)
        iam_files = list(folder.glob("*.iam"))

        if iam_files:
            asm_path = str(iam_files[0])  # primer .iam que encuentre
            print(f"✅ Ensamble encontrado: {asm_path}")
        else:
            asm_path = None
            print("❌ No se encontró ningún archivo .iam")

        if not hasattr(self, "asmDoc") or self.asmDoc is None:
            if os.path.exists(asm_path):
                self.asmDoc = self.inventor.Documents.Open(asm_path)
                print("✅ Ensamble abierto para guardar")
            else:
                print("❌ No se encontró el archivo de ensamble")
                return

        if self.skeleton_doc:
            params = self.skeleton_doc.ComponentDefinition.Parameters
            parametros = self.get_param_dict()

            for nombre, valor in parametros.items():
                try:
                    params.Item(nombre).Value = valor/10  # Convertir mm a cm
                    print(f"✅ Parámetro '{nombre}' actualizado a {valor}")
                except Exception as e:
                    print(f"❌ Error en '{nombre}': {e}")

            # Propagar cambios
            self.skeleton_doc.Update()
            self.asmDoc.Update()

    # ---------- Table Data Handling ----------

    def _parse_number(self, v):
        """Convierte el valor de la celda a float si se puede (soporta '1,23')."""
        if isinstance(v, (int, float)):
            return float(v)  # Convertir cm a mm
        s = str(v).strip()
        if not s:
            return None
        try:
            return float(s.replace(",", "."))  # 1,23 -> 1.23
        except ValueError:
            return None  # o devuelve s si prefieres preservar cadenas

    def get_rows(self) -> list[dict]:
        """Devuelve todas las filas como lista de dicts con las llaves que usamos en la UI."""
        rows = []
        for r in range(self.model.rowCount()):
            rows.append({
                "Parametro": self.model.item(r, 0).text().strip() if self.model.item(r, 0) else "",
                "Valor":     self.model.item(r, 1).text().strip() if self.model.item(r, 1) else "",
                "Unidad":    self.model.item(r, 2).text().strip() if self.model.item(r, 2) else "",
            })
        return rows

    def get_param_dict(self) -> dict[str, float | None]:
        """
        Devuelve { PARAMETRO: VALOR } para usarlo igual que tu 'parametros' del Excel.
        Si un valor no es numérico o está vacío, deja None (ajústalo si prefieres otra cosa).
        """
        d = {}
        for r in range(self.model.rowCount()):
            name_item = self.model.item(r, 0)
            val_item  = self.model.item(r, 1)
            if not name_item:
                continue
            name = name_item.text().strip()
            val  = self._parse_number(val_item.text() if val_item else "")
            if name:
                d[name] = val
        return d
    
    # ---------- Table Setup ----------

    def _apply_header_bounds(self):
        h = self.view.horizontalHeader()
        h.setStretchLastSection(False)
        h.setMinimumSectionSize(60)
        h.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # alineación del texto del header

        h.setSectionResizeMode(0, QHeaderView.Stretch)           # Parametro ocupa espacio libre
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Valor al contenido

        col_width = h.sectionSize(1)
        h.resizeSection(1, col_width + 100)

        h.setSectionResizeMode(2, QHeaderView.Fixed)             # Unidad fijo
        self.view.setColumnWidth(2, 72)

    def set_rows(self, rows: list[dict]):
        """
        rows: [{"Parametro": str, "Valor": any, "Unidad": str}, ...]
        """
        self.model.removeRows(0, self.model.rowCount())
        
        for r in rows:
            self._append_row(
                f" {r.get("Parametro","")}",
                f"  {r.get("Valor","")}   ",
                f" {r.get("Unidad","mm")}",
            )
        
        self.view.resizeColumnsToContents()

        self._apply_header_bounds() 

    # ---------- Inventor Model Integration ----------

    def load_inventor_model(self, model_path: str, loading_Bar):
        print(f"Cargando modelo de Inventor desde: {model_path}")

            # === Conexion con Inventor ===

        loading_Bar.set_Text("Cargando modelo de Inventor...")
        loading_Bar.set_Progress(4)

        self.inventor = win32com.client.Dispatch("Inventor.Application")
        self.inventor.Visible = False  # No mostrar la ventana de Inventor inicialmente

        loading_Bar.set_Text("Abriendo Skeleton...")
        loading_Bar.set_Progress(5)

        # === Apertura Skeleton Part ===
        self.model_path = model_path
        skeleton_path = f"{model_path}\\Skeleton Part.ipt"

        if os.path.exists(skeleton_path):
            print(f"✅ Skeleteon abierto")
            self.skeleton_doc = self.inventor.Documents.Open(skeleton_path)
        else:
            print(f"❌ No se encontró el archivo Skeleton del modelo")
            return
        
        loading_Bar.set_Text("Extrayendo parametro...")
        loading_Bar.set_Progress(6)

        params = self.skeleton_doc.ComponentDefinition.Parameters       

        print("Parámetros del modelo:")
        for param in params:
            print(f"- {param.Name}: {param.Value} {param.Units}")


        rows = []
        for p in params:
            nombre = getattr(p, "Name", None) or getattr(p, "name", "")
            valor  = getattr(p, "Value", None) or getattr(p, "value", "")
            unidad = getattr(p, "Units", None) or getattr(p, "units", "")

            if any(other.Name in p.Expression  and other.Name != param.Name for other in params):
                print(f"Parametro '{nombre}' depende de otro, se ignora.")
                continue

            if isinstance(valor, (int, float)):
                valor = valor * 10

            rows.append({
                "Parametro": str(nombre),
                "Valor": valor,
                "Unidad": unidad,
            })
        return rows

    def _append_row(self, param, value, unit):
        items = [
            QStandardItem(str(param)),        # read-only
            QStandardItem(str(value)),        # editable
            QStandardItem(str(unit)),         # read-only
        ]
        # Marcar Min/Max como no editables
        for idx in (0, 2):
            items[idx].setEditable(False)
        self.model.appendRow(items)