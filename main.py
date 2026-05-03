import os
from Main.MainWindow import MainWindow, load_stylesheet
from PySide6.QtWidgets import QApplication

ROOT = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    app = QApplication([])
    stylesheet = load_stylesheet(os.path.join(ROOT, "Style", "stylelight.qss"))
    app.setStyleSheet(stylesheet)
    window = MainWindow(db_path=os.path.join(ROOT, "data_film.db"))
    window.show()
    app.exec()