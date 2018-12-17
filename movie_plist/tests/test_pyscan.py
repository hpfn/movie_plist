import os
from unittest.mock import patch

import pytest

from movie_plist.data import pyscan  # noqa: E402

expected = [
    hasattr(pyscan, 'os'),
    hasattr(pyscan, 're'),
    hasattr(pyscan, 'time'),
    hasattr(pyscan, 'exit'),
    hasattr(pyscan, 'MOVIE_SEEN'),
    hasattr(pyscan, 'MOVIE_UNSEEN'),
    hasattr(pyscan, 'create_dicts'),
    hasattr(pyscan, '_new_data'),
    hasattr(pyscan, '_new_desktop_f'),
    hasattr(pyscan, '_unknow_dirs'),
    hasattr(pyscan, '_open_right_file'),
    hasattr(pyscan, 'mk_title_year'),
    hasattr(pyscan, 'InvalidPath'),
    hasattr(pyscan, 'read_path'),
    hasattr(pyscan, 'write_path'),
    hasattr(pyscan, 'get_dir_path'),
    hasattr(pyscan, 'scan_dir_has_movies'),

]


@pytest.mark.parametrize('e', expected)
def test_attrs(e):
    assert e


pyscan.MOVIE_SEEN = dict()
pyscan.MOVIE_UNSEEN = dict()


@pytest.fixture()
def test_all(mocker):
    mocker.patch.object(
        pyscan,
        'get_dir_path',
        return_value='movie_plist/tests/videos_test/'
    )
    return pyscan.create_dicts()


def test_all_key(test_all):
    assert 'Shawshank Redemption, the 1994' in pyscan.MOVIE_UNSEEN.keys()


def test_all_url(test_all):
    url, _ = list(pyscan.MOVIE_UNSEEN.values())[0]
    assert 'https://www.imdb.com/title/tt0111161/' in url


def test_all_path_to(test_all):
    _, path_to = list(pyscan.MOVIE_UNSEEN.values())[0]

    return_path = 'movie_plist/tests/'
    return_path += 'videos_test/Shawshank Redemption, the 1994'
    assert return_path in path_to


def test_all_movie_seen_len(test_all):
    # assert len(pyscan.MOVIE_UNSEEN) == 1
    assert len(pyscan.MOVIE_SEEN) == 0


def test_url_raises():
    with pytest.raises(Exception):
        pyscan.create_dicts('movie_plist/tests/url_test/')


@pytest.fixture
def test_cfg_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_path_read = os.path.join(base_dir, 'tests/videos_test')
    pyscan.CFG_FILE = 'movie_plist/tests/movie_plist.cfg'
    with open(pyscan.CFG_FILE, 'w') as w_file:
        w_file.write(test_path_read)
    yield test_path_read, pyscan.CFG_FILE
    os.system('/bin/rm -fr ' + pyscan.CFG_FILE)


def test_write_path(test_cfg_file):
    """
    call write_path to create movie_plist.cfg file
    """
    test_path = 'movie_plist/tests'
    assert os.path.isdir(test_path)
    r_path = pyscan.write_path(test_path)
    assert r_path == test_path
    assert os.path.isfile(pyscan.CFG_FILE)


def test_read_path(test_cfg_file):
    test_path_read, _ = test_cfg_file

    assert 'videos_test' in test_path_read
    assert pyscan.read_path() == test_path_read


def test_whole_success_process(test_cfg_file):
    test_path_read, _ = test_cfg_file
    assert test_path_read == pyscan.get_dir_path()


def test_fail_write_path():
    with pytest.raises(pyscan.InvalidPath):
        pyscan.write_path('/tmp/XXX')


def test_fail_read_path():
    pyscan.CFG_FILE = 'movie_plist/tests/__init__.py'
    with pytest.raises(pyscan.InvalidPath):
        pyscan.read_path()


@patch('movie_plist.data.pyscan.exit')
@patch('PyQt5.QtWidgets.QApplication')
@patch('PyQt5.QtWidgets.QMessageBox')
def test_fail_scan(message, app, exit):
    pyscan.scan_dir_has_movies('/tmp/XXX')
    assert message.call_count == 1
    assert app.call_count == 1
    assert exit.call_count == 1


def test_scan_dir_has_movies():
    """
     It is called from read_path, but testing alone
     Must return True to not call PyQt stuff
    """
    assert pyscan.scan_dir_has_movies('movie_plist/tests/videos_test')
