#!/usr/bin/python3
# -*-coding-utf8-*
import sys, json
from PyQt5.QtWidgets import QApplication
from conf.global_conf import internet_on, get_dir_path, json_file
from data.pyscan import create_dicts
from pyqt_gui.main_window import Window


def main(d_scan):
    # seen movies now are all_movies
    movie_seen, movie_unseen = create_dicts(d_scan)
    # create two lists from dicts
    # seen_list = sorted(movie_seen.keys())
    # unseen_list = sorted(movie_unseen.keys())
    # merge dicts and clean unseen - probably smaller
    # all_movies = {}
    # all_movies.update(movie_unseen)
    # all_movies.update(movie_seen)
    # movie_unseen.clear()  # = {}

    # launch movie_plist
    app = QApplication(sys.argv)
    ex = Window(movie_seen, movie_unseen)
    
    def json_seen_m(movie_dic):
        #unseen_l = set(u_l)
        # seen_dict = {key: list_items
        #             for key, list_items in movie_dic.items()
        #             if not key in u_l}
        with open(json_file, 'w') as outfile:
            json.dump(movie_dic, outfile)

    sys.exit([app.exec_(), json_seen_m(movie_seen)])


if __name__ == '__main__':
    if internet_on() == 200:
        path_dir_scan = get_dir_path()
        main(path_dir_scan)
    else:
        print(" Please, check your internet connection. ")
