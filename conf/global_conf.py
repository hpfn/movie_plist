import os
import sys
from pathlib import Path
import urllib3

# user
home_user = os.environ['HOME']
# first, main path
movie_plist_stuff = os.path.join(home_user, '.config/movie_plist')
cfg_file = os.path.join(movie_plist_stuff, 'movie_plist.cfg')
seen_json_file = os.path.join(movie_plist_stuff, 'seen_movies.json')
unseen_json_file = os.path.join(movie_plist_stuff, 'unseen_movies.json')

# if path to movie_plist does not exist create one
movie_plist_config_dir = Path(movie_plist_stuff)
if not movie_plist_config_dir.is_dir():
    os.system('/bin/mkdir -p ' + movie_plist_stuff)

if not os.path.isfile(seen_json_file):
    with open(seen_json_file, 'w') as j_file:
        j_file.write('{}')

if not os.path.isfile(unseen_json_file):
    with open(unseen_json_file, 'w') as j_file:
        j_file.write('{}')


def read_path():
    with open(cfg_file, 'r') as movie_plist_cfg:
        cfg_path = movie_plist_cfg.readline()

    chck_path = Path(cfg_path)
    if chck_path.is_dir():
        return cfg_path
    else:
        print("Invalid path in movie_plist.cfg file")
        print(chck_path)
        sys.exit(1)


def write_path(cfg_path):
    # path already checked
    with open(cfg_file, 'w') as cfg_write:
        cfg_write.write(cfg_path)

    return cfg_path


def get_dir_path():
    chck_path = Path(cfg_file)
    if chck_path.is_file():
        path_dir_scan = read_path()
    else:
        path_dir_scan = input(" Do the scan in which directory ? ")
        path_dir_scan = write_path(path_dir_scan)

    return path_dir_scan


def internet_on():
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.imdb.com', retries=False, timeout=4.0)
        return r.status
    # more except is needed
    except urllib3.exceptions.ConnectTimeoutError:
        print('No Internet Connection ! Or IMDB has a problem...')
        print('and movie_plist will crash, probably')
        return False


def scan_dir_has_movies(scan_dir):
    # tem que fazer uma checagem melhor
    d_size = os.lstat(scan_dir)

    if d_size.st_size > 5000:
        return True

    from PyQt5.QtWidgets import QMessageBox, QApplication

    app = QApplication(['0'])

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Empty Directory")

    text = """
        The directory scanned seems empty. 
        Please check the scan dir.
        """ + scan_dir

    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

    sys.exit('1')
