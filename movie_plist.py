#!/usr/bin/python3
# -*-coding-utf8-*
import sys
import urllib.request
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from conf.global_conf import internet_on, cfg_file
from data import pimdbdata
from data.pyscan import dir_to_scan
from info_in_db.movie_plist_sqlite3 import DataStorage
from pyqt_gui.new_movie_plist import Window


def create_dicts(s_dir):
    """
    
    """
    movie_seen = dict()
    movie_unseen = dict()
    stored_data = DataStorage()
    movies_stored = str(stored_data.movie_url())
    # check if the movie info is in movie_plist_sqlite3.db
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
    # will check data in db and create dict - two
    # seen movies now are all_movies
    all_movies, unseen_movies = create_dicts(d_scan)
    # send the two dicts to new_movie_plist.py file. A class
    seen_list = [s for s in all_movies.keys()]
    unseen_list = [us for us in unseen_movies.keys()]
    all_movies.update(unseen_movies)
    # .clear() ?
    # movie_seen = {}

    # print(seen_list)
    # print(unseen_list)
    # print(movie_seen)
    # print(movie_unseen)

    # launch movie_plist
    app = QApplication(sys.argv)
    ex = Window(seen_list, unseen_list, all_movies)
    sys.exit(app.exec_())


if __name__ == '__main__':
    net_status = internet_on()
    if net_status == 200:
        print('Internet Connection: ok - {}'.format(net_status))
        # if len(sys.argv) is 2:
        #    path_dir_scan = sys.argv[1]
        # else:
        check_path = Path(cfg_file)
        if check_path.is_file():
            print("Arquivo existe. Pular pergunta.")
        else:
            path_dir_scan = input(" Do the scan in which directory ? ")

        check_path = Path(path_dir_scan)
        if not check_path.is_dir():
            print(" Please, check the path ")
        else:
            print("The path will be saved.")
            main(path_dir_scan)
