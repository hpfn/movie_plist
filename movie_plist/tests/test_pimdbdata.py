# import sys
# import os
# sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
import os

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


def test_dunder_init(mocker):
    mocker.patch.object(ParseImdbData, '_poster_file',
                        return_value=b'tests/Shawshank_Redemption-1994.png')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    test_class = ParseImdbData('file://'+html_path)
    assert 'Um Sonho de Liberdade (1994)' == test_class.title_year()
    synopsys = [
        'The Shawshank Redemption is a highly-acclaimed movie starring',
        'Tim Robbins and Morgan Freeman. Andy Dufresne is convicted of',
        'the murder of his wife and her lover, and sentenced to life',
        'imprisonment at Shawshank prison. Life seems to have taken a turn',
        'for the worse, but fortunately Andy befriends some of the other',
        'inmates, in particular a character known only as Red. Over time',
        'Andy finds ways to live out life with relative ease as one can in',
        'a prison, leaving a message for all that while the body may be',
        'locked away in a cell, the spirit can never be truly imprisoned.',
    ]
    synopsys_parsed = test_class.synopsis()

    for txt in synopsys:
        assert txt in synopsys_parsed

    poster_url = 'https://m.media-amazon.com/images/'
    poster_url += 'M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFm'
    poster_url += 'NTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU'
    poster_url += '@._V1_UX182_CR0,0,182,268_AL_.jpg'

    assert poster_url == test_class._poster_url()

    assert test_class._do_poster_png_file() is None
