# import pytest
# from pytest_mock import mocker
# import mock
# from unittest.mock import patch
# import sys
# import os
# sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from movie_plist.html_file.htmltags import HtmlTags  # noqa: E402


# @patch('html_file.htmltags.HtmlTags._retrieve_data')
def test_htmltags_class(mocker):
    # html_patch.value = None
    mocker.patch.object(HtmlTags, '_retrieve_data', value=None)

    url = 'http://www.example.com'
    _html_page = HtmlTags(url)
    # Message in _synopsis which come from pimdbdata should
    # not be here because of mocker
    assert 'Maybe something is wrong' not in _html_page.context
    assert url in _html_page.context
