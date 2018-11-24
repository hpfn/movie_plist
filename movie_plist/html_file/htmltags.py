# -*- coding: utf-8 -*-
import textwrap

from movie_plist.data import pimdbdata


class HtmlTags:
    def __init__(self, url, title):
        self._url = url
        self.title = title
        self._poster_path = ''
        self.context = ''
        self._synopsis = ''

        self._retrieve_data()
        self._build_html()

    def _retrieve_data(self):
        self._get_synopsis()
        self._wrap_synopsis()

    def _build_html(self):
        self._top_header()
        self._inside_table()
        self._bottom_tags()

    def _get_synopsis(self):
        html_movie = pimdbdata.ParseImdbData(self._url, self.title)
        self._poster_path = html_movie.cache_poster
        self._synopsis = html_movie.synopsis

    def _wrap_synopsis(self):
        self._synopsis = '<br />'.join(textwrap.wrap(self._synopsis))

    def _top_header(self):
        """ from <html> tag until <table> tag """
        self.context = (
            "<html><head>"
            "<meta http-equiv=\"Content-Type\" content=\"text/html_file; charset=utf-8\">"
            "</head><body>"
            "<table>"
        )

    def _inside_table(self):
        """
        '/tmp/picture.png' hardcoded - see pimdbdata.ParseImdbData
        """
        self.context += "<td>\n<img src=\"" + self._poster_path + "\"></td>"
        self.context += "<td width=\"70\">"
        self.context += self._synopsis + "<br>"
        self.context += "<a href=\"" + self._url + "\">imdb</a><br>"
        self.context += "</td>"

    def _bottom_tags(self):
        """ from </table> to </html> """
        self.context += "</table></body>\n</html>"
