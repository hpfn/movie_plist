# import sys
# import os
# sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from movie_plist.data.pimdbdata import ParseImdbData  # noqa: E402


# usar pytest.fixture ?

def test_synopsis(mocker):
    # mocker just mock methods, no attrs
    # mocker.patch.object(ParseImdbData, 'BeautifulSoup', value=None)
    mocker.patch.object(ParseImdbData, '__init__', return_value=None)

    test_synopsis = ParseImdbData('http://www.example.com')
    except_msg = test_synopsis.synopsis()
    assert 'Maybe something is wrong' in except_msg


def test_poster_url(mocker):
    mocker.patch.object(ParseImdbData, '__init__', return_value=None)

    test_poster = ParseImdbData()
    poster_url = test_poster._poster_url()
    assert 'https://static.significados.com.br/' in poster_url
