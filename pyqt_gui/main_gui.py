
from pyqt_gui.pyqt_browser import qt_browser
from pyqt_gui.combo_box_build import Combo

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget  # , QRadioButton


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

        # watch_0_button = QRadioButton(self.tr("&seen"))
        # watch_1_button = QRadioButton(self.tr("&unseen"))

        # Combo inherit QComboBox
        movie_update_cbox = Combo("update", None, None, self.scanned_dir_and_html, browser)
        movie_seen_cbox = Combo("watch_again")
        movie_remove_cbox = Combo("remove", movie_update_cbox, movie_seen_cbox)

        # movie selected. remove/update info in the db
        movie_update_cbox.get_item_selected()
        movie_remove_cbox.get_item_selected()
        movie_seen_cbox.get_item_selected()

        # browser = qt_browser(self.scanned_dir)

        # formatted as
        # seen insert (movie in db) remove (movie from db)
        # old format grid.addWidget(watch_0_button, 0, 0)
        # old format grid.addWidget(watch_1_button, 1, 0)
        grid.addWidget(movie_seen_cbox, 0, 0)
        grid.addWidget(movie_update_cbox, 0, 1)
        grid.addWidget(movie_remove_cbox, 0, 2)

        grid.addWidget(browser, 1, 0,7 ,7)

        self.show()
