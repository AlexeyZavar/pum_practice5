import sys

from PySide6.QtWidgets import QApplication

from src import MathWindow

app = QApplication()
math_window = MathWindow(app)

math_window.show()

sys.exit(app.exec())
