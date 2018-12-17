import os
import re
import time
from sys import exit

from movie_plist.conf.global_conf import CFG_FILE, MOVIE_SEEN, MOVIE_UNSEEN

# from movie_plist.data.pimdbdata import ParseImdbData


# class CreateDict:
#     def __init__(self, scan_dir):
#         self._scan_dir = scan_dir
#         self._json_movies = ''
#         self._file_with_url = ''
#


# _scan_dir = ''


def create_dicts():
    """
    # get seen movies from json file
    # get unseen movies from on json file
    # check for new moview
    # if no unseen movies ask if continue
    # return seen and unseen movies
    """

    # global _scan_dir

    # _scan_dir = scan_dir

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

    # global _scan_dir
    _scan_dir = get_dir_path()

    _json_movies = {**MOVIE_SEEN, **MOVIE_UNSEEN}

    for root, _, filename in os.walk(_scan_dir):
        title_year = _json_movies.get(mk_title_year(root), 0)
        if not title_year:
            yield (root, filename)


def _open_right_file(file_with_url):
    """ open the right file and get the url"""
    # IO error out of try/except
    with open(file_with_url, 'r') as check_content:
        file_lines = check_content.readlines()

    try:
        line_with_url = re.search(r"(URL|url)=https?://.*", ' '.join(file_lines))
        url = line_with_url.group(0)[4:]
    except AttributeError:
        raise Exception('There is no url in %s' % file_with_url)
    else:
        return url


def mk_title_year(root_path):
    return root_path.rpartition('/')[-1]


class InvalidPath(Exception):
    pass


def read_path():
    with open(CFG_FILE, 'r') as movie_plist_cfg:
        cfg_path = movie_plist_cfg.readline()

    if not os.path.isdir(cfg_path):
        raise InvalidPath('Invalid path in movie_plist.cfg file.')

    scan_dir_has_movies(cfg_path)
    return cfg_path


def write_path(cfg_path):
    if not os.path.isdir(cfg_path):
        raise InvalidPath('Invalid path. Please try again.')

    with open(CFG_FILE, 'w') as cfg_write:
        cfg_write.write(cfg_path)

    scan_dir_has_movies(cfg_path)
    return cfg_path


def get_dir_path():
    if os.path.isfile(CFG_FILE):
        path_dir_scan = read_path()
    else:
        get_dir_scan = input(" Do the scan in which directory ? ")
        path_dir_scan = write_path(get_dir_scan)

    return path_dir_scan


def scan_dir_has_movies(scan_dir):
    # tem que fazer uma checagem melhor
    for _, _, filename in os.walk(scan_dir):
        for file in filename:
            if file.endswith('.desktop'):
                return True

    from PyQt5.QtWidgets import QMessageBox, QApplication  # pylint: disable-msg=E0611
    #    import sys

    app = QApplication(['0'])  # noqa: F841

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Empty Directory")

    text = """
        The directory scanned seems empty.
        Please check the directory
         """ + scan_dir

    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

    exit('1')
