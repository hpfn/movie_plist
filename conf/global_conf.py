import os
import sys
from pathlib import Path
import urllib3


# user
user_name = os.environ['USER']
# first, main path
movie_plist_stuff = '/home/' + user_name + '/.config/movie_plist'
cfg_file = movie_plist_stuff + '/movie_plist.cfg'

# if path to movie_plist does not exist create one
check_path = Path(movie_plist_stuff)
if not check_path.is_dir():
    os.system('/bin/mkdir -p ' + movie_plist_stuff)


def read_path():
    with open(cfg_file, 'r') as movie_plist_cfg:
        cfg_path = movie_plist_cfg.readline()

    chck_path = Path(cfg_path)
    if chck_path.is_dir():
        return cfg_path
    else:
        print("Invalid path in movie_plist.cfg file")
        sys.exit(1)


def write_path(cfg_path):
    chck_path = Path(cfg_path)
    if not chck_path.is_dir():
        print(" Please, check the path. ")
        sys.exit(2)
    else:
        with open(cfg_file, 'w') as cfg_write:
            cfg_write.write(cfg_path)

    return cfg_path


def internet_on():
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.imdb.com', retries=False, timeout=4.0)
        return r.status
    except urllib3.exceptions.ConnectTimeoutError:
        print('No Internet Connection ! Or IMDB has a problem...')
        print('No poster')
        print('If the .html file must be re-created, no rate/votes')
        print('If there is a new movie, no data will be retrieve')
        print('and movie_plist will crash, probably')
        return False
