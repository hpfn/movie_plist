#!/usr/bin/python3
# -*-coding-utf8-*
import sys, json
from PyQt5.QtWidgets import QApplication
from conf.global_conf import internet_on, get_dir_path, seen_json_file, unseen_json_file
from data.pyscan import create_dicts
from pyqt_gui.main_window import Window


def main(d_scan):
    movie_seen, movie_unseen = create_dicts(d_scan)
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
    main(path_dir_scan)
    # else:
    #     print(" Please, check your internet connection. ")
