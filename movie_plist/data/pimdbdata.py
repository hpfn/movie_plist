# -*- coding: utf-8 -*-
import os
import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup
from PyQt5.QtGui import QImage

from _socket import timeout
from movie_plist.conf.global_conf import (
    movie_plist_cache, movie_seen, movie_unseen
)


class ParseImdbData:
    def __init__(self, url, title):
        """
        receive an url to be
        """
        self._url = url
        self.title = title
        self.checked_description = ''
        # self.seen = load_from_json(seen_json_file)
        # self.unseen = load_from_json(unseen_json_file)
        count_spaces = title.count(' ')
        title = title.replace(' ', '_', count_spaces)
        self.cache_poster = movie_plist_cache + '/' + title + '.png'
        if not self.synopsis_exists():
            self.soup = BeautifulSoup(self._get_html(), 'html.parser')
        # self.make_poster_name()
        self._do_poster_png_file()

    # def make_poster_name(self):
    #     """
    #     title_year: title and year in your language
    #     """
    #     title = self.soup.title.string[:-7]
    #     count_spaces = title.count(' ')
    #     self.cache_poster = movie_plist_cache + '/' + title.replace(' ', '_', count_spaces) +
    # '.png'

    def synopsis(self):
        """

        """
        try:
            if self.synopsis_exists():
                return self.checked_description
            description = self.soup.find('meta', property="og:description")
            description_content = description['content']

            self.add_synopsis(description_content)

            return description_content
        except AttributeError:
            return """
                   Maybe something is wrong with internet connection.
                   Or the imdb .css has changed.
                   A skull and this text, that's it. Try again to confirm.
                   """

    def synopsis_exists(self):
        all_movies = {**movie_unseen, **movie_seen}
        if self.title in all_movies and len(all_movies[self.title]) == 3:
            self.checked_description = all_movies[self.title][1]
            return True

    def add_synopsis(self, new_info):
        if self.title in movie_unseen:
            movie_info = list(movie_unseen[self.title])
            movie_info.insert(1, new_info)
            movie_unseen[self.title] = tuple(movie_info)
            print(movie_unseen[self.title])
        elif self.title in movie_seen:
            movie_info = list(movie_seen[self.title])
            movie_info.insert(1, new_info)
            movie_seen[self.title] = tuple(movie_info)
            print(movie_seen[self.title])

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
