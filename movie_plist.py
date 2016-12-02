#!/usr/bin/python3

import sys, os
from pathlib import Path
from subprocess import Popen
import urllib3
# import time # to see how long a job takes
from PyQt5.QtWidgets import QApplication
# movie_plist stuff
import html_file.create_page
from data.pyscan import PyScan
from info_in_db.movie_plist_sqlite3 import DataStorage
from pyqt_gui.main_gui import Window

def internet_on():
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.imdb.com', retries=False, timeout=3.0)
        return r.status
    except urllib3.exceptions.NewConnectionError:
        print('No Internet Connection ! Or IMDB has a problem...')
        print('No poster')
        print('If the .html file must be re-created, no rate/votes')
        print('If there is a new movie, no data will be retrieve')
        print('and movie_plist will crash, probably')
        return False

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
    dir_to_html = d_scan + '/pymovieinfo.html'
    check_pushto_db(obtain_url, dir_to_html)

    # This is a fake implementation to test a cgi script to
    # mark as seen a movie on db. Needs a httpd.
    # But how to run the server on a specific location ?
    # every ugly this manner. The simple_httpd script call
    # os.chdir(), but from there it does not work as expected
    cgi_server = d_scan + '/simple_httpd.py'
    dir_now = os.path.join(os.path.dirname(__file__))
    run_at = os.path.join(d_scan)
    os.chdir(run_at)
    run_cgi = ['/usr/bin/python3', cgi_server]
    proc = Popen(run_cgi)
    os.chdir(dir_now)

    # launch movie_plist
    app = QApplication(sys.argv)
    ex = Window(dir_to_html)
    sys.exit([app.exec_(), proc.terminate()])
    #sys.exit(app.exec_())

if __name__ == '__main__':
    net_status = internet_on()
    if net_status:
        print('Internet Connection: ok - {}' .format(net_status))
    if len(sys.argv) is 2:
        path_dir_scan = sys.argv[1]
    else:
        path_dir_scan = input(" Do the scan in which directory ? ")

    check_path = Path(path_dir_scan)
    if not check_path.is_dir():
        print(" Please, check the path ")
    else:
        main(path_dir_scan)
