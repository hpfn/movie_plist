from PyQt5.QtWidgets import QMessageBox
from .combo_box_interact import InteractBox
from .combo_box_build import Combo


class CboxSeen(Combo):
    def __init__(self):
        super().__init__()

    def combo_list(self):
        """
            sqlite returns a list of tuples
            using a for loop to have a 'str' item
            and be easier to find the index on
            confirm_option method (InteractBox())
        """
        # self.movies_stored = ['seen movies']
        #for i in self.stored_data.movie_seen():
        #    self.movies_stored.append(i[0])
        self.movies_stored = [i[0] for i in self.stored_data.movie_seen()]
        self.movies_stored.insert(0, 'seen movies')

        # self.show_list()

    def confirm_option(self, index, movie_selected):
        """ show msg with a synopsis of the movie"""
        # msg.setIcon(QMessageBox.Information)
        try:
            txt_info = "Put a synopsis here for " + movie_selected
            msg = QMessageBox()
            reply = msg.question(self, 'The selected movie', txt_info,
                                 QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                html_cboxlist_changes = InteractBox(movie_selected)
                html_cboxlist_changes.watch_movie()
            else:
                msg.text("Ignore this window")
            msg.exec()
        except TypeError:
            print('Error when trying to load the movie')
            print('"{}" is not a valid entry' .format(movie_selected))





















































