import logging

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal

from .spinner import Spinner
from .tools import center_widget
from .check_version import CheckVersionMessage


class WaitWindow(QWidget):
    sigUpdateClicked = pyqtSignal()
    sigRestartClicked = pyqtSignal()
    sigCheckClicked = pyqtSignal()

    log = logging.getLogger(__name__)

    def __init__(self, label: str = 'You use the latest version!', parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # self.setWindowModality(Qt.ApplicationModal)

        self.spinner = Spinner(self)
        self.spinner.pause()
        self.spinner.hide()

        self.check_button = QPushButton('Check for updates')
        self.check_button.clicked.connect(self.sigCheckClicked)

        self.update_button = QPushButton('Update')
        self.update_button.clicked.connect(self.sigUpdateClicked)
        self.update_button.hide()
        self.update_button.setDisabled(True)

        self.restart_button = QPushButton('Restart')
        self.restart_button.clicked.connect(self.sigRestartClicked)
        self.restart_button.hide()
        self.restart_button.setDisabled(True)

        self.label = QLabel(label)
        self.setMinimumWidth(700)
        self.setFixedHeight(150)

        layout = QGridLayout(self)
        layout.addWidget(self.spinner, 0, 0)
        layout.addWidget(self.check_button, 1, 0, 1, 3)
        layout.addWidget(self.label, 0, 1)
        layout.addWidget(self.update_button, 0, 2)
        layout.addWidget(self.restart_button, 0, 3)

        center_widget(self)
        self.show()

    def set_text(self, text: str):
        self.label.setText(text)

    def on_checking(self):
        self.spinner.show()
        self.spinner.resume()
        self.check_button.setDisabled(True)

    def on_update(self):
        self.spinner.show()
        self.spinner.resume()
        self.label.setText('Updating version ...')
        self.update_button.hide()
        self.check_button.hide()

    def _update_clicked(self):
        self.sigUpdateClicked.emit()

    def show_info(self, text: str, hide_spinner: bool = True):
        if hide_spinner:
            self.spinner.pause()
            self.spinner.hide()
        self.label.setText(text)
        self.check_button.show()

    def show_restart(self):
        self.spinner.pause()
        self.spinner.hide()
        self.label.setText('Please, restart the program.')
        self.restart_button.show()
        self.restart_button.setDisabled(False)

    @pyqtSlot(object, name='checkOutdated')
    def get_result(self, res: CheckVersionMessage):
        if res == CheckVersionMessage.no_internet:
            self.set_text('Could not check the latest version (connection error).')
        if res == CheckVersionMessage.error:
            self.set_text('Could not check the latest version.')
        if res == CheckVersionMessage.latest_version_installed:
            self.set_text(f'You use the latest version {res.version}!')
        if res == CheckVersionMessage.new_version_available:
            self.set_text(f'New version available: {res.version}. Please, update your program.')
            self.update_button.setDisabled(False)
            self.update_button.show()

        self.spinner.pause()
        self.spinner.hide()

        self.check_button.show()
        self.check_button.setDisabled(False)
