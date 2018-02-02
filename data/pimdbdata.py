# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re


class ParseImdbData(object):
    def __init__(self, html):
        """ html is the url to be parsed """
        self.soup = BeautifulSoup(html, 'html.parser')

    def title_year(self):
        """
        title_year: title and year in your language
        """
        return self.soup.title.string[:-7]

    def movie_poster(self):
        poster = self.soup.find(itemprop="image")
        re_poster = re.compile("http.*\.jpg")
        result = re_poster.search(str(poster))
        return result.group(0)

    def synopsis(self):
        description = self.soup.find(itemprop="description")
        raw_txt = description.get_text()
        return raw_txt

