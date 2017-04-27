#!/usr/bin/python3

import os


def open_right_file(root_path, right_file):
    """ open the right file and get the url"""
    file_to_search = root_path + '/' + right_file
    with open(file_to_search, 'r') as check_content:
        url = check_content.readlines()
        return url[-2][4:-1]


def dir_to_scan(scan_dir):
    """
    find .desktop file and call others methods
    to append: path to dir with movie
    imdb url
    """
    # urls_movies = list()
    for root, dir_name, filename in os.walk(scan_dir):
        # print(root)
        for wanted_file in filename:
            if wanted_file.endswith('.desktop'):
                imdb_url = open_right_file(root, wanted_file)
                # print(imdb_url)

                # colocar yield aqui. enviar para conferir se esta no db
                # urls_movies.append([imdb_url, root])
                # imdb_url will go to sqlite3 when marked as seen
                # root will go to QTab-QTree
                # dir_name is a replacement to title_year
                yield [imdb_url, root], dir_name

                # return urls_movies
