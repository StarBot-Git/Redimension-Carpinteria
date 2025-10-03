from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar

class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.n_Steps = None

        # ==== Contenedor base ====

        layout = QVBoxLayout(self)

        # ==== Titulo de la barra de carga ====

        self.title = QLabel("Cargando...")
        self.title.setObjectName("ProgressBarTitle")
        layout.addWidget(self.title)
        
        # ==== Barra de progreso ====

        self.progress_Bar = QProgressBar()
        self.progress_Bar.setMinimum(0)
        self.progress_Bar.setMaximum(0) # Modo indeterminado
        self.progress_Bar.setTextVisible(False)

        layout.addWidget(self.progress_Bar)

        self.setLayout(layout)

    def set_Text(self, text:str):
        self.title.setText(text)

    def set_Progress(self, value:int):
        if self.n_Steps is not None:
            self.progress_Bar.setMaximum(self.n_Steps)
        self.progress_Bar.setValue(value)

    def start_Indeterminate(self, text="cargando..."):
        self.set_Text(text)
        self.progress_Bar.setMaximum(0)

    def stop(self):
        self.n_Steps = None
        self.progress_Bar.reset()

