#!/usr/bin/python3

import os


def dir_to_scan():
    """
       return urls from .desktop files and
       path to dir with movie
    """
    scan_dir = "/home/zaza/Vídeos/"
    urls_movies = list()

    for root, dir_name, filename in os.walk(scan_dir):
        for wanted_file in filename:
            urls_movies_stuff = list()
            if wanted_file.endswith('.desktop'):
                file_to_search = root + '/' + wanted_file
                with open(file_to_search, 'r') as check_content:
                    url = check_content.readlines()
                    urls_movies_stuff.append(url[-2].strip()[4:])
                    urls_movies_stuff.append(root)
                    for path, dir_n, file_n in os.walk(root):
                        for i in file_n:
                            name = i.startswith('sample')
                            if i.endswith(('.avi', '.mp4', '.mkv')) and not name:
                                urls_movies_stuff.append(i)
            # with open(file_to_search, 'r') as check_content:
            # url = check_content.readlines()
            # urls_movies.append([url[-2].strip()[4:], root, movie_file])
            if urls_movies_stuff:
                urls_movies.append(urls_movies_stuff)

    print(urls_movies)
    return urls_movies
