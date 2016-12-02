from PyQt5.QtWidgets import QMessageBox
from .combo_box_build import Combo
from .combo_box_interact import InteractBox


class CboxRemove(Combo):
    def __init__(self, update_object, seen_object, browser_obj):
        super().__init__()
        self.watch_again = seen_object
        self.up_date = update_object
        self.browser_reload = browser_obj

    def combo_list(self):
        """
            sqlite returns a list of tuples
            using a for loop to have a 'str' item
            and be easier to find the index on
            confirm_option method (InteractBox())
        """
        self.movies_stored = [i[0] for i in self.stored_data.movie_title_list()]
        self.movies_stored.insert(0, 'remove movie from db')

    def confirm_option(self, index, movie_selected):
        """ show msg about what to_do with the movie selected"""
        if index:
            txt_info = "You will remove " + movie_selected
            msg = QMessageBox()
            reply = msg.question(self, 'The selected movie', txt_info,
                                 QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

            if reply == QMessageBox.Yes:
                msg.setText('remove this window!!!')
                html_cboxlist_changes = InteractBox(movie_selected)
                html_cboxlist_changes.movie_remove(self.up_date, self.watch_again, self.browser_reload)
                self.removeItem(index)
            else:
                # how to ignore this ???
                # QEvent.setAccepted()
                msg.setText('Doing nothing.')

            msg.exec_()





















































