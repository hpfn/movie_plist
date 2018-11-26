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
        # self.seen = load_from_json(seen_json_file)
        # self.unseen = load_from_json(unseen_json_file)
        count_spaces = title.count(' ')
        title = title.replace(' ', '_', count_spaces)
        self.cache_poster = MOVIE_PLIST_CACHE + '/' + title + '.png'
        if not self.synopsis_exists():
            self.soup = BeautifulSoup(self._get_html(), 'html.parser')
            self.bs4_synopsis()
            self._do_poster_png_file()

    # def make_poster_name(self):
    #     """
    #     title_year: title and year in your language
    #     """
    #     title = self.soup.title.string[:-7]
    #     count_spaces = title.count(' ')
    #     self.cache_poster = movie_plist_cache + '/' + title.replace(' ', '_', count_spaces) +
    # '.png'

    # def synopsis(self):
    #     """
    #     created by a call to synopsis_exists
    #     in dunder init
    #     """
    #     return self.checked_description

    def synopsis_exists(self):
        all_movies = {**MOVIE_UNSEEN, **MOVIE_SEEN}
        if self.title in all_movies and len(all_movies[self.title]) == 3:
            self.synopsis = all_movies[self.title][1]
            # return True

        return self.synopsis

    def bs4_synopsis(self):
        try:
            description = self.soup.find('meta', property="og:description")
            # self.synopsis = description['content']
            # self.add_synopsis()
        except AttributeError:
            return """
                   Maybe something is wrong with internet connection.
                   Or the imdb .css has changed.
                   A skull and this text, that's it. Try again to confirm.
                   """
        self.synopsis = description['content']
        self.add_synopsis()

    def add_synopsis(self):
        if self.title in MOVIE_UNSEEN:
            self.dict_movie_choice(MOVIE_UNSEEN)
            # dump_json_movie(MOVIE_UNSEEN, UNSEEN_JSON_FILE)
        elif self.title in MOVIE_SEEN:
            self.dict_movie_choice(MOVIE_SEEN)
            # dump_json_movie(MOVIE_SEEN, SEEN_JSON_FILE)

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
        # TODO: save file in .cache/movie_plist - self.movie.title_year
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
            # print(result.group(0))
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
