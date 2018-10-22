import os
import textwrap
from unittest.mock import patch

import pytest

from movie_plist.data import pimdbdata
from movie_plist.data.pimdbdata import ParseImdbData

expected = [

    hasattr(pimdbdata, 'BeautifulSoup'),
    hasattr(pimdbdata.ParseImdbData, 'synopsis'),
    hasattr(pimdbdata.ParseImdbData, '_do_poster_png_file'),
    hasattr(pimdbdata.ParseImdbData, '_save_poster_file'),
    hasattr(pimdbdata.ParseImdbData, '_poster_file'),
    hasattr(pimdbdata.ParseImdbData, '_poster_url'),

]


@pytest.mark.parametrize('e', expected)
def test_init_mocked_attrs(e):
    assert e


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
                        return_value=b'tests/Shawshank_Redemption_1994.png')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    title = 'Shawshank Redemption 1994'
    return ParseImdbData('file://' + html_path, title)


# def test_init_title_year(run_init):
#    assert 'Um Sonho de Liberdade (1994)' == run_init.title_year()


def test_init_synopsys(run_init):
    synopsys = [
        'Directed by Frank Darabont.  With Tim Robbins, Morgan Freeman,',
        'Bob Gunton, William Sadler. Two imprisoned men bond over a number',
        'of years, finding solace and eventual redemption through acts of',
        'common decency.'
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


def test_poster_name(run_init):
    file_name = run_init.cache_poster.rpartition('/')
    assert file_name[-1] == 'Shawshank_Redemption_1994.png'


@patch('movie_plist.data.pimdbdata.QImage')
def test_do_save_poster_steps(img_mock, run_init, mocker):
    mocker.patch.object(os.path, 'isfile', return_value=False)
    run_init._do_poster_png_file()
    assert img_mock.call_count == 1
    img_mock.assert_has_calls(img_mock.loadFromData)
    img_mock.assert_has_calls(img_mock.save)


@patch('movie_plist.data.pimdbdata.QImage')
def test_do_not_save_poster_steps(img_mock, run_init, mocker):
    mocker.patch.object(os.path, 'isfile', return_value=True)
    run_init._do_poster_png_file()
    assert img_mock.call_count == 0
    img_mock.loadFromData.assert_not_called()
    img_mock.save.assert_not_called()
