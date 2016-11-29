from .pyqt_browser import qt_browser
from .combo_box_seen import CboxSeen
from .combo_box_update import CboxUpdate
from .combo_box_remove import CboxRemove

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget


class Window(QWidget):
    def __init__(self, scan_dir_html):
        super(QWidget, self).__init__()
        self.scanned_dir_and_html = scan_dir_html

        self.initui()

    def initui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # QWebView object
        browser = qt_browser(self.scanned_dir_and_html)

        # Combo inherit QComboBox
        movie_update_cbox = CboxUpdate(browser)
        movie_seen_cbox = CboxSeen()
        movie_remove_cbox = CboxRemove(movie_update_cbox, movie_seen_cbox, browser)

        # movie selected. remove/update info in the db
        movie_update_cbox.get_item_selected()
        movie_remove_cbox.get_item_selected()
        movie_seen_cbox.get_item_selected()

        # Combo box formatted as
        # 'seen' 'insert movie in db' 'remove movie from db'
        grid.addWidget(movie_seen_cbox, 0, 0)
        grid.addWidget(movie_update_cbox, 0, 1)
        grid.addWidget(movie_remove_cbox, 0, 2)
        # the .html file
        grid.addWidget(browser, 1, 0, 7, 7)

        self.show()
