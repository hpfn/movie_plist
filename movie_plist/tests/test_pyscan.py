import pytest

from movie_plist.data import pyscan  # noqa: E402

expected = [
    hasattr(pyscan, 'os'),
    hasattr(pyscan, 're'),
    hasattr(pyscan, 'time'),
    hasattr(pyscan, 'MOVIE_SEEN'),
    hasattr(pyscan, 'MOVIE_UNSEEN'),
    # hasattr(pyscan, 'UNSEEN_JSON_FILE')
]


@pytest.mark.parametrize('e', expected)
def test_attrs(e):
    assert e


pyscan.MOVIE_SEEN = dict()
pyscan.MOVIE_UNSEEN = dict()
# pyscan.UNSEEN_JSON_FILE = 'movie_plist/tests/unseen_movies.json'
# c_d = pyscan.create_dicts('movie_plist/tests/videos_test/')
pyscan.create_dicts('movie_plist/tests/videos_test/')
# movie_seen, movie_unseen = pyscan.MOVIE_SEEN, pyscan.MOVIE_UNSEEN
# pyscan.create_dicts('movie_plist/tests/videos_test/')
# c_d.create_dicts()

# url, synopsis, path_to = list(movie_unseen.values())[0]
url, path_to = list(pyscan.MOVIE_UNSEEN.values())[0]

str_params = [
    ('Shawshank Redemption, the 1994', pyscan.MOVIE_UNSEEN.keys()),
    ('https://www.imdb.com/title/tt0111161/', url),
    # (synopsis_text, synopsis),
    ('movie_plist/tests/videos_test/Shawshank Redemption, the 1994', path_to)
]


@pytest.mark.parametrize("a,b", str_params)
def test_dict(a, b):
    assert a in b


size_params = [
    (len(pyscan.MOVIE_UNSEEN), 1),
    (len(pyscan.MOVIE_SEEN), 0)
]


@pytest.mark.parametrize("a,b", size_params)
def test_dict_size(a, b):
    assert a == b


def test_url_raises():
    with pytest.raises(Exception):
        pyscan.create_dicts('movie_plist/tests/url_test/')
