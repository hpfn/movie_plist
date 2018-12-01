import os
import re
import time

from movie_plist.conf.global_conf import MOVIE_SEEN, MOVIE_UNSEEN

# from movie_plist.data.pimdbdata import ParseImdbData


# class CreateDict:
#     def __init__(self, scan_dir):
#         self._scan_dir = scan_dir
#         self._json_movies = ''
#         self._file_with_url = ''
#


_scan_dir = ''


def create_dicts(scan_dir):
    """
    # get seen movies from json file
    # get unseen movies from on json file
    # check for new moview
    # if no unseen movies ask if continue
    # return seen and unseen movies
    """

    global _scan_dir

    _scan_dir = scan_dir

    start = time.time()

    movie_unseen_to_add = {dir_name: i for dir_name, i in _new_data()}
    MOVIE_UNSEEN.update(movie_unseen_to_add)
    # dump_json_movie(MOVIE_UNSEEN, UNSEEN_JSON_FILE)

    end = time.time()
    print(end - start)

    # return MOVIE_SEEN, MOVIE_UNSEEN


def _new_data():
    """ return title_year, imdb_url and path to movie """

    for root, file_n in _new_desktop_f():
        file_with_url = os.path.join(root, file_n)
        imdb_url = _open_right_file(file_with_url)
        title_year = mk_title_year(root)

        yield title_year, (imdb_url, root)


def _new_desktop_f():
    """ search for a .desktop file in a directory """
    return ((root, file_n)
            for root, filename in _unknow_dirs()
            for file_n in filename
            if file_n.endswith('.desktop'))


def _unknow_dirs():
    """ root (path) that are not in json files """

    global _scan_dir

    _json_movies = {**MOVIE_SEEN, **MOVIE_UNSEEN}

    for root, _, filename in os.walk(_scan_dir):
        title_year = _json_movies.get(mk_title_year(root), 0)
        if not title_year:
            yield (root, filename)


def _open_right_file(file_with_url):
    """ open the right file and get the url"""
    with open(file_with_url, 'r') as check_content:
        file_lines = check_content.readlines()

    url = re.search(r"(URL|url)=https?://.*", ' '.join(file_lines))

    if url:
        return url.group(0)[4:]


def mk_title_year(root_path):
    return root_path.rpartition('/')[-1]
