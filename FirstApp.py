from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, \
    QHBoxLayout, QLabel, QListWidget, QTextEdit, QFileDialog
import sys


class PhotoViewer(QWidget):
    def __init__(self):
        super(PhotoViewer, self).__init__()
        self.setWindowTitle("Photo Viewer")
        self.resize(1000, 600)

        # app attributes
        self.current_dir = None

        # main layout with open folder button
        main_layout = QVBoxLayout(self)

        open_bttn = QPushButton("Open Folder...")
        main_layout.addWidget(open_bttn)

        # hLayout for file list/details and Image
        h_layout = QHBoxLayout()
        main_layout.addLayout(h_layout)

        # hLayout with file list and photo details
        file_list_layout = QVBoxLayout()
        h_layout.addLayout(file_list_layout)

        # File list view
        file_list = QListWidget()
        file_list.setMaximumWidth(200)
        file_list_layout.addWidget(file_list)

        # photo details view
        photo_details = QTextEdit()
        photo_details.setMaximumHeight(80)
        photo_details.setMaximumWidth(200)
        file_list_layout.addWidget(photo_details)

        # image view
        image_label = QLabel("IMAGE")
        h_layout.addWidget(image_label)

        # connect signals
        open_bttn.clicked.connect(self.open_folder_action)

    def collect_files(self):
        print(self.current_dir)

    def open_folder_action(self):
        directory = QFileDialog.getExistingDirectory(self, "Select folder", "c:/")

        if len(directory):
            self.current_dir = directory
            self.collect_files()


app = QApplication(sys.argv)
win = PhotoViewer()
win.show()
app.exec_()
