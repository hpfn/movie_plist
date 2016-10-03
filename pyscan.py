#!/usr/bin/python3

import os


def find_movie_file(urls_m_stuff2, file_name):
    """ find the file to play """
    for file_n in file_name:  # path, dir_n, file_n in os.walk(root):
        # for i in file_n:
        name = file_n.lower().startswith('sample')
        if file_n.endswith(('.avi', '.mp4', '.mkv')) and not name:
            urls_m_stuff2.append(file_n)

    if len(urls_m_stuff2) < 3:
        urls_m_stuff2.append("No_movie_file_yet")


def open_right_file(urls_m_stuff, root_path, right_file):
    """ open the right file and get the url"""
    # urls_movies_stuff = list()
    file_to_search = root_path + '/' + right_file
    with open(file_to_search, 'r') as check_content:
        url = check_content.readlines()
        urls_m_stuff.append(url[-2][4:-1])
        urls_m_stuff.append(root_path)


def dir_to_scan(scan_dir):
    """
       find .desktop file and call others functions
       to append: path to dir with movie
                  movie file ( lower case ): avi, mp4, mkv
    """
    urls_movies = list()

    for root, dir_name, filename in os.walk(scan_dir):
        for wanted_file in filename:
            urls_movies_stuff = list()
            if wanted_file.endswith('.desktop'):
                # urls_movies_stuff = list()
                open_right_file(urls_movies_stuff, root, wanted_file)
                find_movie_file(urls_movies_stuff, filename)

            if urls_movies_stuff:
                urls_movies.append(urls_movies_stuff)

    return urls_movies
