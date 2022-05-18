from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QScrollArea


class Scroller(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)

    def wheelEvent(self, event: QEvent):
        # disable mouse wheel scroll
        if event.type() == QEvent.Wheel:
            event.ignore()
