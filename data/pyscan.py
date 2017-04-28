#!/usr/bin/python3

import os
import re
import sys
# import urllib.request
# import urllib.error
# from socket import timeout
# from data import pimdbdata
# from data.pyscan import dir_to_scan
from info_in_db.movie_plist_sqlite3 import DataStorage


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
    dir name
    """
    for root, dir_name, filename in os.walk(scan_dir):
        for wanted_file in filename:
            if wanted_file.endswith('.desktop'):
                imdb_url = open_right_file(root, wanted_file)
                # imdb_url will go to sqlite3 when marked as seen
                # root will go to QTab-QTree
                # named_dir is a replacement to title_year
                named_dir = re.compile('/.*/')
                named_dir = named_dir.sub('', root)
                yield [imdb_url, root], named_dir

                # return urls_movies


def create_dicts(s_dir):
    """
    # check if the movie info is in movie_plist_sqlite3.db
    # if yes goes to movie_seen dict
    # if not goes to movie_unseen dict
    # dict's key is title_year of the movie
    """
    movie_seen = dict()
    movie_unseen = dict()
    stored_data = DataStorage()
    movies_stored = str(stored_data.movie_url())

    for i, dir_name in dir_to_scan(s_dir):
        ''' this is too slow...
        try:
            html = urllib.request.urlopen(i[0], timeout=3).read()
            movie = pimdbdata.ParseImdbData(html)
            title_year = movie.title_year()
        except timeout:
            title_year = dir_name
        except urllib.error.URLError:
            title_year = dir_name
        except ValueError:
            print("please, check .desktop file in {}".format(dir_name))
            # check pyqt_guit/splitter.py
            i[0] = 'bad url'
            title_year = dir_name
        '''
        title_year = dir_name
        if i[0] in movies_stored:
            movie_seen[title_year] = i
        else:
            movie_unseen[title_year] = i

    stored_data.exit_from_db()

    if len(movie_unseen) == 0 and len(movie_seen) == 0:
        print("No .desktop file found.")
        sys.exit()

    return movie_seen, movie_unseen
