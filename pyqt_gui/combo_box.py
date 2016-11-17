from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
# from PyQt5.QtCore import QEvent
from info_in_db.movie_plist_sqlite3 import DataStorage

from subprocess import call

from data.pyscan import PyScan
import html_file.create_page


class Combo(QComboBox):
    def __init__(self, will_do, update_object=None, seen_object=None, scan_local_html=None, browser_obj=None):
        super().__init__()
        self.to_do = will_do
        self.path_html = scan_local_html
        self.watch_again = seen_object
        self.watch_again_list = None
        self.up_date = update_object
        self.insert_movie_file_list= None
        self.browser_reload = browser_obj
        self.stored_data = DataStorage()
        self.movies_stored = ""

        self.first_item_combo()
        self.combo_list()

    def first_item_combo(self):
        def update(self):
            self.addItem("insert movie file ")
            self.insert_movie_file_list = ['insert movie file']

        def remove(self):
            self.addItem("remove movie from db")

        def seen(self):
            self.addItem("seen movies")
            self.watch_again_list = ['seen movies']

        option = {"update": update,
                  "remove": remove,
                  "watch_again": seen}
        option[self.to_do](self)

    def combo_list(self):
        def update(self):
            self.movies_stored = self.stored_data.no_movie_yet()
            # doing this here make update in confirm_option
            # method easier to read
            for i in self.movies_stored:
                self.insert_movie_file_list.append(i[0])

        def remove(self):
            self.movies_stored = self.stored_data.movie_title_list()

        def seen(self):
            self.movies_stored = self.stored_data.movie_seen()
            # doing this here make remove() in confirm_option
            # method easier to read
            for i in self.movies_stored:
                self.watch_again_list.append(i[0])

        option = {"update": update,
                  "remove": remove,
                  "watch_again": seen}

        option[self.to_do](self)
        self.show_list()

    def show_list(self):
        for title_year in self.movies_stored:
            title_l = list(title_year)
            self.add_to_cbox(title_l[0])

    def add_to_cbox(self, item):
        self.addItem(item)

    def get_item_selected(self):
        self.activated.connect(lambda s_item: self.confirm_option(s_item, self.currentText()))

    def confirm_option(self, index, movie_selected):
        """ show msg about what to_do with the movie selected"""
        txt_info = "You will " + self.to_do + " " + movie_selected
        msg = QMessageBox()
        reply = msg.question(self, 'The selected movie', txt_info,
                             QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            # call db
            # rebuild .html file
            msg.setText('remove this window!!!')

            def update(self):
                p_file = self.stored_data.movie_path(movie_selected)
                # scan selected movie dir
                scan_dir = PyScan(p_file[0])
                scan_dir = scan_dir.dir_to_scan()
                # file name
                file_n = scan_dir[0][2]
                self.stored_data.update_movie_file(file_n, movie_selected)
                # update list
                self.removeItem(index)
                # Regrex edit .html file ? re-create by now. First get the movies
                # then rm the html file and re-create.
                # This can be better
                unseen_movies = self.stored_data.movie_unseen()
                html_f = self.path_html
                call(['/bin/rm', html_f])
                html_file.create_page.generate_html(self.path_html, unseen_movies)
                self.browser_reload.reload()

            def remove(self):
                db_seen_movie = self.stored_data.movie_select_one(movie_selected, '0')
                if db_seen_movie:
                    self.removeItem(index)
                    count = self.up_date.insert_movie_file_list.index(movie_selected)
                    self.up_date.insert_movie_file_list.remove(movie_selected)
                    self.up_date.removeItem(count)
                    print("{} must be removed from the .html file and db" .format(movie_selected))
                else:
                    self.removeItem(index)
                    count = self.watch_again.watch_again_list.index(movie_selected)
                    self.watch_again.watch_again_list.remove(movie_selected)
                    self.watch_again.removeItem(count)
                    print("{} must be removed from db" .format(movie_selected))

            def seen(self):
                path = self.stored_data.movie_to_watchagain(movie_selected)
                to_watch = str(path[0]) + '/' + str(path[1])
                call(['/usr/bin/vlc', to_watch])

            option = {"update": update,
                      "remove": remove,
                      "watch_again": seen}

            option[self.to_do](self)
        else:
            # how to ignore this ???
            # QEvent.setAccepted()
            msg.setText('Doing nothing.')

        msg.show()
        msg.exec_()
