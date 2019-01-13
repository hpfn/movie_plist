import os
from unittest.mock import patch

import pytest

from movie_plist.data import pimdbdata
from movie_plist.data.pimdbdata import ParseImdbData

expected = [

    hasattr(pimdbdata, 'BeautifulSoup'),
    hasattr(pimdbdata, 'MOVIE_SEEN'),
    hasattr(pimdbdata, 'MOVIE_UNSEEN'),
    hasattr(pimdbdata, 'MOVIE_PLIST_CACHE'),
    # inside init
    # hasattr(pimdbdata.ParseImdbData, 'synopsis'),
    # hasattr(pimdbdata.ParseImdbData, 'cache_poster'),
    # methods
    hasattr(pimdbdata.ParseImdbData, 'synopsis_exists'),
    hasattr(pimdbdata.ParseImdbData, 'bs4_synopsis'),
    hasattr(pimdbdata.ParseImdbData, 'add_synopsis'),
    hasattr(pimdbdata.ParseImdbData, 'dict_movie_choice'),
    hasattr(pimdbdata.ParseImdbData, '_do_poster_png_file'),
    hasattr(pimdbdata.ParseImdbData, '_save_poster_file'),
    hasattr(pimdbdata.ParseImdbData, '_poster_file'),
    hasattr(pimdbdata.ParseImdbData, '_poster_url'),
]


@pytest.mark.parametrize('e', expected)
def test_init_mocked_attrs(e):
    assert e


@pytest.fixture()
def init_mocked(mocker):
    """
    For whatever reason bs4 returns nothing
    """
    mocker.patch.object(pimdbdata, 'MOVIE_PLIST_CACHE', return_value='home/.cache/movie_plist')
    mocker.patch.object(pimdbdata, 'BeautifulSoup', return_value=None)
    return ParseImdbData('url', 'title')


def test_synopsis(init_mocked):
    assert 'Maybe something is wrong' in init_mocked.synopsis


def test_poster_url(init_mocked):
    assert 'https://static.significados.com.br/' in init_mocked._poster_url()


@pytest.fixture
def run_init(mocker):
    """
    new movie scanned
    """
    mocker.patch.object(ParseImdbData, '_poster_file',
                        return_value=b'tests/Shawshank_Redemption_1994.png')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    title = 'Shawshank Redemption 1994'
    return ParseImdbData('file://' + html_path, title)


# def test_init_title_year(run_init):
#    assert 'Um Sonho de Liberdade (1994)' == run_init.title_year()


def test_init_synopsys(run_init):
    synopsys = 'Directed by Frank Darabont.  With Tim Robbins, Morgan Freeman, '
    synopsys += 'Bob Gunton, William Sadler. Two imprisoned men bond over a number '
    synopsys += 'of years, finding solace and eventual redemption through acts of '
    synopsys += 'common decency.'

    assert synopsys == run_init.synopsis


def test_init_poster_url(run_init):
    poster_url = 'https://m.media-amazon.com/images/'
    poster_url += 'M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFm'
    poster_url += 'NTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU'
    poster_url += '@._V1_UX182_CR0,0,182,268_AL_.jpg'
    assert poster_url == run_init._poster_url()


def test_poster_name(run_init):
    file_name = run_init.cache_poster.rpartition('/')
    assert file_name[-1] == 'Shawshank_Redemption_1994.png'


@patch('movie_plist.data.pimdbdata.ParseImdbData._do_poster_png_file')
@patch('movie_plist.data.pimdbdata.ParseImdbData.bs4_synopsis')
def test_description_content(bs4_synopsis, do_poster_file, mocker):
    """
    What happens when synopsis does not exists
    """
    mocker.patch.object(pimdbdata, 'BeautifulSoup', return_value=str())
    mocker.patch.object(ParseImdbData, 'synopsis_exists', return_value=False)
    obj = ParseImdbData('url', 'title')
    # does not check what the method does. only what it calls
    assert isinstance(obj.soup, str)
    assert bs4_synopsis.call_count == 1
    assert do_poster_file.call_count == 1


@patch('movie_plist.data.pimdbdata.ParseImdbData.add_synopsis')
def test_add_synopsis_attr(add, run_init):
    """
    When synopsis does not exists bs4_synopsis calls add_synopsis
    """
    run_init.bs4_synopsis()
    assert add.call_count == 1


@patch('movie_plist.data.pimdbdata.ParseImdbData.dict_movie_choice')
def test_choice_no_made(choice, run_init):
    """
    json data does not have a record of the new movie
    no choice can be made
    the method works for old records
    """
    run_init.add_synopsis()
    assert choice.call_count == 0
    assert run_init.title not in pimdbdata.MOVIE_UNSEEN


def test_synopsis_exists():
    """
    Synopsis exists. Do nothing.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pimdbdata.MOVIE_PLIST_CACHE = os.path.join(base_dir, 'tests/.cache')
    pimdbdata.MOVIE_UNSEEN = dict(
        title=('/root', 'synopsis', 'any_path')
    )

    obj = ParseImdbData('url', 'title')
    # soup attr only exists if there is no synopsis
    assert not hasattr(obj, 'soup')
    assert obj.synopsis == 'synopsis'
    assert obj.cache_poster.endswith('movie_plist/tests/.cache/title.png')


def test_choice_unseen(run_init):
    """
    A record exists and it goes to an unseen movie dict
    """
    pimdbdata.MOVIE_UNSEEN[run_init.title] = ('root/',)
    run_init.bs4_synopsis()
    assert 'Directed' in pimdbdata.MOVIE_UNSEEN[run_init.title][1]
    del pimdbdata.MOVIE_UNSEEN[run_init.title]


def test_choice_seen(run_init):
    """
    A record exists and it goes to a seen movie dict
    """
    pimdbdata.MOVIE_SEEN[run_init.title] = ('root/',)
    run_init.bs4_synopsis()
    assert 'Directed' in pimdbdata.MOVIE_SEEN[run_init.title][1]
    del pimdbdata.MOVIE_SEEN[run_init.title]


@patch('movie_plist.data.pimdbdata.ParseImdbData._save_poster_file')
def test_do_save_poster_call(save_file, run_init, mocker):
    """
    There is no poster yet. Create one and save it
    What is done when _save_poster_file is called
    """
    mocker.patch.object(os.path, 'isfile', return_value=False)
    run_init._do_poster_png_file()
    assert save_file.call_count == 1


@patch('movie_plist.data.pimdbdata.QImage')
def test_do_save_poster_steps(img_mock, run_init):
    """
    There is no poster yet. Create one and save it
    What is done when _save_poster_file is called
    """
    run_init._save_poster_file()
    assert img_mock.call_count == 1
    img_mock.assert_has_calls(img_mock.loadFromData)
    img_mock.assert_has_calls(img_mock.save)


@patch('movie_plist.data.pimdbdata.ParseImdbData._save_poster_file')
def test_do_not_save_poster_steps(save_file, run_init, mocker):
    """
    A poster exists. Do nothing.
    """
    mocker.patch.object(os.path, 'isfile', return_value=True)
    run_init._do_poster_png_file()
    assert save_file.call_count == 0
