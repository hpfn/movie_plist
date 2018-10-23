import pytest

# import sys
# import os
# sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from movie_plist.data import pyscan  # noqa: E402

expected = [
    hasattr(pyscan, 'os'),
    hasattr(pyscan, 're'),
    hasattr(pyscan, 'time'),
    hasattr(pyscan, 'movie_seen'),
    hasattr(pyscan, 'movie_unseen'),
    hasattr(pyscan, 'ParseImdbData')
]


@pytest.mark.parametrize('e', expected)
def test_attrs(e):
    assert e


pyscan.movie_seen = dict()
pyscan.movie_unseen = dict()

c_d = pyscan.CreateDict('movie_plist/tests/videos_test/')
movie_seen, movie_unseen = c_d.create_dicts()

url, synopsis, path_to = list(movie_unseen.values())[0]

instance_params = [
    (isinstance(movie_unseen, dict), True),
    (isinstance(movie_seen, dict), True)
]


@pytest.mark.parametrize("a,b", instance_params)
def test_dict_instance(a, b):
    assert a is b


synopsis_text = 'Directed by Frank Darabont.'
synopsis_text += '  With Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler.'
synopsis_text += ' Two imprisoned men bond over a number of years, finding solace'
synopsis_text += ' and eventual redemption through acts of common decency.'

str_params = [
    ('Shawshank Redemption, the 1994', movie_unseen.keys()),
    ('https://www.imdb.com/title/tt0111161/', url),
    (synopsis_text, synopsis),
    ('movie_plist/tests/videos_test/Shawshank Redemption, the 1994', path_to)
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
