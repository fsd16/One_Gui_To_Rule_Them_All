
import logging
from PySide6.QtWidgets import QPlainTextEdit

class QPlainTextEditLogger(logging.Handler, QPlainTextEdit):
    def __init__(self, parent=None, *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        QPlainTextEdit.__init__(self, parent, *args, **kwargs)
        self.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText(msg)