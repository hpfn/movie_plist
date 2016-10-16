#!/usr/bin/python3

import sys

from PyQt5.QtWidgets import QApplication

import pyscan
from info_in_db.movie_plist_sqlite3 import DataStorage
from pyqt_gui.htmltags import HtmlTags
from pyqt_gui.main_gui import Window


def main(d_scan):
    obtain_url = pyscan.dir_to_scan(d_scan)
    html_page = HtmlTags(d_scan)
    html_page.top_header()
    stored_data = DataStorage()
    movies_stored = stored_data.check_movie()

    # check if the movie is in th db
    # if not, put it in there
    for url, path, moviefile in obtain_url:
        if url not in movies_stored:
            stored_data.insert_data(url, path, moviefile)

    # get data from db and close the db
    m_data = stored_data.show_data()
    stored_data.exit_from_db()
    # send data to the table in the .html file
    html_page.parse_data_to_inside_table(m_data)
    # final html tags
    html_page.bottom_tags()

    # decide_how = input("show html file (Firefox|PyQt): ")
    # if decide_how in 'PyQt':
    # pyqt_browser.qt_browser(d_scan)
    app = QApplication(sys.argv)
    ex = Window(d_scan)
    sys.exit(app.exec_())
    # else:
    #    file_location = d_scan + '/pymovieinfo.html'
    #    call(['firefox', file_location])


if __name__ == '__main__':
    if len(sys.argv) is 2:
        path_dir_scan = sys.argv[1]
    else:
        path_dir_scan = input(" Do the scan in which directory ? ")

    main(path_dir_scan)
