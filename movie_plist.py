#!/usr/bin/python3
# -*-coding-utf8-*
import sys

from PyQt5.QtWidgets import QApplication

from movie_plist.conf.global_conf import (
    SEEN_JSON_FILE, UNSEEN_JSON_FILE, check_movie_plist_dirs, dump_json_movie,
    get_dir_path, scan_dir_has_movies
)
from movie_plist.data.pyscan import CreateDict
from movie_plist.pyqt_gui.main_window import Window


def main(d_scan):
    c_d = CreateDict(d_scan)
    movie_seen, movie_unseen = c_d.create_dicts()
    app = QApplication(sys.argv)
    ex = Window(movie_seen, movie_unseen)  # noqa: F841

    # def w_json_movie_file(movie_dic, json_file):
    #    with open(json_file, 'w') as outfile:
    #        json.dump(movie_dic, outfile)

    exit_task = [
        app.exec_(),
        dump_json_movie(movie_unseen, UNSEEN_JSON_FILE),
        dump_json_movie(movie_seen, SEEN_JSON_FILE),
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
