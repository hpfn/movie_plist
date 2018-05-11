# -*- coding: utf-8 -*-
import re
import urllib.request
import urllib.error
from _socket import timeout
from PyQt5.QtGui import QImage
from bs4 import BeautifulSoup


class ParseImdbData:
    def __init__(self, url):
        """
        receive an url to be
        """
        # self.url = url
        html_page = self._get_html(url)
        self.soup = BeautifulSoup(html_page, 'html.parser')
        self._do_poster_png_file()

    def title_year(self):
        """
        title_year: title and year in your language
        """
        return self.soup.title.string[:-7]

    def synopsis(self):
        """
        obs: tem um conserto no azak.
        """
        description = self.soup.find(itemprop="description")
        raw_txt = description.get_text()
        return raw_txt

    def _do_poster_png_file(self):
        """
        obs: tem um conserto no azak
        """
        try:
            poster = self._movie_poster()
            data = urllib.request.urlopen(poster).read()
            self._save_poster_file(data)
        except urllib.error.URLError:
            print("Poster - URLError. Try again.")
        except timeout:
            print("Poster - Connection timeout. Try again.")

    def _movie_poster(self):
        """
        obs: tem um conserto no azak
        """
        poster = self.soup.find(itemprop="image")
        re_poster = re.compile("http.*\.jpg")
        result = re_poster.search(str(poster))
        return result.group(0)

    @staticmethod
    def _save_poster_file(data):
        img = QImage()  # (8,10,4)
        img.loadFromData(data)
        # TODO: save file in .cache/movie_plist - self.movie.title_year
        img.save('/tmp/picture.png')

    def _get_html(self, url):
        """
        obs: tem um conserto no azak
        """
        try:
            return urllib.request.urlopen(url, timeout=3).read()
        except urllib.error.URLError:
            self.context = "HTML - URLError. Try again."
        except timeout:
            self.context = "HTML - Connection timeout. Try again."
        except ValueError:
            self.context = "HTML - Please, check the .desktop file for this movie."

    # def parse_html(self):
    #            self.soup = BeautifulSoup(self.html, 'html.parser')
