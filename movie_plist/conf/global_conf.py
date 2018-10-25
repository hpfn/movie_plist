import json
import os
import sys

# from PyQt5.QtWidgets import QApplication, QMessageBox

# user
home_user = os.environ['HOME']
# first, main path
MOVIE_PLIST_CACHE = os.path.join(home_user, '.cache/movie_plist')
MOVIE_PLIST_STUFF = os.path.join(home_user, '.config/movie_plist')
CFG_FILE = os.path.join(MOVIE_PLIST_STUFF, 'movie_plist.cfg')
SEEN_JSON_FILE = os.path.join(MOVIE_PLIST_STUFF, 'seen_movies.json')
UNSEEN_JSON_FILE = os.path.join(MOVIE_PLIST_STUFF, 'unseen_movies.json')


class InvalidPath(Exception):
    pass


def check_movie_plist_dirs():
    if not os.path.isdir(MOVIE_PLIST_CACHE):
        os.system('/bin/mkdir -p ' + MOVIE_PLIST_CACHE)

    if not os.path.isdir(MOVIE_PLIST_STUFF):
        os.system('/bin/mkdir -p ' + MOVIE_PLIST_STUFF)

    # for json_file in [seen_json_file, unseen_json_file]:
    #     if not os.path.isfile(json_file):
    #         with open(json_file, 'w') as j_file:
    #             j_file.write('{}')


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

    return cfg_path


def get_dir_path():
    if os.path.isfile(CFG_FILE):
        path_dir_scan = read_path()
    else:
        get_dir_scan = input(" Do the scan in which directory ? ")
        path_dir_scan = write_path(get_dir_scan)

    return path_dir_scan


def load_from_json(json_file):
    if os.path.isfile(json_file):
        with open(json_file) as json_data:
            return json.load(json_data)

    return dict()


MOVIE_SEEN = load_from_json(SEEN_JSON_FILE)
MOVIE_UNSEEN = load_from_json(UNSEEN_JSON_FILE)


def dump_json_movie(movie_dic, json_file):
    with open(json_file, 'w') as outfile:
        json.dump(movie_dic, outfile)


def scan_dir_has_movies(scan_dir):
    # tem que fazer uma checagem melhor
    for _, _, filename in os.walk(scan_dir):
        for file in filename:
            if file.endswith('.desktop'):
                return True

    from PyQt5.QtWidgets import QMessageBox, QApplication  # pylint: disable-msg=E0611

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

    sys.exit('1')
