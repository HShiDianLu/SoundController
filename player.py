import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QLabel):
    def __init__(self, images_folder, image_show_width, image_show_height):
        super().__init__()

        self.images_folder = images_folder
        self.image_show_width = image_show_width
        self.image_show_height = image_show_height

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Drawer)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(QApplication.desktop().screenGeometry().width() - image_show_width,
                         QApplication.desktop().screenGeometry().height() - image_show_height - 100, image_show_width,
                         image_show_height)
        self.setScaledContents(False)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)
        self.timer.start(16)

        self.images = os.listdir(os.path.join(os.getcwd(), images_folder))
        self.max_num = len(self.images) - 1
        self.num = 0
        self.set_image()
        self.wait_time = 0

    def set_image(self):
        path = os.path.join(os.getcwd(), self.images_folder, self.images[self.num])
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(self.image_show_width, self.image_show_height)
        self.setPixmap(pixmap)

    def change_image(self):
        if self.num == 125 and self.wait_time < 200:
            self.wait_time += 1
        else:
            self.num += 1
        if self.num > self.max_num:
            self.num = self.max_num
            self.destroy()
            sys.exit()
        self.set_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow("anim/" + sys.argv[1], 1558, 681)
    w.show()
    sys.exit(app.exec_())
