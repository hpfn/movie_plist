#!/usr/bin/python3
# -*-coding-utf8-*
import sys
import json
from PyQt5.QtWidgets import QApplication
from conf.global_conf import (
    internet_on, get_dir_path, seen_json_file, unseen_json_file,
    scan_dir_has_movies)
from data.pyscan import CreateDict
from pyqt_gui.main_window import Window


def main(d_scan):
    c_d = CreateDict(d_scan)
    movie_seen, movie_unseen = c_d.create_dicts()
    app = QApplication(sys.argv)
    ex = Window(movie_seen, movie_unseen)
    
    def w_json_movie_file(movie_dic, json_file):
        with open(json_file, 'w') as outfile:
            json.dump(movie_dic, outfile)

    exit_task = [
        app.exec_(),
        w_json_movie_file(movie_unseen, unseen_json_file),
        w_json_movie_file(movie_seen, seen_json_file),
    ]
    sys.exit(exit_task)


if __name__ == '__main__':
    # if internet_on() == 200:
    path_dir_scan = get_dir_path()
    scan_dir_has_movies(path_dir_scan)
    main(path_dir_scan)
    # else:
    #     print(" Please, check your internet connection. ")
