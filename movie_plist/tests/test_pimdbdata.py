import os
import textwrap
import pytest
from unittest.mock import patch
from movie_plist.data.pimdbdata import ParseImdbData


@pytest.fixture
def init_mocked(mocker):
    mocker.patch.object(ParseImdbData, '__init__', return_value=None)
    return ParseImdbData()


def test_synopsis(init_mocked):
    init_mocked.url = 'http://www.example.com'
    assert 'Maybe something is wrong' in init_mocked.synopsis()


def test_poster_url(init_mocked):
    assert 'https://static.significados.com.br/' in init_mocked._poster_url()


@pytest.fixture
def run_init(mocker):
    mocker.patch.object(ParseImdbData, '_poster_file',
                        return_value=b'tests/Shawshank_Redemption-1994.png')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    return ParseImdbData('file://' + html_path)


def test_init_title_year(run_init):
    assert 'Um Sonho de Liberdade (1994)' == run_init.title_year()


def test_init_synopsys(run_init):
    synopsys = [
        ' The Shawshank Redemption is a highly-acclaimed movie starring',
        'Tim Robbins and Morgan Freeman. Andy Dufresne is convicted of the',
        'murder of his wife and her lover, and sentenced to life',
        'imprisonment at Shawshank prison. Life seems to have taken a turn',
        'for the worse, but fortunately Andy befriends some of the other',
        'inmates, in particular a character known only as Red. Over time',
        'Andy finds ways to live out life with relative ease as one can in',
        'a prison, leaving a message for all that while the body may be',
        'locked away in a cell, the spirit can never be truly imprisoned.',
    ]
    synopsys_parsed = run_init.synopsis()
    synopsys_parsed = textwrap.wrap(synopsys_parsed, width=65)
    assert synopsys == synopsys_parsed


def test_init_poster_url(run_init):
    poster_url = 'https://m.media-amazon.com/images/'
    poster_url += 'M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFm'
    poster_url += 'NTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU'
    poster_url += '@._V1_UX182_CR0,0,182,268_AL_.jpg'
    assert poster_url == run_init._poster_url()


@patch('movie_plist.data.pimdbdata.QImage')
def test_do_save_poster_steps(img_mock, run_init):
    run_init._do_poster_png_file()
    assert img_mock.call_count == 1
    img_mock.assert_has_calls(img_mock.loadFromData)
    img_mock.assert_has_calls(img_mock.save)
