import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from measurer.gui import MeasurerGUI


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    window = MeasurerGUI()
    sys.exit(app.exec_())
