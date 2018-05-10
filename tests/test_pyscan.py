import pytest
import sys
import os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))


#@pytest.fixture
#def py_scan():
from data import pyscan

pyscan.seen_json_file = './tests/seen_json_file.json'
pyscan.unseen_json_file = './tests/unseen_json_file.json'

c_d = pyscan.CreateDict('./tests/videos_test/')
#    return c_d
movie_seen, movie_unseen = c_d.create_dicts()
url, path_to = list(movie_unseen.values())[0]

instance_params = [
    (isinstance(movie_unseen, dict), True),
    (isinstance(movie_seen, dict), True)
]


@pytest.mark.parametrize("a,b", instance_params)
def test_dict_instance(a, b):
    assert a is b


str_params = [
    ('Shawshank Redemption, the 1994', movie_unseen.keys()),
    ('https://www.imdb.com/title/tt0111161/', url),
    ('./tests/videos_test/Shawshank Redemption, the 1994', path_to)
]


@pytest.mark.parametrize("a,b", str_params)
def test_dict(a, b):
    assert a in b


size_params = [
    (len(movie_unseen), 1),
    (len(movie_seen), 0)
]


@pytest.mark.parametrize("a,b", size_params)
def test_dict_size(a, b):
    assert a == b


# def test_unknow_dirs():
#     scan_dir = py_scan()
#
#     unkown_dirs = scan_dir._unknow_dirs()
#     list_scan_dir = list(unkown_dirs)
#     assert len(list_scan_dir) == 2
#     assert './tests/videos_test/Shawshank Redemption, the 1994' in list_scan_dir[1]
#
#
# def test_new_desktop_f():
#     scan_dir = py_scan()
#
#     new_desktop_f = scan_dir._new_desktop_f()
#     new_desktop_f = list(new_desktop_f)
#     assert len(new_desktop_f) == 1