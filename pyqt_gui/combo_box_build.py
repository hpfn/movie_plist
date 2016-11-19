from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
# from PyQt5.QtCore import QEvent
from info_in_db.movie_plist_sqlite3 import DataStorage

from subprocess import call

from data.pyscan import PyScan
from .combo_box_interact import InteractBox
import html_file.create_page


class Combo(QComboBox):
    def __init__(self, will_do, update_object=None, seen_object=None, scanlocal_htmlf=None, browser_obj=None):
        super().__init__()
        self.to_do = will_do
        self.path_html = scanlocal_htmlf
        self.watch_again = seen_object
        self.watch_again_list = None
        self.up_date = update_object
        self.insert_movie_file_list = None
        self.browser_reload = browser_obj
        self.stored_data = DataStorage()
        self.movies_stored = ""

        self.first_item_combo()
        self.combo_list()

    def first_item_combo(self):
        def update():
            self.addItem("insert movie file ")
            self.insert_movie_file_list = ['insert movie file']

        def remove():
            self.addItem("remove movie from db")

        def seen():
            self.addItem("seen movies")
            self.watch_again_list = ['seen movies']

        option = {"update": update,
                  "remove": remove,
                  "watch_again": seen}
        option[self.to_do]()

    def combo_list(self):
        def update():
            self.movies_stored = self.stored_data.no_movie_yet()
            # doing this here make update in confirm_option
            # method easier to read
            for i in self.movies_stored:
                self.insert_movie_file_list.append(i[0])

        def remove():
            self.movies_stored = self.stored_data.movie_title_list()

        def seen():
            self.movies_stored = self.stored_data.movie_seen()
            # doing this here make remove() in confirm_option
            # method easier to read
            for i in self.movies_stored:
                self.watch_again_list.append(i[0])

        option = {"update": update,
                  "remove": remove,
                  "watch_again": seen}

        option[self.to_do]()
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
            msg.setText('remove this window!!!')

            def update():
                update_list_html = InteractBox(index, movie_selected)
                update_list_html.insert_movie_file_list()
                # self.insert_movie_file_action(index, movie_selected)

            def remove():
                remove_item = InteractBox(index, movie_selected)
                remove_item.movie_remove(self.up_date, self.watch_again)
                self.removeItem(index)
                # self.movie_remove(index, movie_selected)

            def seen():
                watch_movie = InteractBox(movie_selected)
                watch_movie.watch_movie()
                # self.watch_movie(movie_selected)

            option = {"update": update,
                      "remove": remove,
                      "watch_again": seen}

            option[self.to_do]()
        else:
            # how to ignore this ???
            # QEvent.setAccepted()
            msg.setText('Doing nothing.')

        msg.show()
        msg.exec_()

    def insert_movie_file_action(self, i, m):
        """
            :param i: index
            :param m: movie_selected
            :return: nothing
        """
        p_file = self.stored_data.movie_path(m)
        # scan selected movie dir
        scan_dir = PyScan(p_file[0])
        scan_dir = scan_dir.dir_to_scan()
        # file name
        file_n = scan_dir[0][2]
        self.stored_data.update_movie_file(file_n, m)
        # update list
        self.removeItem(i)
        # Regrex edit .html file ? re-create by now. First get the movies
        # then rm the html file and re-create.
        # This can be better
        unseen_movies = self.stored_data.movie_unseen()
        html_f = self.path_html
        print(html_f)
        call(['/bin/rm', html_f])
        html_file.create_page.generate_html(self.path_html, unseen_movies)
        self.browser_reload.reload()

    def movie_remove(self, i, m):
        """
            :param i: index
            :param m: movie_selected
            :return: nothing
        """
        db_seen_movie = self.stored_data.movie_select_one(m, '0')
        if db_seen_movie:
            self.removeItem(i)
            count = self.up_date.insert_movie_file_list.index(m)
            self.up_date.insert_movie_file_list.remove(m)
            self.up_date.removeItem(count)
            print("{} must be removed from the .html file and db".format(m))
        else:
            self.removeItem(i)
            count = self.watch_again.watch_again_list.index(m)
            self.watch_again.watch_again_list.remove(m)
            self.watch_again.removeItem(count)
            print("{} must be removed from db".format(m))

    def watch_movie(self, m):
        """
            :param m: movie_selected
            :return: nothing
        """
        path = self.stored_data.movie_to_watchagain(m)
        to_watch = str(path[0]) + '/' + str(path[1])
        call(['/usr/bin/vlc', to_watch])
