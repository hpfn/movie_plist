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

_json_movies = ''
_scan_dir = ''


def create_dicts(scan_dir):
    """
    # get seen movies from json file
    # get unseen movies from on json file
    # check for new moview
    # if no unseen movies ask if continue
    # return seen and unseen movies
    """
    global _json_movies
    global _scan_dir

    _scan_dir = scan_dir

    start = time.time()

    # alterar para for *_,
    movies_path = set(m_path for *_, m_path in MOVIE_SEEN.values())
    umovies_path = set(um_path for *_, um_path in MOVIE_UNSEEN.values())
    _json_movies = set.union(movies_path, umovies_path)

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
        title_year = root.rpartition('/')[-1]
        # synopsis = ParseImdbData(imdb_url, title_year)
        # yield title_year, (imdb_url, synopsis.synopsis(), root)
        yield title_year, (imdb_url, root)


def _new_desktop_f():
    """ search for a .desktop file in a directory """
    return ((root, file_n)
            for root, filename in _unknow_dirs()
            for file_n in filename
            if file_n.endswith('.desktop'))


def _unknow_dirs():
    """ root (path) that are not in json files """
    global _json_movies
    global _scan_dir

    return ((root, filename)
            for root, _, filename in os.walk(_scan_dir)
            if not {root}.issubset(_json_movies))


def _open_right_file(file_with_url):
    """ open the right file and get the url"""
    with open(file_with_url, 'r') as check_content:
        file_lines = check_content.readlines()

    url = re.search(r"(URL|url)=https?://.*", ' '.join(file_lines))

    if url:
        return url.group(0)[4:]
