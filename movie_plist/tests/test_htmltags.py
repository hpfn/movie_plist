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
        ' The Shawshank Redemption is a highly-acclaimed movie starring Tim',
        'Robbins and Morgan Freeman. Andy Dufresne is convicted of the murder',
        'of his wife and her lover, and sentenced to life imprisonment at',
        'Shawshank prison. Life seems to have taken a turn for the worse, but',
        'fortunately Andy befriends some of the other inmates, in particular a',
        'character known only as Red. Over time Andy finds ways to live out',
        'life with relative ease as one can in a prison, leaving a message for',
        'all that while the body may be locked away in a cell, the spirit can',
        'never be truly imprisoned.',
    ]
    synopsys_parsed = build_obj._synopsis.split('<br />')
    assert synopsys == synopsys_parsed
