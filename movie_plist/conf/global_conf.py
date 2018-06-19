import os
import sys
from PyQt5.QtWidgets import QMessageBox, QApplication

# user
home_user = os.environ['HOME']
# first, main path
movie_plist_stuff = os.path.join(home_user, '.config/movie_plist')
cfg_file = os.path.join(movie_plist_stuff, 'movie_plist.cfg')
seen_json_file = os.path.join(movie_plist_stuff, 'seen_movies.json')
unseen_json_file = os.path.join(movie_plist_stuff, 'unseen_movies.json')


class InvalidPath(Exception):
    pass


def check_module_attr():
    if not os.path.isdir(movie_plist_stuff):
        os.system('/bin/mkdir -p ' + movie_plist_stuff)

    for json_file in [seen_json_file, unseen_json_file]:
        if not os.path.isfile(json_file):
            with open(json_file, 'w') as j_file:
                j_file.write('{}')


def read_path():
    with open(cfg_file, 'r') as movie_plist_cfg:
        cfg_path = movie_plist_cfg.readline()

    if not os.path.isdir(cfg_path):
        raise InvalidPath('Invalid path in movie_plist.cfg file.')

    scan_dir_has_movies(cfg_path)
    return cfg_path


def write_path(cfg_path):
    if not os.path.isdir(cfg_path):
        raise InvalidPath('Invalid path. Please try again.')

    with open(cfg_file, 'w') as cfg_write:
        cfg_write.write(cfg_path)

    return cfg_path


def get_dir_path():
    if os.path.isfile(cfg_file):
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

#    from PyQt5.QtWidgets import QMessageBox, QApplication

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
