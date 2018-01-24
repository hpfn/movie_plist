#!/usr/bin/python3
# -*-coding-utf8-*
import sys, json
from PyQt5.QtWidgets import QApplication
from conf.global_conf import internet_on, get_dir_path
from data.pyscan import create_dicts
from pyqt_gui.main_window import Window


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
    
    def json_seen_m(movie_dic, u_l):
        seen_dict = {key: list_items for key, list_items in movie_dic.items() if key not in set(u_l)}
        with open('seen_movies.json', 'w') as outfile:
            json.dump(seen_dict, outfile)

    sys.exit([app.exec_(), json_seen_m(all_movies, unseen_list)])


if __name__ == '__main__':
    if internet_on() == 200:
        path_dir_scan = get_dir_path()
        main(path_dir_scan)
    else:
        print(" Please, check your internet connection. ")
