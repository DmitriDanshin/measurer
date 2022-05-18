import json
import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QImage, QPalette, QWheelEvent
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QAction,
                             QSlider, QToolButton, QToolBar, QDockWidget, QMessageBox,
                             QGridLayout, QScrollBar)

from views.image import Image
from views.scroller import Scroller


def load_settings():
    with open('settings.json') as settings_file:
        return json.load(settings_file)


settings = load_settings()


class MeasurerGUI(QMainWindow):
    scroll_area: Scroller
    exit_act: QAction
    new_act: QAction

    def __init__(self):
        super().__init__()
        self.initializeUI()
        self.image = QImage()

    def initializeUI(self):
        self.setMinimumSize(
            settings["MAIN_WINDOW"]["MIN_WIDTH"],
            settings["MAIN_WINDOW"]["MIN_HEIGHT"]
        )
        self.setWindowTitle(
            settings["MAIN_WINDOW"]["TITLE"]
        )
        self.showMaximized()
        self.createMainLabel()
        self.createEditingBar()
        self.create_menu()
        self.createToolBar()
        self.show()

    def create_menu(self) -> None:
        """Set up the menubar."""
        # Actions for Photo Editor menu
        about_act = QAction('About', self)
        about_act.triggered.connect(self.aboutDialog)

        self.exit_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "exit.png")), 'Quit Photo Editor', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.triggered.connect(self.close)

        # Actions for File menu
        self.new_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "new.png")), 'New...')

        self.open_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "open.png")), 'Open...', self)
        self.open_act.setShortcut('Ctrl+O')
        self.open_act.triggered.connect(self.image_label.open_image)

        self.print_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "print.png")), "Print...", self)
        self.print_act.setShortcut('Ctrl+P')
        self.print_act.setEnabled(False)

        self.save_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "save.png")), "Save...", self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.triggered.connect(self.image_label.save_image)
        self.save_act.setEnabled(False)

        # Actions for Edit menu
        self.revert_act = QAction("Revert to Original", self)
        self.revert_act.triggered.connect(self.image_label.revertToOriginal)
        self.revert_act.setEnabled(False)

        # Actions for Tools menu
        self.crop_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "crop.png")), "Crop", self)
        self.crop_act.setShortcut('Shift+X')
        self.crop_act.triggered.connect(self.image_label.cropImage)

        self.resize_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "resize.png")), "Resize", self)
        self.resize_act.setShortcut('Shift+Z')
        self.resize_act.triggered.connect(self.image_label.resizeImage)

        self.rotate90_cw_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "rotate90_cw.png")), 'Rotate 90º CW',
                                       self)
        self.rotate90_cw_act.triggered.connect(
            lambda: self.image_label.rotate_image(settings["ROTATION_DIRECTION"]["CW"])
        )

        self.rotate90_ccw_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "rotate90_ccw.png")),
                                        'Rotate 90º CCW', self)
        self.rotate90_ccw_act.triggered.connect(
            lambda: self.image_label.rotate_image(settings["ROTATION_DIRECTION"]["CCW"])
        )

        self.flip_horizontal = QAction(
            QIcon(os.path.join(settings['ICON_PATH'], "flip_horizontal.png")), 'Flip Horizontal', self
        )
        self.flip_horizontal.triggered.connect(
            lambda: self.image_label.flip_image(settings["REFLECTION_DIRECTION"]["HORIZONTAL"])
        )

        self.flip_vertical = QAction(QIcon(os.path.join(settings['ICON_PATH'], "flip_vertical.png")), 'Flip Vertical',
                                     self)
        self.flip_vertical.triggered.connect(
            lambda: self.image_label.flip_image(settings["REFLECTION_DIRECTION"]["VERTICAL"])
        )

        self.zoom_in_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "zoom_in.png")), 'Zoom In', self)
        self.zoom_in_act.setShortcut('Ctrl++')
        self.zoom_in_act.triggered.connect(lambda: self.zoom_image(1.25))
        self.zoom_in_act.setEnabled(False)

        self.zoom_out_act = QAction(QIcon(os.path.join(settings['ICON_PATH'], "zoom_out.png")), 'Zoom Out', self)
        self.zoom_out_act.setShortcut('Ctrl+-')
        self.zoom_out_act.triggered.connect(lambda: self.zoom_image(0.8))
        self.zoom_out_act.setEnabled(False)

        self.normal_size_act = QAction("Normal Size", self)
        self.normal_size_act.setShortcut('Ctrl+=')
        self.normal_size_act.triggered.connect(self.normalize_size)
        self.normal_size_act.setEnabled(False)

        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create Photo Editor menu and add actions
        main_menu = menu_bar.addMenu('Photo Editor')
        main_menu.addAction(about_act)
        main_menu.addSeparator()
        main_menu.addAction(self.exit_act)

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)
        file_menu.addSeparator()
        file_menu.addAction(self.print_act)

        edit_menu = menu_bar.addMenu('Edit')
        edit_menu.addAction(self.revert_act)

        views_menu = menu_bar.addMenu('Views')
        views_menu.addAction(self.tools_menu_act)

    def createToolBar(self):
        """Set up the toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(26, 26))
        self.addToolBar(toolbar)

        # Add actions to the toolbar
        toolbar.addAction(self.open_act)
        toolbar.addAction(self.save_act)
        toolbar.addAction(self.print_act)
        toolbar.addAction(self.exit_act)
        toolbar.addSeparator()
        toolbar.addAction(self.crop_act)
        toolbar.addAction(self.resize_act)
        toolbar.addSeparator()
        toolbar.addAction(self.rotate90_ccw_act)
        toolbar.addAction(self.rotate90_cw_act)
        toolbar.addAction(self.flip_horizontal)
        toolbar.addAction(self.flip_vertical)
        toolbar.addSeparator()
        toolbar.addAction(self.zoom_in_act)
        toolbar.addAction(self.zoom_out_act)

    def createEditingBar(self):
        """Create dock widget for editing tools."""
        self.editing_bar = QDockWidget("Tools")
        self.editing_bar.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.editing_bar.setMinimumWidth(90)

        convert_to_grayscale = QToolButton()
        convert_to_grayscale.setIcon(QIcon(os.path.join(settings['ICON_PATH'], "grayscale.png")))
        convert_to_grayscale.clicked.connect(self.image_label.convertToGray)

        convert_to_RGB = QToolButton()
        convert_to_RGB.setIcon(QIcon(os.path.join(settings['ICON_PATH'], "rgb.png")))
        convert_to_RGB.clicked.connect(self.image_label.convert2rgb)

        convert_to_sepia = QToolButton()
        convert_to_sepia.setIcon(QIcon(os.path.join(settings['ICON_PATH'], "sepia.png")))
        convert_to_sepia.clicked.connect(self.image_label.convertToSepia)

        change_hue = QToolButton()
        change_hue.setIcon(QIcon(os.path.join(settings['ICON_PATH'], "")))
        change_hue.clicked.connect(self.image_label.changeHue)

        brightness_label = QLabel("Brightness")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(settings['BRIGHTNESS_MIN_VALUE'], settings['BRIGHTNESS_MAX_VALUE'])
        self.brightness_slider.setTickInterval(35)
        self.brightness_slider.setTickPosition(QSlider.TicksAbove)
        self.brightness_slider.valueChanged.connect(self.image_label.change_brightness)

        contrast_label = QLabel("Contrast")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(settings['CONTRAST_MIN_VALUE'], settings['CONTRAST_MAX_VALUE'])
        self.contrast_slider.setTickInterval(35)
        self.contrast_slider.setTickPosition(QSlider.TicksAbove)
        self.contrast_slider.valueChanged.connect(self.image_label.change_contrast)

        editing_grid = QGridLayout()

        editing_grid.addWidget(convert_to_grayscale, 1, 0)
        editing_grid.addWidget(convert_to_RGB, 1, 1)
        editing_grid.addWidget(convert_to_sepia, 2, 0)
        editing_grid.addWidget(change_hue, 2, 1)
        editing_grid.addWidget(brightness_label, 3, 0)
        editing_grid.addWidget(self.brightness_slider, 4, 0, 1, 0)
        editing_grid.addWidget(contrast_label, 5, 0)
        editing_grid.addWidget(self.contrast_slider, 6, 0, 1, 0)
        editing_grid.setRowStretch(7, 10)

        container = QWidget()
        container.setLayout(editing_grid)

        self.editing_bar.setWidget(container)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.editing_bar)

        self.tools_menu_act = self.editing_bar.toggleViewAction()

    def createMainLabel(self):
        """Create an instance of the ImageLabel class and set it
           as the main window's central widget."""
        self.image_label = Image(self)
        self.image_label.resize(self.image_label.pixmap().size())

        self.scroll_area = Scroller()
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.image_label)

        self.setCentralWidget(self.scroll_area)

    def updateActions(self):
        """Update the values of menu and toolbar items when an image
        is loaded."""
        self.save_act.setEnabled(True)
        self.revert_act.setEnabled(True)
        self.zoom_in_act.setEnabled(True)
        self.zoom_out_act.setEnabled(True)
        self.normal_size_act.setEnabled(True)

    def zoom_image(self, zoom_value: float) -> None:
        """Zoom in and zoom out."""

        self.image_label.resize(self.image_label.size() * zoom_value)

        self.__adjust_scrollbar(self.scroll_area.horizontalScrollBar(), zoom_value)
        self.__adjust_scrollbar(self.scroll_area.verticalScrollBar(), zoom_value)

    def normalize_size(self):
        """View image with its normal dimensions."""
        self.image_label.adjustSize()

    @staticmethod
    def __adjust_scrollbar(scroll_bar: QScrollBar, value: float) -> None:
        """Adjust the scrollbar when zooming in or out."""
        value = int(value * scroll_bar.value() + ((value - 1) * scroll_bar.pageStep() / 2))
        scroll_bar.setValue(value)

    def aboutDialog(self):
        QMessageBox.about(self, "About Photo Editor",
                          "Measurer particles")

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_F1:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

    def wheelEvent(self, event: QWheelEvent) -> None:
        wheel_direction = event.angleDelta().y()
        if wheel_direction == settings["MOUSEWHEEL_UP"]:
            self.zoom_image(1 + settings['ZOOM_FACTOR'])
        elif wheel_direction == settings["MOUSEWHEEL_DOWN"]:
            self.zoom_image(1 - settings['ZOOM_FACTOR'])

    def closeEvent(self, event):
        pass
