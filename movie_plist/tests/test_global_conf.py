import os
from unittest.mock import patch

import pytest

from movie_plist.conf import global_conf


@pytest.fixture(scope='module')
def mock_attrs():
    # SetUp
    global_conf.home_user = 'home'
    global_conf.MOVIE_PLIST_STUFF = os.path.join(global_conf.home_user, '.config/movie_plist')
    os.system('/bin/mkdir -p ' + global_conf.MOVIE_PLIST_STUFF)
    global_conf.MOVIE_PLIST_CACHE = os.path.join(global_conf.home_user, '.cache/movie_plist')
    os.system('/bin/mkdir -p ' + global_conf.MOVIE_PLIST_CACHE)
    global_conf.CFG_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'movie_plist.cfg')
    global_conf.SEEN_JSON_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'seen_movies.json')
    global_conf.UNSEEN_JSON_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'unseen_movies.json')
    for json_file in [global_conf.SEEN_JSON_FILE, global_conf.UNSEEN_JSON_FILE]:
        if not os.path.isfile(json_file):
            with open(json_file, 'w') as j_file:
                j_file.write('{}')

    global_conf.check_movie_plist_dirs()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yield os.path.join(base_dir, 'tests/videos_test')
    # TearDown
    os.system('/bin/rm -fr ' + global_conf.home_user)


def test_movie_plist_conf_files(mock_attrs):
    assert os.path.isdir(global_conf.MOVIE_PLIST_CACHE)
    assert os.path.isdir(global_conf.MOVIE_PLIST_STUFF)
    assert os.path.isfile(global_conf.SEEN_JSON_FILE)
    assert os.path.isfile(global_conf.UNSEEN_JSON_FILE)


def test_write_path(mock_attrs):
    """
    call write_path to create movie_plist.cfg file
    """
    global_conf.write_path(mock_attrs)
    assert os.path.isfile(global_conf.CFG_FILE)
    assert os.path.isfile(global_conf.CFG_FILE)


def test_scan_dir_has_movies(mock_attrs):
    """
     It is called from read_path, but testing alone
     Must return True to not call PyQt stuff
    """
    assert global_conf.scan_dir_has_movies(mock_attrs)


def test_read_path(mock_attrs):
    """
    get the path from file created by write_path

    read_path calls already tested 'scan_dir_has_movies(scan_dir)'
    """
    assert mock_attrs == global_conf.read_path()


def test_whole_success_process(mock_attrs):
    assert mock_attrs == global_conf.get_dir_path()


def test_fail_write_path():
    with pytest.raises(global_conf.InvalidPath):
        global_conf.write_path('/tmp/XXX')


def test_fail_read_path():
    global_conf.CFG_FILE = global_conf.UNSEEN_JSON_FILE
    with pytest.raises(global_conf.InvalidPath):
        global_conf.read_path()


@patch('movie_plist.conf.global_conf.sys')
@patch('PyQt5.QtWidgets.QApplication')
@patch('PyQt5.QtWidgets.QMessageBox')
def test_fail_scan(message, app, sys):
    global_conf.scan_dir_has_movies('/tmp/XXX')
    assert message.call_count == 1
    assert app.call_count == 1
    assert sys.call_count == 0


def test_json_functions_exists():
    assert hasattr(global_conf, 'load_from_json')
    assert hasattr(global_conf, 'dump_json_movie')


def test_movies_attrs():
    assert isinstance(global_conf.MOVIE_SEEN, dict)
    assert isinstance(global_conf.MOVIE_UNSEEN, dict)
