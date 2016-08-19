#!/usr/bin/python3

import sys
from subprocess import call
import urllib
# from bs4 import BeautifulSoup
import pyscan
import pimdbdata
from htmltags import HtmlTags
import pyqt_browser
from movie_plist_sqlite3 import DataStorage


def main(d_scan):
    obtain_url = pyscan.dir_to_scan(d_scan)
    html_page = HtmlTags(d_scan)
    html_page.top_header()
    storaged_data = DataStorage()
    movies_storaged = storaged_data.check_movie()

    # check if the movie is in th db
    # if not, put it in there
    for url, path, moviefile in obtain_url:
        html = urllib.request.urlopen(url).read()
        movie = pimdbdata.ParseImdbData(html)
        if url in movies_storaged:
            print("in db already!")
            continue
        else:
            storaged_data.populate_db(url, path, moviefile, movie)

    # get data from db and close the db
    m_data = storaged_data.show_data()
    storaged_data.exit_from_db()

    # put data in .html file
    for db_info in m_data:
        db_info_list = list(db_info)
        html = urllib.request.urlopen(db_info_list[0]).read()
        movie = pimdbdata.ParseImdbData(html)
        m_poster = movie.movie_poster()
        rate_votes = movie.rate_value_and_votes()
        db_info_list.insert(2, rate_votes)
        html_page.inside_table(m_poster, db_info_list[1:-3], db_info_list[-3], db_info_list[-2])

    html_page.bottom_tags()

    decide_how = input("show html file (Firefox|QWebView): ")
    if decide_how in 'QWebView':
        pyqt_browser.qt_browser(d_scan)  # call('./pyqt_browser.py')
    else:
        file_location = d_scan + '/pymovieinfo.html'
        call(['firefox', file_location])


if __name__ == '__main__':
    if len(sys.argv) is 2:
        path_dir_scan = sys.argv[1]
    else:
        path_dir_scan = input(" Do the scan in which directory ?")

    main(path_dir_scan)
