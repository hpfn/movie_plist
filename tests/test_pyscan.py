import pytest
import sys
import os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))


@pytest.fixture
def py_scan():
    from data import pyscan

    pyscan.seen_json_file = './tests/seen_json_file.json'
    pyscan.unseen_json_file = './tests/unseen_json_file.json'

    c_d = pyscan.CreateDict('./tests/videos_test/')

    return c_d

params = [

]


def test_create_dicts():
    scan_dir = py_scan()

    _, movie_unseen = scan_dir.create_dicts()
    assert isinstance(movie_unseen, dict)
    assert 'Shawshank Redemption, the 1994' in movie_unseen.keys()
    assert len(movie_unseen) == 1


def test_unknow_dirs():
    scan_dir = py_scan()

    unkown_dirs = scan_dir._unknow_dirs()
    list_scan_dir = list(unkown_dirs)
    assert len(list_scan_dir) == 2
    assert './tests/videos_test/Shawshank Redemption, the 1994' in list_scan_dir[1]


def test_new_desktop_f():
    scan_dir = py_scan()

    new_desktop_f = scan_dir._new_desktop_f()
    new_desktop_f = list(new_desktop_f)
    assert len(new_desktop_f) == 1