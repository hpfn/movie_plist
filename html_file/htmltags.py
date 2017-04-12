# -*- coding: utf-8 -*-
"""
   
"""

import urllib.request

from data import pimdbdata


class HtmlTags:
    def __init__(self, url, synopsis):
        self.url = url
        self.synopsis = synopsis
        self.context = ''

        self.top_header()
        self.inside_table()
        self.bottom_tags()

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
                place = s_list[x:].index(i)
                s_list[x+place] = '<br>'
                x *= 2
                y = x
            else:
                y += 1
            #if y > list_size: break

        # print("<tr valign=\"top\">", file=self.open_file)
        self.context += "<td>\n<img src=\"/tmp/picture.png\"></td>"

        self.context += "<td width=\"70\">"
        self.context += ''.join(s_list)
        self.context += "<br>"
        # self.context += self.synopsis + "<br>"
        self.context += "<a href=\"" + self.url + "\">imdb</a><br>"
        self.context += "</td>"

    def bottom_tags(self):
        """ from </table> to </html> """
        self.context += "</table><input type=submit value=\"Submit\"></form></body>\n</html>"
