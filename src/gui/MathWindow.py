from PySide6.QtGui import Qt, QPaintEvent, QPainter
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QVBoxLayout, QWidget

from .TitleBarWidget import TitleBarWidget
from .consts import *

BORDER_RADIUS = 12


class MathWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedHeight(702)
        self.setFixedWidth(1050)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(24)
        shadow_effect.setOffset(0)
        shadow_effect.setColor(hex2QColor('EDEDED').darker())

        self.setGraphicsEffect(shadow_effect)

        layout = QVBoxLayout()
        layout.setContentsMargins(BORDER_RADIUS, BORDER_RADIUS, BORDER_RADIUS, BORDER_RADIUS)

        layout.addWidget(TitleBarWidget(), 0, Qt.AlignTop)

        self.setStyleSheet('''
        * {
            color: #424F6B;
        } 
        ''')

        self.setLayout(layout)

    def paintEvent(self, event: QPaintEvent) -> None:
        size = self.size()

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)

        qp.setPen(QColor(0, 0, 0, 0))
        qp.setBrush(QColor(0, 0, 0, 0))
        qp.drawRect(0, 0, size.width(), size.height())

        qp.setPen(BACKGROUND)
        qp.setBrush(BACKGROUND)
        qp.drawRoundedRect(BORDER_RADIUS, BORDER_RADIUS, size.width() - 2 * BORDER_RADIUS,
                           size.height() - 2 * BORDER_RADIUS, BORDER_RADIUS, BORDER_RADIUS)

        qp.end()
