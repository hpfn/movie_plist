import os
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
