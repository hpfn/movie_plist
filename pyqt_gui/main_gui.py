from info_in_db.movie_plist_sqlite3 import DataStorage
from pyqt_gui.pyqt_browser import qt_browser
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget, QRadioButton
from PyQt5.QtWidgets import QComboBox


class Window(QWidget):
    def __init__(self, scan_dir):
        super(QWidget, self).__init__()
        self.scanned_dir = scan_dir

        self.initui()

    def initui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        watch_0_button = QRadioButton(self.tr("&seen"))
        watch_1_button = QRadioButton(self.tr("&unseen"))

        movie_update_cbox = QComboBox()
        movie_update_cbox.addItem("insert movie file ")
        stored_data = DataStorage()
        movies_stored = stored_data.no_movie_yet()
        for title_year in movies_stored:
            title_l = list(title_year)
            movie_update_cbox.addItem(title_l[0])

        movie_remove_cbox = QComboBox()
        movie_remove_cbox.addItem("remove movie from hd ")
        # stored_data = DataStorage()
        movies_stored = stored_data.movie_list_title()
        for title_year in movies_stored:
            title_l = list(title_year)
            movie_remove_cbox.addItem(title_l[0])

        stored_data.exit_from_db()

        browser = qt_browser(self.scanned_dir)

        # formatted as
        # seen      insert
        # unseen    remove
        grid.addWidget(watch_0_button, 0, 0)
        grid.addWidget(watch_1_button, 1, 0)

        grid.addWidget(movie_update_cbox, 0, 2)
        grid.addWidget(movie_remove_cbox, 1, 2)

        grid.addWidget(browser, 2, 0, 7, 7)

        self.show()
