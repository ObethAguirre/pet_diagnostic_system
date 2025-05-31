import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class MenuView(QWidget):
    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel

        layout = QVBoxLayout()

        # Encabezado con logo + texto
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
        pixmap = QPixmap(logo_path)

        # Ajustamos el logo al tamaño máximo disponible
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)
        logo_label.setMinimumSize(200, 230)  

        text_label = QLabel("Menú Principal")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        header_layout.addWidget(logo_label, stretch=1)
        header_layout.addWidget(text_label, stretch=3)
        layout.addLayout(header_layout)

        # Botones del menú
        self.register_pet_btn = QPushButton("Registrar Mascota")
        self.diagnosis_btn = QPushButton("Diagnóstico de Mascota")
        self.history_btn = QPushButton("Historial de Diagnósticos")
        self.settings_btn = QPushButton("Configuración")
        self.logout_btn = QPushButton("Cerrar Sesión")

        layout.addWidget(self.register_pet_btn)
        layout.addWidget(self.diagnosis_btn)
        layout.addWidget(self.history_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.logout_btn)

        self.setLayout(layout)

        # Conectar botones
        self.register_pet_btn.clicked.connect(lambda: self.viewmodel.navigate_to(2))
        self.diagnosis_btn.clicked.connect(lambda: self.viewmodel.navigate_to(3))
        self.history_btn.clicked.connect(lambda: self.viewmodel.navigate_to(4))
        self.settings_btn.clicked.connect(lambda: self.viewmodel.navigate_to(5))
        self.logout_btn.clicked.connect(self.viewmodel.logout)
