# -*- coding: utf-8 -*-
import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup
from PyQt5.QtGui import QImage

from _socket import timeout


class ParseImdbData:
    def __init__(self, url):
        """
        receive an url to be
        """
        self._url = url
        self.cache_poster = '/tmp/picture.png'
        self.soup = BeautifulSoup(self._get_html(), 'html.parser')
        self._do_poster_png_file()

    def title_year(self):
        """
        title_year: title and year in your language
        """
        return self.soup.title.string[:-7]

    def synopsis(self):
        """

        """
        try:
            description = self.soup.find('meta', property="og:description")
            return description['content']
        except AttributeError:
            return """
                   Maybe something is wrong with internet connection.
                   Or the imdb .css has changed.
                   A skull and this text, that's it. Try again to confirm.
                   """

    def _do_poster_png_file(self):
        """

        """
        try:
            self._save_poster_file()
        except urllib.error.URLError:
            print("Poster - URLError. Try again.")
        except timeout:
            print("Poster - Connection timeout. Try again.")

    def _save_poster_file(self):
        img = QImage()  # (8,10,4)
        img.loadFromData(self._poster_file())
        # TODO: save file in .cache/movie_plist - self.movie.title_year
        img.save(self.cache_poster)

    def _poster_file(self):
        return urllib.request.urlopen(self._poster_url()).read()

    def _poster_url(self):
        """

        """
        try:
            poster = self.soup.find('div', class_="poster")
            re_poster = re.compile("http.*\.jpg")
            result = re_poster.search(str(poster))
            return result.group(0)
        except AttributeError:
            # tem que retornar uma url
            url_err = 'https://static.significados.com.br/'
            url_err += 'foto/adesivo-caveira-mexicana-caveira-mexicana_th.jpg'
            return url_err

    def _get_html(self):
        """

        """
        try:
            return urllib.request.urlopen(self._url, timeout=3).read()
        except urllib.error.URLError:
            print("HTML - URLError. Try again.")
        except timeout:
            print("HTML - Connection timeout. Try again.")
        except ValueError:
            print("HTML - Please, check the .desktop file for this movie.")

    # def parse_html(self):
    #            self.soup = BeautifulSoup(self.html, 'html.parser')
