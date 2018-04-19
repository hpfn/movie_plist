#!/usr/bin/python3

import os
import re
import sys
import json
import time
# from PyQt5.QtWidgets import QMessageBox, QApplication
from conf.global_conf import seen_json_file, unseen_json_file


class CreateDict:
    def __init__(self, scan_dir):
        self._scan_dir = scan_dir
        self._json_movies = ''
        self._file_with_url = ''

    def create_dicts(self):
        """
        # get seen movies from json file
        # build unseen movies based on json file
        # if no unseen movies ask if continue
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

        if not movie_unseen:
            self._empty_unseen_dict()

        end = time.time()
        print(end - start)

        return movie_seen, movie_unseen

    def _new_data(self):
        for root, file_n in self._new_desktop_f():
            self.file_with_url = os.path.join(root, file_n)
            imdb_url = self._open_right_file()
            yield root.rpartition('/')[-1], (imdb_url, root)

    def _new_desktop_f(self):
        return ((root, file_n)
                for root, filename in self._unknow_dirs()
                for file_n in filename
                if file_n.endswith('.desktop'))

    def _unknow_dirs(self):
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

    @staticmethod
    def _empty_unseen_dict():
        from PyQt5.QtWidgets import QMessageBox, QApplication
        app = QApplication(['0'])
        msg = QMessageBox()
        button_reply = msg.question(
            msg,
            'No unseen movies.',
            'Maybe a good tip is to check the scan dir. Continue anyway?',
            QMessageBox.Yes | QMessageBox.No
        )

        if button_reply == QMessageBox.No:
            sys.exit('1')


# def dir_to_scan(scan_dir, seen_movies):
#     """
#     find .desktop file  to get imdb url
#
#     yield:
#       imdb_url: to get poster and synopsis
#       root will go to QTab-QTree
#       named_dir is title_year (user mkdir name)
#     """
#     new_dirs = ((root, filename)
#                 for root, _, filename in os.walk(scan_dir)
#                 if not {root}.issubset(seen_movies))
#
#     new_desktop_f = ((root, file_n)
#                      for root, filename in new_dirs
#                      for file_n in filename
#                      if file_n.endswith('.desktop'))
#
#     for root, file_n in new_desktop_f:
#         file_with_url = os.path.join(root, file_n)
#         imdb_url = open_right_file(file_with_url)
#         yield root.rpartition('/')[-1], (imdb_url, root)
#

    # for root, _, filename in os.walk(scan_dir):
    #    if not {root}.issubset(seen_movies):
    #        for file_n in filename:
    #            if file_n.endswith('.desktop'):
    #                file_with_url = os.path.join(root, file_n)
    #                imdb_url = open_right_file(file_with_url)
    #                yield root.rpartition('/')[-1], (imdb_url, root)
