# -*- coding: utf-8 -*-
"""
   
"""

import urllib.request
import urllib.error
import textwrap
from socket import timeout
from PyQt5.QtGui import QImage
from data import pimdbdata


class HtmlTags:
    def __init__(self, url):
        self.url = url
        self.context = ''
        self.synopsis = ''
        self.html = ''
        self.movie = ''

        self.retrieve_data()
        self.build_html()

    def retrieve_data(self):
        self.get_html()
        self.parse_html()
        self.get_synopsis()
        self.wrap_synopsis()
        self.do_poster_png_file()

    def build_html(self):
        self.top_header()
        self.inside_table()
        self.bottom_tags()

    def get_html(self):
        try:
            self.html = urllib.request.urlopen(self.url, timeout=3).read()
        except urllib.error.URLError:
            self.context = "HTML - URLError. Try again."
        except timeout:
            self.context = "HTML - Connection timeout. Try again."
        except ValueError:
            self.context = "HTML - Please, check the .desktop file for this movie."

    def parse_html(self):
        self.movie = pimdbdata.ParseImdbData(self.html)

    def get_synopsis(self):
        self.synopsis = self.movie.synopsis()

    def wrap_synopsis(self):
        self.synopsis = '<br />'.join(textwrap.wrap(self.synopsis))

    def do_poster_png_file(self):
        poster = self.movie.movie_poster()
        try:
            data = urllib.request.urlopen(poster).read()
        except urllib.error.URLError:
            self.context = "Poster - URLError. Try again."
        except timeout:
            self.context = "Poster - Connection timeout. Try again."

        img = QImage()  # (8,10,4)
        img.loadFromData(data)
        img.save('/tmp/picture.png')

    def top_header(self):
        """ from <html> tag until <table> tag """
        self.context = ("<html><head>"
                        "<meta http-equiv=\"Content-Type\" content=\"text/html_file; charset=utf-8\">"
                        "</head><body>"
                        "<table>")

    def inside_table(self):
        self.context += "<td>\n<img src=\"/tmp/picture.png\"></td>"
        self.context += "<td width=\"70\">"
        self.context += self.synopsis + "<br>"
        self.context += "<a href=\"" + self.url + "\">imdb</a><br>"
        self.context += "</td>"

    def bottom_tags(self):
        """ from </table> to </html> """
        self.context += "</table><input type=submit value=\"Submit\"></form></body>\n</html>"

