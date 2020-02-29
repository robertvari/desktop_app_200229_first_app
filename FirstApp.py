from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, \
    QHBoxLayout, QLabel, QListWidget, QTextEdit, QFileDialog
import sys, os


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

        open_bttn = QPushButton("Open Folder...")
        main_layout.addWidget(open_bttn)

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
        photo_details = QTextEdit()
        photo_details.setMaximumHeight(80)
        photo_details.setMaximumWidth(200)
        file_list_layout.addWidget(photo_details)

        # image view
        image_label = QLabel("IMAGE")
        h_layout.addWidget(image_label)

        # connect signals
        open_bttn.clicked.connect(self.open_folder_action)

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
            self.current_dir = directory
            self.collect_files()


app = QApplication(sys.argv)
win = PhotoViewer()
win.show()
app.exec_()
