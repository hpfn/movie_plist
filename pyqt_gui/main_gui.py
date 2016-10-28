
from pyqt_gui.pyqt_browser import qt_browser
from pyqt_gui.combo_box import Combo

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget, QRadioButton


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

        # Combo inherit QComboBox
        movie_update_cbox = Combo("update")
        movie_remove_cbox = Combo("remove")

        # movie selected. remove/update info in the db
        movie_update_cbox.get_item_selected()
        movie_remove_cbox.get_item_selected()

        browser = qt_browser(self.scanned_dir)

        # formatted as
        # seen      insert (movie in db)
        # unseen    remove (movie from db)
        grid.addWidget(watch_0_button, 0, 0)
        grid.addWidget(watch_1_button, 1, 0)

        grid.addWidget(movie_update_cbox, 0, 2)
        grid.addWidget(movie_remove_cbox, 1, 2)

        grid.addWidget(browser, 2, 0, 7, 7)

        self.show()
