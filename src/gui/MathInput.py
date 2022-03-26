import PySide6
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFont, QKeyEvent
from PySide6.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QLabel

from src import Lexer, LexerException
from src.evaluator.consts import OPERATORS, SYMBOL_DEGREE, SYMBOL_MINUS, SYMBOL_BRACKET_OPEN


class MathInput(QWidget):
    def __init__(self):
        super().__init__()

        self.lexer = Lexer()

        layout = QVBoxLayout()

        self.line_edit = QLineEdit()
        self.line_edit.installEventFilter(self)

        font = QFont('JetBrains Mono', 18)

        self.line_edit.setFont(font)
        self.line_edit.setFixedHeight(48)
        self.line_edit.setMinimumWidth(800)
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setStyleSheet('''
        border-radius: 24px;
        ''')

        layout.addWidget(self.line_edit)

        self.error_label = QLabel()
        self.error_label.setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
        if event.type() == QEvent.KeyPress and watched == self.line_edit and isinstance(event, QKeyEvent):
            key = event.key()
            text = self.line_edit.text()

            if key == 40:
                pos = self.line_edit.cursorPosition()

                text = text[:pos] + '()' + text[pos:]
                self.line_edit.setText(text)
                self.line_edit.setCursorPosition(pos + 1)
            elif key == 16777219 and not (
                    self.line_edit.hasSelectedText() and self.line_edit.selectedText() == self.line_edit.text()):  # backspace
                pos = self.line_edit.cursorPosition()

                if pos != len(text) and text[pos - 1] == '(' and text[pos] == ')':
                    text = text[:pos - 1] + text[pos + 1:]
                    self.line_edit.setText(text)
                    self.line_edit.setCursorPosition(pos - 1)

                    pos -= 1
                else:
                    self.line_edit.keyPressEvent(event)
                    text = self.line_edit.text()
                    pos = self.line_edit.cursorPosition()

                if len(text) > 1 and text[pos - 1] in OPERATORS and text[pos - 2] == ' ':
                    text = text[:pos - 2] + text[pos:]
                    self.line_edit.setText(text)
                    self.line_edit.setCursorPosition(pos - 2)

                    pos -= 1

            elif event.text() in OPERATORS and event.text() != SYMBOL_DEGREE:
                pos = self.line_edit.cursorPosition()

                if event.text() == SYMBOL_MINUS and (len(text) == 0 or text[pos - 1] == SYMBOL_BRACKET_OPEN):
                    self.line_edit.keyPressEvent(event)
                    text = self.line_edit.text()
                else:
                    text = text[:pos] + ' ' + event.text() + ' ' + text[pos:]
                    self.line_edit.setText(text)
                    self.line_edit.setCursorPosition(pos + 3)
            elif event.text() in [' ', '=']:
                pass
            else:
                self.line_edit.keyPressEvent(event)
                text = self.line_edit.text()

            try:
                _ = self.lexer.parse(text)
                self.error_label.setText('')
            except LexerException as err:
                self.error_label.setText(str(err))
                # todo: err.pos

            return True

        return super().eventFilter(watched, event)
