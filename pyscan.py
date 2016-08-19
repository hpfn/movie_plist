#!/usr/bin/python3

import os


def dir_to_scan(scan_dir):
    """
       return urls from .desktop files and
       path to dir with movie
       movie file ( lower case ): avi, mp4, mkv
    """
    # scan_dir = "/path/to/dir/"
    urls_movies = list()

    for root, dir_name, filename in os.walk(scan_dir):
        for wanted_file in filename:
            urls_movies_stuff = list()
            if wanted_file.endswith('.desktop'):
                file_to_search = root + '/' + wanted_file
                with open(file_to_search, 'r') as check_content:
                    url = check_content.readlines()
                    urls_movies_stuff.append(url[-2][4:-1])
                    urls_movies_stuff.append(root)
                    for file_n in filename:  # path, dir_n, file_n in os.walk(root):
                        # for i in file_n:
                        name = file_n.lower().startswith('sample')
                        if file_n.endswith(('.avi', '.mp4', '.mkv')) and not name:
                            urls_movies_stuff.append(file_n)
            # with open(file_to_search, 'r') as check_content:
            # url = check_content.readlines()
            # urls_movies.append([url[-2].strip()[4:], root, movie_file])
            if urls_movies_stuff:
                if len(urls_movies_stuff) < 3:
                    urls_movies_stuff.append("No_movie_file_yet")
                urls_movies.append(urls_movies_stuff)

    # print(urls_movies)
    return urls_movies

# dir_to_scan("/home/zaza/Vídeos")
