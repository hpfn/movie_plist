#!/usr/bin/python3
# -*-coding-utf8-*
import sys
import urllib.request
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from conf.global_conf import internet_on
from conf.global_conf import cfg_file, read_path, write_path
from data import pimdbdata
from data.pyscan import dir_to_scan
from info_in_db.movie_plist_sqlite3 import DataStorage
from pyqt_gui.main_window import Window


def create_dicts(s_dir):
    """
    
    """
    movie_seen = dict()
    movie_unseen = dict()
    stored_data = DataStorage()
    movies_stored = str(stored_data.movie_url())
    # check if the movie info is in movie_plist_sqlite3.db
    # if yes goes to movie_seen dict
    # if not goes to movie_unseen dict
    # dict's key is title_year of the movie
    for i in dir_to_scan(s_dir):
        # print(i)
        html = urllib.request.urlopen(i[0]).read()
        movie = pimdbdata.ParseImdbData(html)
        title = movie.title_year()
        # print(movies_stored)
        if i[0] in movies_stored:
            movie_seen[title] = i
        else:
            movie_unseen[title] = i

    stored_data.exit_from_db()

    return movie_seen, movie_unseen


def main(d_scan):
    # seen movies now are all_movies
    all_movies, movie_unseen = create_dicts(d_scan)
    # create two lists from dicts
    seen_list = [s for s in all_movies.keys()]
    unseen_list = [us for us in movie_unseen.keys()]
    # merge dicts and clean unseen - probably smaller
    all_movies.update(movie_unseen)
    movie_unseen.clear()  # = {}

    # launch movie_plist
    app = QApplication(sys.argv)
    ex = Window(seen_list, unseen_list, all_movies)
    sys.exit(app.exec_())


if __name__ == '__main__':
    # net_status = internet_on()
    if internet_on() == 200:
        check_path = Path(cfg_file)
        if check_path.is_file():
            path_dir_scan = read_path()
        else:
            path_dir_scan = input(" Do the scan in which directory ? ")
            path_dir_scan = write_path(path_dir_scan)

        main(path_dir_scan)
    else:
        print(" Please, check your internet connection. ")
