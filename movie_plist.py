#!/usr/bin/python3
# -*-coding-utf8-*
import sys, os
from pathlib import Path
from subprocess import Popen
# import urllib3
# import time # to see how long a job takes
from PyQt5.QtWidgets import QApplication
# movie_plist stuff
from conf.global_conf import movie_plist_stuff_html_dir as html_dir
from conf.global_conf import internet_on
import html_file.create_page
from data.pyscan import PyScan
from info_in_db.movie_plist_sqlite3 import DataStorage
from pyqt_gui.main_gui import Window


def check_pushto_db(url_got, p_html):
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

    html_file.create_page.generate_html(p_html, data_to_html)


def main(d_scan):
    # scan the directory
    obtain_url = PyScan(d_scan)
    obtain_url = obtain_url.dir_to_scan()

    # will push data to db if necessary
    # and call create_page.generate_html
    dir_to_html = html_dir + '/index.html'
    check_pushto_db(obtain_url, dir_to_html)

    # start a cgi http server
    # after change directory
    cgi_server = html_dir + '/simple_httpd.py'
    dir_now = os.path.join(os.path.dirname(__file__))
    run_at = os.path.join(html_dir)
    os.chdir(run_at)
    run_cgi = ['/usr/bin/python3', cgi_server]
    proc = Popen(run_cgi)
    os.chdir(dir_now)

    # launch movie_plist
    app = QApplication(sys.argv)
    ex = Window(dir_to_html)
    sys.exit([app.exec_(), proc.terminate()])

if __name__ == '__main__':
    net_status = internet_on()
    if net_status == 200:
        print('Internet Connection: ok - {}' .format(net_status))
        # if len(sys.argv) is 2:
        #    path_dir_scan = sys.argv[1]
        #else:

        path_dir_scan = input(" Do the scan in which directory ? ")

        check_path = Path(path_dir_scan)
        if not check_path.is_dir():
            print(" Please, check the path ")
        else:
            main(path_dir_scan)
