from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout
import sys


class PhotoViewer(QWidget):
    def __init__(self):
        super(PhotoViewer, self).__init__()
        self.setWindowTitle("Photo Viewer")
        main_layout = QVBoxLayout(self)


app = QApplication(sys.argv)
win = PhotoViewer()
win.show()
app.exec_()
