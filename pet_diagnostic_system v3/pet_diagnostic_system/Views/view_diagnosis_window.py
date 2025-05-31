from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
)
from PyQt6.QtGui import QFont

class ViewDiagnosisWindow(QWidget):
    def __init__(self, filename, content):
        super().__init__()
        self.setWindowTitle(f"Diagnóstico - {filename}")

        layout = QVBoxLayout()

        # Título
        title_label = QLabel(f"Archivo: {filename}")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title_label)

        # Contenido del archivo
        self.content_text = QTextEdit()
        self.content_text.setPlainText(content)
        self.content_text.setReadOnly(True)
        self.content_text.setFont(QFont("Courier New", 10))
        self.content_text.setStyleSheet("""
            background-color: #f9f9f9;
            color: #000000;
            padding: 10px;
        """)
        layout.addWidget(self.content_text)

        # Botón cerrar
        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)
        self.resize(500, 400)
