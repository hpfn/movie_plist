#!/usr/bin/python3

import  sys
from subprocess import call
import urllib
# from bs4 import BeautifulSoup
import pyscan
import pimdbdata
from htmltags import HtmlTags
import pyqt_browser
from movie_plist_sqlite3 import DataStorage

def main(d_scan):
    # d_scan = "/home/zaza/Vídeos/"
    obtain_url = pyscan.dir_to_scan(d_scan)
    html_page = HtmlTags(d_scan)
    html_page.top_header()
    storaged_data = DataStorage()
    movies_storaged = storaged_data.check_movie()
    print(movies_storaged)
    #/homequit(0)

    for url, path, moviefile in obtain_url:
        # m_data = list()
        html = urllib.request.urlopen(url).read()
        if url in movies_storaged:
            continue
        else:
            movie = pimdbdata.ParseImdbData(html)

            # m_poster is not going to database !!!
            m_poster = movie.movie_poster()
            title_year = movie.title_year()
            # rate_votes does not go to database !!!
            rate_votes = movie.rate_value_and_votes()
            director = movie.director()
            writers_list = movie.creator_writers()
            actors_list = movie.actors()
            snps_txt = movie.synopsis()

            # for i in [title_year, rate_votes, director, writers_list, actors_list, snps_txt]:
            #    m_data.append(i)
            m_data = [url, title_year, director]
            wrt_str = ""
            for w in writers_list:
                wrt_str = wrt_str + w + " "
            m_data.append(wrt_str)
            actr_str = ""
            for a in actors_list:
                actr_str = actr_str + a + " "
            m_data.append(actr_str)
            m_data.append(snps_txt)
            m_data.append(0)
            # print(m_data)
            storaged_data.insert_data(m_data)

    storaged_data.show_data()
    storaged_data.exit_from_db()

    quit(0)

    # html_page.inside_table(m_poster, m_data, path, moviefile)

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
        path_dir_scan = input(" Do the scan which directory ?")

    main(path_dir_scan)
