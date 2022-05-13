import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from measurer.gui import MeasurerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
    window = MeasurerGUI()
    sys.exit(app.exec_())
