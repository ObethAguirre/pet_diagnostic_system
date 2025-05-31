import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedLayout,
    QPushButton, QVBoxLayout, QLabel, QSplashScreen
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from ViewModels.diagnosis_viewmodel import DiagnosisViewModel
from Views.diagnosis_view import DiagnosisView
from Views.history_view import DiagnosisHistoryView
from Views.login_view import LoginView
from Views.pet_registration_view import PetRegistrationView
from Views.settings_view import SettingsView

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Diagnóstico de Mascotas")
        self.setGeometry(100, 100, 800, 600)
        self.theme = "light"

        self.viewmodel = DiagnosisViewModel(main_app=self)
        self.login_view = LoginView(main_app=self)
        self.diagnosis_view = DiagnosisView(viewmodel=self.viewmodel, main_app=self)
        self.history_view = DiagnosisHistoryView(viewmodel=self.viewmodel, main_app=self)
        self.registration_view = PetRegistrationView(viewmodel=self.viewmodel, main_app=self)
        self.settings_view = SettingsView(main_app=self)

        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)

        self.menu_layout = QVBoxLayout()
        self.menu_label = QLabel("Menú Principal")

        self.diagnosis_button = QPushButton("Diagnóstico")
        self.diagnosis_button.clicked.connect(lambda: self.navigate_to(2))
        self.history_button = QPushButton("Historial de Diagnósticos")
        self.history_button.clicked.connect(lambda: self.navigate_to(3))
        self.registration_button = QPushButton("Registrar Mascota")
        self.registration_button.clicked.connect(lambda: self.navigate_to(4))
        self.settings_button = QPushButton("Configuración")
        self.settings_button.clicked.connect(lambda: self.navigate_to(5))
        self.logout_button = QPushButton("Cerrar Sesión")
        self.logout_button.clicked.connect(lambda: self.navigate_to(0))
        self.exit_button = QPushButton("Salir")
        self.exit_button.clicked.connect(self.close)

        self.menu_layout.addWidget(self.menu_label)
        self.menu_layout.addWidget(self.diagnosis_button)
        self.menu_layout.addWidget(self.history_button)
        self.menu_layout.addWidget(self.registration_button)
        self.menu_layout.addWidget(self.settings_button)
        self.menu_layout.addWidget(self.logout_button)
        self.menu_layout.addWidget(self.exit_button)

        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.menu_layout)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.login_view)            # index 0
        self.stacked_layout.addWidget(self.menu_widget)           # index 1
        self.stacked_layout.addWidget(self.diagnosis_view)        # index 2
        self.stacked_layout.addWidget(self.history_view)          # index 3
        self.stacked_layout.addWidget(self.registration_view)     # index 4
        self.stacked_layout.addWidget(self.settings_view)         # index 5

        self.layout.addLayout(self.stacked_layout)
        self.setCentralWidget(self.main_widget)

        self.apply_theme(self.theme)
        self.navigate_to(0)

    def navigate_to(self, index):
        self.stacked_layout.setCurrentIndex(index)

    def refresh_history(self):
        self.history_view.refresh_history()

    def apply_theme(self, theme):
        self.theme = theme
        from PyQt6.QtCore import QFile, QTextStream
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        qss_path = os.path.join(base_path, 'styles.qss')
        qss_file = QFile(qss_path)
        try:
            if qss_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(qss_file)
                stylesheet = stream.readAll()
                qss_file.close()
                self.main_widget.setProperty("theme", self.theme)
                for widget in [
                    self.login_view,
                    self.menu_widget,
                    self.diagnosis_view,
                    self.history_view,
                    self.registration_view,
                    self.settings_view
                ]:
                    widget.setProperty("theme", self.theme)
                    widget.style().polish(widget)
                    for child in widget.findChildren(QWidget):
                        child.setProperty("theme", self.theme)
                        child.style().polish(child)
                self.setStyleSheet(stylesheet)
            else:
                print(f"⚠️ Error al abrir styles.qss en la ruta: {qss_path}.")
        except Exception as e:
            print(f"⚠️ Error al aplicar tema: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Configurar ruta al logo
    base_path = os.path.abspath(os.path.dirname(__file__))
    logo_path = os.path.join(base_path, "assets", "logo.png")

    if os.path.exists(logo_path):
        splash_pix = QPixmap(logo_path)
        splash_pix = splash_pix.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
        splash.setFixedSize(800, 600)
        splash.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        splash.show()
    else:
        print(f"⚠️ Logo no encontrado en: {logo_path}")
        splash = None

    # Esperar 2 segundos antes de mostrar la app
    def start_main_app():
        if splash:
            splash.close()
        window = MainApp()
        window.show()

    QTimer.singleShot(2000, start_main_app)
    sys.exit(app.exec())
