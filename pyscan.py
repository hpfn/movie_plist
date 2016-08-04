#!/usr/bin/python3

import os


def dir_to_scan():
    """ return urls from .desktop files """
    scan_dir = "/home/zaza/Vídeos/"
    urls_movies = list()

    for root, dir_name, filename in os.walk(scan_dir):
        for wanted_file in filename:
            if wanted_file.endswith('.desktop'):
                file_to_search = root + '/' + wanted_file
                with open(file_to_search, 'r') as check_content:
                    url = check_content.readlines()
                    if url:
                        urls_movies.append(url[-2].strip()[4:])

    return urls_movies
