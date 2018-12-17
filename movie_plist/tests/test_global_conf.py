import os

import pytest

from movie_plist.conf import global_conf

params = [
    hasattr(global_conf, 'home_user'),
    hasattr(global_conf, 'MOVIE_PLIST_STUFF'),
    hasattr(global_conf, 'MOVIE_PLIST_CACHE'),
    hasattr(global_conf, 'CFG_FILE'),
    hasattr(global_conf, 'SEEN_JSON_FILE'),
    hasattr(global_conf, 'UNSEEN_JSON_FILE'),
    hasattr(global_conf, 'check_movie_plist_dirs'),
    hasattr(global_conf, 'load_from_json'),
    hasattr(global_conf, 'dump_json_movie'),
    hasattr(global_conf, 'MOVIE_UNSEEN'),
    hasattr(global_conf, 'MOVIE_SEEN'),
]


@pytest.mark.parametrize('a', params)
def test_attrs(a):
    assert a


@pytest.fixture()
def mock_attrs():
    # SetUp
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    global_conf.home_user = os.path.join(base_dir, 'home')

    global_conf.MOVIE_PLIST_STUFF = os.path.join(global_conf.home_user, '.config/movie_plist')
    global_conf.MOVIE_PLIST_CACHE = os.path.join(global_conf.home_user, '.cache/movie_plist')
    global_conf.CFG_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'movie_plist.cfg')

    global_conf.SEEN_JSON_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'seen_movies.json')
    global_conf.UNSEEN_JSON_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'unseen_movies.json')

    global_conf.check_movie_plist_dirs()

    for json_file in [global_conf.SEEN_JSON_FILE, global_conf.UNSEEN_JSON_FILE]:
        if not os.path.isfile(json_file):
            with open(json_file, 'w') as j_file:
                j_file.write('{}')

    yield global_conf
    # TearDown
    os.system('/bin/rm -fr ' + global_conf.home_user)


def test_movie_plist_conf_files(mock_attrs):
    assert os.path.isdir(global_conf.MOVIE_PLIST_CACHE)
    assert os.path.isdir(global_conf.MOVIE_PLIST_STUFF)
    assert os.path.isfile(global_conf.SEEN_JSON_FILE)
    assert os.path.isfile(global_conf.UNSEEN_JSON_FILE)


def test_movies_attrs():
    assert isinstance(global_conf.MOVIE_SEEN, dict)
    assert isinstance(global_conf.MOVIE_UNSEEN, dict)


def test_cache_dir(mock_attrs):
    assert 'home/.cache/movie_plist' in global_conf.MOVIE_PLIST_CACHE


def test_config_dir(mock_attrs):
    assert 'home/.config/movie_plist' in global_conf.MOVIE_PLIST_STUFF
