#!/usr/bin/python3

import os
import re
import sys
import json
from conf.global_conf import json_file
# import urllib.request
# import urllib.error
# from socket import timeout
# from data import pimdbdata
# from data.pyscan import dir_to_scan
# from info_in_db.movie_plist_sqlite3 import DataStorage


def open_right_file(root_path, right_file):
    """ open the right file and get the url"""
    file_to_search = root_path + '/' + right_file
    with open(file_to_search, 'r') as check_content:
        url = check_content.readlines()
        return url[-2][4:-1]


def dir_to_scan(scan_dir):
    """
    find .desktop file  to get imdb url
    get path to movie file
    dir_name is not used

    yield:
      imdb_url will go to sqlite3 when marked as seen
      root will go to QTab-QTree
      named_dir is a replacement to title_year
    """
    arq_pattern = re.compile(r"[\w,'-.]+\.desktop")
    named_dir_pattern = re.compile('/.*/')
    for root, dir_name, filename in os.walk(scan_dir):
        this_one = re.search(arq_pattern, ' '.join(filename))
        if this_one:
            imdb_url = open_right_file(root, this_one.group(0))
            named_dir = named_dir_pattern.sub('', root)
            yield [imdb_url, root], named_dir


def create_dicts(s_dir):
    """
    # check if the movie info is in movie_plist_sqlite3.db
    # if yes goes to movie_seen dict
    # if not goes to movie_unseen dict
    # dict's key is title_year of the movie
    """
    with open(json_file) as json_data:
        movie_seen = json.load(json_data)

    movie_unseen = {dir_name: i for i, dir_name in dir_to_scan(s_dir)
                    if dir_name not in movie_seen.keys()}
    # movie_seen = dict()
    # movie_unseen = dict()
    # stored_data = DataStorage()
    # movies_stored = set(x[0] for x in stored_data.movie_url())

    # for i, dir_name in dir_to_scan(s_dir):
    #     title_year = dir_name
    #     item = set([i[0]])
    #     if item.issubset(movies_stored):
    #         movie_seen[title_year] = i
    #     else:
    #         movie_unseen[title_year] = i
    #
    # stored_data.exit_from_db()

    if len(movie_unseen) == 0 and len(movie_seen) == 0:
        print("No .desktop file found.")
        sys.exit()

    return movie_seen, movie_unseen
