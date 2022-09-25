import sys
import urllib.request

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QProgressBar, QPushButton, QApplication, QMessageBox, \
    QFileDialog


class Downloader(QDialog):

    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()

        self.url = QLineEdit()
        self.save_location = QLineEdit()
        self.progress = QProgressBar()
        download = QPushButton("Download")
        browse = QPushButton("Browse")

        self.url.setPlaceholderText("URL")
        self.save_location.setPlaceholderText("File save location")

        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.url)
        layout.addWidget(self.save_location)
        layout.addWidget(self.progress)
        layout.addWidget(browse)
        layout.addWidget(download)

        self.setLayout(layout)
        self.setWindowTitle("PyDownloader")
        self.setFocus()

        download.clicked.connect(self.download)
        browse.clicked.connect(self.browse_file)

    def browse_file(self):
        save_file = QFileDialog.getSaveFileName(self, caption="Save File As", directory=".", filter="All Files (*.*)")
        self.save_location.setText(QDir.toNativeSeparators(save_file[0]))

    def download(self):
        url = self.url.text()
        save_location = self.save_location.text()

        try:
            urllib.request.urlretrieve(url, save_location, self.report)
        except Exception:
            QMessageBox.warning(self, "Warning", "The download failed")
        else:
            QMessageBox.information(self, "Information", "The download is complete!")
            self.progress.setValue(0)
            self.url.setText("")
            self.save_location.setText("")

    def report(self, block_num, block_size, total_size):
        progress = block_num * block_size

        if total_size > 0:
            percent = progress * 100 / total_size
            self.progress.setValue(int(percent))


app = QApplication(sys.argv)
dialog = Downloader()
dialog.show()
app.exec_()
