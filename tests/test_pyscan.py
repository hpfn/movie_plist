import pytest
import sys
import os
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from data import pyscan


pyscan.seen_json_file = './tests/seen_json_file.json'
pyscan.unseen_json_file = './tests/unseen_json_file.json'

c_d = pyscan.CreateDict('./tests/videos_test/')
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
