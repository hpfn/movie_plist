# from PyQt5.QtWidgets import QMessageBox
# from PyQt5.QtCore import QEvent
from .combo_box_build import Combo
# from .combo_box_interact import InteractBox


class CboxUpdate(Combo):
    def __init__(self, browser_obj=None):
        super().__init__()
        self.browser_reload = browser_obj

    def combo_list(self):
        """
            sqlite returns a list of tuples
            using a for loop to have a 'str' item
            and be easier to find the index on
            confirm_option method (InteractBox())
        """
        self.movies_stored = [i[0] for i in self.stored_data.no_movie_yet()]
        self.movies_stored.insert(0, 'insert movie file')

    def confirm_option(self, index, movie_selected):
        """ show msg about what to_do with the movie selected"""
        # msg = QMessageBox()
        if index:
            from .combo_box_interact import InteractBox

            html_cboxlist_changes = InteractBox(movie_selected)
            html_cboxlist_changes.insert_movie_file_action(self.browser_reload)
            self.removeItem(index)
