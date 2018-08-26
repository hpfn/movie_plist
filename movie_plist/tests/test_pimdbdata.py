import os
import textwrap
from unittest.mock import patch

import pytest

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


@patch('movie_plist.data.pimdbdata.QImage')
def test_do_save_poster_steps(img_mock, run_init):
    run_init._do_poster_png_file()
    assert img_mock.call_count == 1
    img_mock.assert_has_calls(img_mock.loadFromData)
    img_mock.assert_has_calls(img_mock.save)
