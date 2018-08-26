import os

import pytest

from movie_plist.html_file.htmltags import HtmlTags


def test_htmltags_class(mocker):
    mocker.patch.object(HtmlTags, '_retrieve_data', value=None)

    url = 'http://www.example.com'
    _html_page = HtmlTags(url)
    # Message in _synopsis which come from pimdbdata should
    # not be here because of mocker
    assert 'Maybe something is wrong' not in _html_page.context
    assert url in _html_page.context


# Kind of integration tests with pimdbdata
@pytest.fixture
def build_obj():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    return HtmlTags('file://' + html_path)


def test_context_has_img_html_tag(build_obj):
    assert "<img src=\"/tmp/picture.png\">" in build_obj.context


def test_context_has_url(build_obj):
    assert "<a href=\"" in build_obj.context


def test_context_has_synopsys(build_obj):
    synopsys = [
        'Directed by Frank Darabont.  With Tim Robbins, Morgan Freeman, Bob',
        'Gunton, William Sadler. Two imprisoned men bond over a number of',
        'years, finding solace and eventual redemption through acts of common',
        'decency.'
    ]
    synopsys_parsed = build_obj._synopsis.split('<br />')
    assert synopsys == synopsys_parsed
