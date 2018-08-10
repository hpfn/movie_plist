#!/usr/bin/python3

import json
import os
import re
import time

from movie_plist.conf.global_conf import seen_json_file, unseen_json_file


class CreateDict:
    def __init__(self, scan_dir):
        self._scan_dir = scan_dir
        self._json_movies = ''
        self._file_with_url = ''

    def create_dicts(self):
        """
        # get seen movies from json file
        # get unseen movies from on json file
        # check for new moview
        # if no unseen movies ask if continue
        # return seen and unseen movies
        """
        start = time.time()
        with open(seen_json_file) as json_data:
            movie_seen = json.load(json_data)

        with open(unseen_json_file) as u_json_data:
            movie_unseen = json.load(u_json_data)

        movies_path = set(m_path for _, m_path in movie_seen.values())
        umovies_path = set(um_path for _, um_path in movie_unseen.values())
        self._json_movies = set.union(movies_path, umovies_path)

        movie_unseen_to_add = {dir_name: i for dir_name, i in self._new_data()}
        movie_unseen.update(movie_unseen_to_add)

        end = time.time()
        print(end - start)

        return movie_seen, movie_unseen

    def _new_data(self):
        """ return title_year, imdb_url and path to movie """
        for root, file_n in self._new_desktop_f():
            self.file_with_url = os.path.join(root, file_n)
            imdb_url = self._open_right_file()
            yield root.rpartition('/')[-1], (imdb_url, root)

    def _new_desktop_f(self):
        """ search for a .desktop file in a directory """
        return ((root, file_n)
                for root, filename in self._unknow_dirs()
                for file_n in filename
                if file_n.endswith('.desktop'))

    def _unknow_dirs(self):
        """ root (path) that are not in json files """
        return ((root, filename)
                for root, _, filename in os.walk(self._scan_dir)
                if not {root}.issubset(self._json_movies))

    def _open_right_file(self):
        """ open the right file and get the url"""
        with open(self.file_with_url, 'r') as check_content:
            file_lines = check_content.readlines()

        url = re.search(r"(URL|url)=https?://.*", ' '.join(file_lines))

        if url:
            return url.group(0)[4:]
