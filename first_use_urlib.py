import re
import urllib
from bs4 import BeautifulSoup
import pyscan
import pimdbdata
from htmltags import HtmlTags

obtain_url = pyscan.dir_to_scan()
html_page = HtmlTags()
html_page.top_header()
for url, path, moviefile in obtain_url:
    m_data = list()
    html = urllib.request.urlopen(url).read()
    movie = pimdbdata.ParseImdbData(html)

    m_poster = movie.movie_poster()

    title_year = movie.title_year()
    rate_votes = movie.rate_value_and_votes()
    director = movie.director()
    writers_list = movie.creator_writers()
    actors_list = movie.actors()
    snps_txt =movie.synopsis()
    # path = 'file://' + path

    for i in [title_year, rate_votes, director, writers_list, actors_list, snps_txt]:
        m_data.append(i)
    html_page.inside_table(m_poster, m_data, path, moviefile)

html_page.bottom_tags()
