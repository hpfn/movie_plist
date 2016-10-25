#!/usr/bin/python3

import os


class PyScan(object):
    def __init__(self, scan_dir):
        self.scan_dir = scan_dir

    @staticmethod
    def gather_info(imdb_url, r_path, f_name, ):
        """
           put where to find info about the
           movie in a list and return that list
        """
        urls_movies_stuff = list()
        urls_movies_stuff.append(imdb_url)
        urls_movies_stuff.append(r_path)
        urls_movies_stuff.append(f_name)
        return urls_movies_stuff

    @staticmethod
    def find_movie_file(file_name):
        """
           find the file to play
           if not tell there is no file
        """
        for file_n in file_name:
            name = file_n.lower().startswith('sample')
            if file_n.endswith(('.avi', '.mp4', '.mkv')) and not name:
                return file_n

        return "No_movie_file_yet"

    @staticmethod
    def open_right_file(root_path, right_file):
        """ open the right file and get the url"""
        file_to_search = root_path + '/' + right_file
        with open(file_to_search, 'r') as check_content:
            url = check_content.readlines()
            return url[-2][4:-1]

    def dir_to_scan(self):
        """
            find .desktop file and call others methods
            to append: path to dir with movie
                       imdb url
                       movie file ( lower case ): avi, mp4, mkv
        """
        urls_movies = list()
        for root, dir_name, filename in os.walk(self.scan_dir):
            for wanted_file in filename:
                if wanted_file.endswith('.desktop'):
                    open_r_f = self.open_right_file(root, wanted_file)
                    file_n = self.find_movie_file(filename)

                    urls_movies.append(self.gather_info(open_r_f, root, file_n))


        return urls_movies
