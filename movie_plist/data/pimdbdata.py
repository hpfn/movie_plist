# -*- coding: utf-8 -*-
import os
import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup
from PyQt5.QtGui import QImage  # pylint: disable-msg=E0611

from _socket import timeout
from movie_plist.conf.global_conf import (
    MOVIE_PLIST_CACHE, MOVIE_SEEN, MOVIE_UNSEEN
)


class ParseImdbData:
    def __init__(self, url, title):
        """
        receive an url to be
        """
        self._url = url
        self.title = title
        self.synopsis = ''
        self.cache_poster = self.make_poster_name()
        if not self.synopsis_exists():
            # Maybe put these in other class
            self.soup = BeautifulSoup(self._get_html(), 'html.parser')
            self.bs4_synopsis()
            self._do_poster_png_file()

    def make_poster_name(self):
        """

        """
        count_spaces = self.title.count(' ')
        cache_name = self.title.replace(' ', '_', count_spaces)
        return MOVIE_PLIST_CACHE + '/' + cache_name + '.png'

    def synopsis_exists(self):
        all_movies = {**MOVIE_UNSEEN, **MOVIE_SEEN}
        if self.title in all_movies and len(all_movies[self.title]) == 3:
            self.synopsis = all_movies[self.title][1]

        return self.synopsis

    def bs4_synopsis(self):
        try:
            description = self.soup.find('meta', property="og:description")
            self.synopsis = description['content']
            self.add_synopsis()
        except AttributeError:
            self.synopsis = """
                   Maybe something is wrong with internet connection.
                   Or the imdb .css has changed.
                   A skull and this text, that's it. Try again to confirm.
                   """

    def add_synopsis(self):
        if self.title in MOVIE_UNSEEN:
            self.dict_movie_choice(MOVIE_UNSEEN)
        elif self.title in MOVIE_SEEN:
            self.dict_movie_choice(MOVIE_SEEN)

    def dict_movie_choice(self, d_movie):
        movie_info = list(d_movie[self.title])
        movie_info.insert(1, self.synopsis)
        d_movie[self.title] = tuple(movie_info)

    def _do_poster_png_file(self):
        """

        """
        try:
            if not os.path.isfile(self.cache_poster):
                self._save_poster_file()
        except urllib.error.URLError:
            print("Poster - URLError. Try again.")
        except timeout:
            print("Poster - Connection timeout. Try again.")

    def _save_poster_file(self):
        img = QImage()  # (8,10,4)
        img.loadFromData(self._poster_file())
        img.save(self.cache_poster)

    def _poster_file(self):
        return urllib.request.urlopen(self._poster_url()).read()

    def _poster_url(self):
        """

        """
        try:
            poster = self.soup.find('div', class_="poster")
            re_poster = re.compile(r'\bhttp\S+jpg\b')
            result = re_poster.search(str(poster))
            return result.group(0)
        except AttributeError:
            # tem que retornar uma url
            # arquivo local
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
