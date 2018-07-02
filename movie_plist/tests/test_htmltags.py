from movie_plist.html_file.htmltags import HtmlTags


def test_htmltags_class(mocker):
    mocker.patch.object(HtmlTags, '_retrieve_data', value=None)

    url = 'http://www.example.com'
    _html_page = HtmlTags(url)
    # Message in _synopsis which come from pimdbdata should
    # not be here because of mocker
    assert 'Maybe something is wrong' not in _html_page.context
    assert url in _html_page.context
