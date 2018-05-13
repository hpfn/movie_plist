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
        self._url = url
        self.soup = BeautifulSoup(self._get_html(), 'html.parser')
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
        try:
            description = self.soup.find(itemprop="description")
            return description.get_text()
        except AttributeError:
            return """
                   Maybe something is wrong with internet connection.
                   If the poster is a skull, that's it. Just try again.
                   """

    def _do_poster_png_file(self):
        """
        obs: tem um conserto no azak
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
        img.save('/tmp/picture.png')

    def _poster_file(self):
        return urllib.request.urlopen(self._poster_url()).read()

    def _poster_url(self):
        """

        """
        try:
            poster = self.soup.find(itemprop="image")
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
        obs: tem um conserto no azak
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
