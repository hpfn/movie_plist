#!/usr/bin/python3
# -*-coding-utf8-*
import sys

from PyQt5.QtWidgets import QApplication

from movie_plist.conf.global_conf import (
    MOVIE_SEEN, MOVIE_UNSEEN, SEEN_JSON_FILE, UNSEEN_JSON_FILE,
    check_movie_plist_dirs, dump_json_movie, get_dir_path, scan_dir_has_movies
)
from movie_plist.data.pyscan import create_dicts
from movie_plist.pyqt_gui.main_window import Window


def main(d_scan):
    # c_d = create_dicts(d_scan)
    create_dicts(d_scan)
    # movie_seen, movie_unseen = MOVIE_SEEN, MOVIE_UNSEEN  # create_dicts(d_scan)
    app = QApplication(sys.argv)
    ex = Window()  # noqa: F841

    # def w_json_movie_file(movie_dic, json_file):
    #    with open(json_file, 'w') as outfile:
    #        json.dump(movie_dic, outfile)

    exit_task = [
        app.exec_(),
        dump_json_movie(MOVIE_UNSEEN, UNSEEN_JSON_FILE),
        dump_json_movie(MOVIE_SEEN, SEEN_JSON_FILE),
    ]
    sys.exit(exit_task)


if __name__ == '__main__':
    # if internet_on() == 200:
    check_movie_plist_dirs()
    path_dir_scan = get_dir_path()
    scan_dir_has_movies(path_dir_scan)
    main(path_dir_scan)
    # else:
    #     print(" Please, check your internet connection. ")
