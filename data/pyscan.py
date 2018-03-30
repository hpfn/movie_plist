#!/usr/bin/python3

import os
import re
import sys
import json
import time
# from PyQt5.QtWidgets import QMessageBox, QApplication
from conf.global_conf import seen_json_file, unseen_json_file


def empty_unseen_dict():
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


def open_right_file(root_path, right_file):
    """ open the right file and get the url"""
    file_to_search = os.path.join(root_path, right_file)
    with open(file_to_search, 'r') as check_content:
        file_lines = check_content.readlines()

    url = re.search(r"(URL|url)=https?://.*", ' '.join(file_lines))

    if url:
        return url.group(0)[4:]


def dir_to_scan(scan_dir, seen_movies):
    """
    find .desktop file  to get imdb url

    yield:
      imdb_url: to get poster and synopsis
      root will go to QTab-QTree
      named_dir is title_year (user mkdir name)
    """
    # arq_pattern = re.compile(r"[\w,'-.]+\.desktop")
    # dirname is the title_year if the user do it right
    # dirname_titleyear = re.compile('/.*/')
    # selection_dirs = ((root, filename)
    #                   for root, _, filename in os.walk(scan_dir)
    #                   if not {root}.issubset(seen_movies))
    #
    # for root, filename in selection_dirs:
    #     this_one = re.search(arq_pattern, ' '.join(filename))
    #     if this_one:
    #         imdb_url = open_right_file(root, this_one.group(0))
    #         yield dirname_titleyear.sub('', root), [imdb_url, root]

    for root, _, filename in os.walk(scan_dir):
        if not {root}.issubset(seen_movies):
            # this_one = re.search(arq_pattern, ' '.join(filename))
            # if this_one:
            #    imdb_url = open_right_file(root, this_one.group(0))
            #    yield dirname_titleyear.sub('', root), [imdb_url, root]
            for file_n in filename:
                if file_n.endswith('.desktop'):
                    imdb_url = open_right_file(root, file_n)
                    # yield dirname_titleyear.sub('', root), [imdb_url, root]
                    yield root.rpartition('/')[-1], (imdb_url, root)


def create_dicts(s_dir):
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
    all_movies_path = set.union(movies_path, umovies_path)

    movie_unseen_to_add = {dir_name: i for dir_name, i in dir_to_scan(s_dir, all_movies_path)}
    movie_unseen.update(movie_unseen_to_add)

    if len(movie_unseen) == 0:
        empty_unseen_dict()

    end = time.time()
    print(end - start)

    return movie_seen, movie_unseen
