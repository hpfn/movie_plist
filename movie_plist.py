#!/usr/bin/python3

import sys
from pathlib import Path
# import time # to see how long a job takes
from PyQt5.QtWidgets import QApplication
# movie_plist stuff
import html_file.create_page
from data.pyscan import PyScan
from info_in_db.movie_plist_sqlite3 import DataStorage
from pyqt_gui.main_gui import Window

def check_pushto_db(url_got, scan):
    """
        if movie info is not in db put data in it
        also call create_page (html) module
    """
    data_to_html = list()
    stored_data = DataStorage()
    movies_stored = stored_data.check_movie()
    # check if the movie info is in movie_plist_sqlite3.db
    # if not, put it in there
    for url, path, movie_file in url_got:
        if url not in movies_stored:
            data_to_html.append(stored_data.insert_data(url, path, movie_file))

    stored_data.exit_from_db()

    html_file.create_page.generate_html(scan, data_to_html)


def main(d_scan):
    # scan the directory
    obtain_url = PyScan(d_scan)
    obtain_url = obtain_url.dir_to_scan()

    # will push data to db if necessary
    # and call create_page.generate_html
    check_pushto_db(obtain_url, d_scan)

    # launch movie_plist
    app = QApplication(sys.argv)
    ex = Window(d_scan)
    sys.exit(app.exec_())

if __name__ == '__main__':
    if len(sys.argv) is 2:
        path_dir_scan = sys.argv[1]
    else:
        path_dir_scan = input(" Do the scan in which directory ? ")

    check_path = Path(path_dir_scan)
    if not check_path.is_dir():
        print(" Please, check the path ")
    else:
        main(path_dir_scan)
