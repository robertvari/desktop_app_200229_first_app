from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, \
    QHBoxLayout, QListWidget, QTextEdit, QFileDialog

from PySide2.QtGui import QPainter, QPen, QBrush, QColor, QPixmap
from PySide2.QtCore import Qt, QSize, QRect

import sys, os
from PIL import Image, ExifTags


class PhotoViewer(QWidget):
    def __init__(self):
        super(PhotoViewer, self).__init__()
        self.setWindowTitle("Photo Viewer")
        self.resize(1000, 600)

        # app attributes
        self.current_dir = None
        self.file_list = []

        # main layout with open folder button
        main_layout = QVBoxLayout(self)

        self.open_bttn = QPushButton("Open Folder...")
        main_layout.addWidget(self.open_bttn)

        # hLayout for file list/details and Image
        h_layout = QHBoxLayout()
        main_layout.addLayout(h_layout)

        # hLayout with file list and photo details
        file_list_layout = QVBoxLayout()
        h_layout.addLayout(file_list_layout)

        # File list view
        self.file_list_view = QListWidget()
        self.file_list_view.setMaximumWidth(200)
        file_list_layout.addWidget(self.file_list_view)

        # photo details view
        self.photo_details = QTextEdit()
        self.photo_details.setReadOnly(True)
        self.photo_details.setMaximumHeight(80)
        self.photo_details.setMaximumWidth(200)
        file_list_layout.addWidget(self.photo_details)

        # image view
        self.image_viewer = ImageViewer()
        h_layout.addWidget(self.image_viewer)

        self.apply_style()

        # connect signals
        self.open_bttn.clicked.connect(self.open_folder_action)

        self.file_list_view.itemClicked.connect(self.photo_changed_action)
        self.file_list_view.itemDoubleClicked.connect(self.open_file_action)

    def apply_style(self):
        with open("style.css") as f:
            style = f.read()
            self.setStyleSheet(style)

    def getExif(self, filePath):
        exif_string = ""

        exif_string += f"File: {filePath}\n"

        img = Image.open(filePath)
        exif = img._getexif()
        if exif:
            for k, v in exif.items():
                if k in ExifTags.TAGS:
                    exifLabel = ExifTags.TAGS[k]

                    if exifLabel == "DateTimeOriginal":
                        exif_string += f"Date: {v}\n"

                    if exifLabel == "Model":
                        exif_string += f"Camera: {v}\n"

                    if exifLabel == "ISOSpeedRatings":
                        exif_string += f"ISO: {v}\n"



        return exif_string

    def photo_changed_action(self, item):
        current_photo = os.path.join(self.current_dir, item.text())

        exif_data = self.getExif(current_photo)
        self.photo_details.setText(exif_data)

        self.image_viewer.set_pixmap(current_photo)

    def open_file_action(self, item):
        os.startfile(os.path.join(self.current_dir, item.text()))

    def refresh_file_list_view(self):
        self.file_list_view.clear()

        for f in self.file_list:
            self.file_list_view.addItem(f)

    def collect_files(self):
        self.file_list = [i for i in os.listdir(self.current_dir) if i.lower().endswith(".jpg")]
        self.refresh_file_list_view()

    def open_folder_action(self):
        directory = QFileDialog.getExistingDirectory(self, "Select folder", "c:/")

        if len(directory):
            self.current_dir = directory.replace("/", "\\")

            self.open_bttn.setText(self.current_dir)
            self.setWindowTitle(f"Photo Viewer: {self.current_dir}")
            self.collect_files()


class ImageViewer(QWidget):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.painter = QPainter()
        self.my_pen = QPen(QColor("red"))
        self.my_pen.setWidth(5)

        self.my_brush = QBrush(QColor("#123456"))

        self.photo = QPixmap()
        self.photo_rect = QRect()

    def set_pixmap(self, image_path):
        self.photo.load(image_path)
        self.repaint()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.draw()
        self.painter.end()

    def draw(self):
        rect = self.rect()

        self.painter.setPen(self.my_pen)
        self.painter.setBrush(self.my_brush)

        photo = self.photo.scaled(QSize(rect.width(), rect.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.photo_rect.setRect(rect.x(), rect.y(), photo.width(), photo.height())
        self.photo_rect.moveCenter(rect.center())

        self.painter.drawPixmap(self.photo_rect, photo)

app = QApplication(sys.argv)
win = PhotoViewer()
win.show()
app.exec_()
