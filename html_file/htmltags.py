# -*- coding: utf-8 -*-
"""
   
"""

import urllib.request
import urllib.request
from PyQt5.QtGui import QImage
from data import pimdbdata


class HtmlTags:
    def __init__(self, url):
        self.url = url
        self.context = ''
        self.synopsis = ''

        self.first_steps()
        self.top_header()
        self.inside_table()
        self.bottom_tags()

    def first_steps(self):
        html = urllib.request.urlopen(self.url).read()
        movie = pimdbdata.ParseImdbData(html)

        self.synopsis = movie.synopsis()

        poster = movie.movie_poster()
        img = QImage()  # (8,10,4)
        data = urllib.request.urlopen(poster).read()
        img.loadFromData(data)
        img.save('/tmp/picture.png')

    def top_header(self):
        """ from <html> tag until <table> tag """
        self.context = ("<html><head>"
                        "<meta http-equiv=\"Content-Type\" content=\"text/html_file; charset=utf-8\">"
                        "</head><body>"
                        "<table>")

    def inside_table(self):
        """
        
        """
        x = 60
        y = 60
        s_list = list(self.synopsis)
        list_size = len(s_list)
        for i in s_list[x:]:
            if i is ' ' and y < list_size:
                try:
                    place = s_list[x:].index(i)
                    s_list[x + place] = '<br>'
                    x *= 2
                    y = x
                except ValueError:
                    print("Please, fix the way the synopsis is formated")
            else:
                y += 1

        self.synopsis = ''.join(s_list)

        self.context += "<td>\n<img src=\"/tmp/picture.png\"></td>"

        self.context += "<td width=\"70\">"
        self.context += self.synopsis + "<br>"
        self.context += "<a href=\"" + self.url + "\">imdb</a><br>"
        self.context += "</td>"

    def bottom_tags(self):
        """ from </table> to </html> """
        self.context += "</table><input type=submit value=\"Submit\"></form></body>\n</html>"
