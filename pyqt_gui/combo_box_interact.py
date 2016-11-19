# from PyQt5.QtWidgets import QComboBox
from info_in_db.movie_plist_sqlite3 import DataStorage
from data.pyscan import PyScan
from html_file import create_page, remove_movie

from subprocess import call

class InteractBox():
    """ remove item and update combo box list """
    def __init__(self, movie_choice):
        # self.index = index_number
        self.movie_selected = movie_choice
        self.stored_data = DataStorage()

    def insert_movie_file_action(self, html_path, browser):
        """
            use self.index to update combo box list
            recreate the .html file with a new movie file
            reload the page
        """
        p_file = self.stored_data.movie_path(self.movie_selected)
        # scan selected movie dir
        scan_dir = PyScan(p_file[0])
        scan_dir = scan_dir.dir_to_scan()
        # file name
        file_n = scan_dir[0][2]
        self.stored_data.update_movie_file(file_n, self.movie_selected)
        # update list
        # Regrex edit .html file ? re-create by now. First get the movies
        # then rm the html file and re-create.
        # This can be better
        unseen_movies = self.stored_data.movie_unseen()
        # html_f = html_path
        call(['/bin/rm', html_path])
        create_page.generate_html(html_path, unseen_movies)
        browser.reload()

    def movie_remove(self, update, watch, browser):
        """
            remove a movie on combo box list
            and  on db.
            from the hd too ?
        """
        db_seen_movie = self.stored_data.movie_select_one(self.movie_selected, '0')
        if db_seen_movie:
            if self.movie_selected in update.insert_movie_file_list:
                count = update.insert_movie_file_list.index(self.movie_selected)
                update.insert_movie_file_list.remove(self.movie_selected)
                update.removeItem(count)
            remove_movie.EditHtml(self.movie_selected)
            browser.reload()
            print("{} must be removed from the .html file".format(self.movie_selected))
        else:
            count = watch.watch_again_list.index(self.movie_selected)
            watch.watch_again_list.remove(self.movie_selected)
            watch.removeItem(count)
            print("{} must be removed from hb".format(self.movie_selected))

        self.stored_data.movie_delete(self.movie_selected)

    def watch_movie(self):
        """
            call vlc to watch a movie
        """
        path = self.stored_data.movie_to_watchagain(self.movie_selected)
        to_watch = str(path[0]) + '/' + str(path[1])
        call(['/usr/bin/vlc', to_watch])

