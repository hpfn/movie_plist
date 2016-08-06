import re
import urllib
from bs4 import BeautifulSoup
import pyscan
import pimdbdata
import htmltags

obtain_url = pyscan.dir_to_scan()
htmltags.top_header()
for url, path in obtain_url:
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
    htmltags.inside_table(m_poster, m_data, path)

htmltags.bottom_tags()
