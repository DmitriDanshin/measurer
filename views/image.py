import cv2
import numpy as np

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPixmap, QImage, QColor, QTransform, qRgb
from PyQt5.QtWidgets import QLabel, QMessageBox, QFileDialog, QSizePolicy, QRubberBand, QMainWindow


# TODO: save all parameters state after each change

class MainImage(QImage):
    @property
    def as_array(self):
        image = self.convertToFormat(QImage.Format_RGB32)

        width = image.width()
        height = image.height()

        ptr = image.bits()
        ptr.setsize(image.byteCount())

        return np.array(ptr).reshape((height, width, QImage.Format_RGB32))

    def as_qimage(self):
        return self.copy()

    def update(self, new_image: "MainImage") -> None:
        raise NotImplemented()


class Image(QLabel):
    """Subclass of QLabel for displaying image"""
    image: MainImage
    original_image: MainImage
    qpixmap: QPixmap

    def __init__(self, parent: QMainWindow):
        super().__init__(parent)

        self.parent = parent

        self.image = MainImage()

        self.original_image = self.image

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

        self.__init_settings()

    def __init_settings(self):
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setScaledContents(True)
        self.qpixmap = QPixmap()
        self.setPixmap(self.qpixmap.fromImage(self.image))
        self.setAlignment(Qt.AlignCenter)

    def open_image(self) -> None:
        """Load a new image into the label"""
        options = QFileDialog.Options() | QFileDialog.DontUseNativeDialog
        image, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                               "All Files (*);;Python Files (*.py)", options=options)
        if image:
            self.parent.print_act.setEnabled(True)
            self.parent.update_actions()
            self.image = MainImage(image)
            self.original_image = self.image.copy()
            self.setPixmap(QPixmap().fromImage(self.image))
            self.resize(self.pixmap().size())

    def save_image(self) -> None:
        """Save the image displayed in the label."""

        if not self.image.isNull():
            image, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                   "PNG Files (*.png);;JPG Files (*.jpeg *.jpg );;Bitmap Files ("
                                                   "*.bmp);; GIF Files (*.gif)")
            if image:
                self.image.save(image)
            else:
                QMessageBox.information(self, "Error",
                                        "Unable to save image.", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Empty Image",
                                    "There is no image to save.", QMessageBox.Ok)

    def clear_image(self) -> None:
        raise NotImplemented()

    def revertToOriginal(self):
        """Revert the image back to original image."""
        # TODO: Display message dialog to confirm actions
        self.image = self.original_image
        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()

    def resizeImage(self):
        """Resize image."""
        # TODO: Resize image by specified size
        if self.image.isNull() == False:
            resize = QTransform().scale(0.5, 0.5)

            pixmap = QPixmap(self.image)

            resized_image = pixmap.transformed(resize, mode=Qt.SmoothTransformation)
            # rotated = pixmap.trueMatrix(transform90, pixmap.width, pixmap.height)

            # self.image_label.setPixmap(rotated)

            # self.image_label.setPixmap(rotated.scaled(self.image_label.size(),
            #    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.image = QImage(resized_image)
            self.setPixmap(resized_image)
            # self.image = QPixmap(rotated)
            self.setScaledContents(True)
            self.repaint()  # repaint the child widget
        else:
            # No image to rotate
            pass

    def cropImage(self):
        """Crop selected portions in the image."""
        if self.image.isNull() == False:
            rect = QRect(10, 20, 400, 200)
            original_image = self.image
            cropped = original_image.copy(rect)

            self.image = QImage(cropped)
            self.setPixmap(QPixmap().fromImage(cropped))

    def rotate_image(self, direction: int) -> None:
        """Rotate image"""
        if not self.image.isNull():
            transform = QTransform().rotate(direction)
            pixmap = QPixmap(self.image.as_qimage())
            rotated = pixmap.transformed(transform, mode=Qt.SmoothTransformation)

            self.resize(self.image.height(), self.image.width())
            self.image = MainImage(rotated)
            self.setPixmap(rotated.scaled(self.size()))
            self.repaint()

    def flip_image(self, axis: tuple[float, float]) -> None:
        """Mirror the image across the horizontal axis."""
        if not self.image.isNull():
            transform = QTransform().scale(*axis)

            pixmap = QPixmap(self.image.as_qimage())
            flipped = pixmap.transformed(transform)

            self.image = MainImage(flipped)
            self.setPixmap(flipped)
            self.repaint()

    def convertToGray(self):
        """Convert image to grayscale."""
        if self.image.isNull() == False:
            converted_img = self.image.convertToFormat(QImage.Format_Grayscale16)
            # self.image = converted_img
            self.image = QImage(converted_img)
            self.setPixmap(QPixmap().fromImage(converted_img))
            self.repaint()

    def convert2rgb(self):
        """Convert image to RGB format."""
        if self.image.isNull() == False:
            converted_img = self.image.convertToFormat(QImage.Format_RGB32)
            # self.image = converted_img
            self.image = QImage(converted_img)
            self.setPixmap(QPixmap().fromImage(converted_img))
            self.repaint()

    def convertToSepia(self):
        """Convert image to sepia filter."""
        # TODO: Sepia #704214 rgb(112, 66, 20)
        # TODO: optimize speed that the image converts, or add to thread
        if self.image.isNull() == False:
            for row_pixel in range(self.image.width()):
                for col_pixel in range(self.image.height()):
                    current_val = QColor(self.image.pixel(row_pixel, col_pixel))

                    # Calculate r, g, b values for current pixel
                    red = current_val.red()
                    green = current_val.green()
                    blue = current_val.blue()

                    new_red = int(0.393 * red + 0.769 * green + 0.189 * blue)
                    new_green = int(0.349 * red + 0.686 * green + 0.168 * blue)
                    new_blue = int(0.272 * red + 0.534 * green + 0.131 * blue)

                    # Set the new RGB values for the current pixel
                    if new_red > 255:
                        red = 255
                    else:
                        red = new_red

                    if new_green > 255:
                        green = 255
                    else:
                        green = new_green

                    if new_blue > 255:
                        blue = 255
                    else:
                        blue = new_blue

                    new_value = qRgb(red, green, blue)
                    self.image.setPixel(row_pixel, col_pixel, new_value)

        self.setPixmap(QPixmap().fromImage(self.image))
        self.repaint()

    def __image_exists(self) -> bool:
        return bool(self.image.width() and self.image.height())

    def __get_pixmap(self, image_array: np.array) -> QPixmap:
        qimage = MainImage(
            image_array,
            image_array.shape[1],
            image_array.shape[0],
            QImage.Format_RGB32
        ).as_qimage()

        return self.qpixmap.fromImage(qimage)

    def change_brightness(self, brightness: int) -> None:
        """
        Change the brightness of the pixels in the image.
        Brightness is the measured intensity of all the pixels.
        """

        if not self.__image_exists():
            return

        image_array = self.image.as_array
        zeros = np.zeros(image_array.shape, image_array.dtype)

        image_array = cv2.addWeighted(image_array, 1, zeros, 0, brightness)

        pixmap = self.__get_pixmap(image_array)

        self.setPixmap(pixmap)

    def change_contrast(self, contrast: int) -> None:
        """
        Change the contrast of the pixels in the image.
        Contrast is the difference between max and min pixel intensity.
        """

        if not self.__image_exists():
            return

        image = self.image.as_array
        zeros = np.zeros(image.shape, image.dtype)
        image_array = cv2.addWeighted(image, 1.0 + contrast / 100, zeros, 0, 0)

        pixmap = self.__get_pixmap(image_array)

        self.setPixmap(pixmap)

    def changeHue(self):
        for row_pixel in range(self.image.width()):
            for col_pixel in range(self.image.height()):
                current_val = QColor(self.image.pixel(row_pixel, col_pixel))

                hue = current_val.hue()

                current_val.setHsv(hue, current_val.saturation(),
                                   current_val.value(), current_val.alpha())
                self.image.setPixelColor(row_pixel, col_pixel, current_val)

        self.setPixmap(QPixmap().fromImage(self.image))

    def mousePressEvent(self, event):
        """Handle mouse press event."""
        self.origin = event.pos()
        if not self.rubber_band:
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()

        # print(self.rubber_band.height())
        print(self.rubber_band.x())

    def mouseMoveEvent(self, event):
        """Handle mouse move event."""
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        """Handle when the mouse is released."""
        self.rubber_band.hide()
