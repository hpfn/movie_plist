import os
from unittest.mock import patch

import pytest
from movie_plist.conf import global_conf


@pytest.fixture(scope='module')
def mock_attrs():
    # SetUp
    global_conf.home_user = 'home'
    global_conf.movie_plist_stuff = os.path.join(global_conf.home_user, '.config/movie_plist')
    global_conf.cfg_file = os.path.join(global_conf.movie_plist_stuff, 'movie_plist.cfg')
    global_conf.seen_json_file = os.path.join(global_conf.movie_plist_stuff, 'seen_movies.json')
    global_conf.unseen_json_file = os.path.join(global_conf.movie_plist_stuff, 'unseen_movies.json')
    global_conf.check_module_attr()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yield os.path.join(base_dir, 'tests/videos_test')
    # TearDown
    os.system('/bin/rm -fr ' + global_conf.home_user)


def test_movie_plist_conf_files(mock_attrs):
    assert os.path.isdir(global_conf.movie_plist_stuff)
    assert os.path.isfile(global_conf.seen_json_file)
    assert os.path.isfile(global_conf.unseen_json_file)


def test_write_path(mock_attrs):
    """
    call write_path to create movie_plist.cfg file
    """
    global_conf.write_path(mock_attrs)
    assert os.path.isfile(global_conf.cfg_file)


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
    global_conf.cfg_file = global_conf.unseen_json_file
    with pytest.raises(global_conf.InvalidPath):
        global_conf.read_path()


@patch('movie_plist.conf.global_conf.sys')
@patch('movie_plist.conf.global_conf.QApplication')
@patch('movie_plist.conf.global_conf.QMessageBox')
def test_fail_scan(message, app, sys):
    global_conf.scan_dir_has_movies('/tmp/XXX')
    assert message.call_count == 1
    assert app.call_count == 1
    # assert sys.call_count == 1
