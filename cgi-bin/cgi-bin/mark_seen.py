#!/usr/bin/python3
# -*- coding: utf-8 -*-

# how to update the seen list on combobox
from html_file.edit_html import EditHtml
from info_in_db.movie_plist_sqlite3 import DataStorage
# from html_file.remove_movie import EditHtmlRemove
# import time
import cgi
import cgitb
cgitb.enable()


def start_response(resp="text/html"):
    return 'Content-type: ' + resp + '\n\n'


def head():
    html_to_body = ("<html>\n<head>\n"
                    "<meta http-equiv=\"Content-Type\" content=\"text/html_file; charset=utf-8\">\n"
                    "<meta http-equiv=\"refresh\" content=\"5; URL=../index.html\">\n"
                    "<title>Py Movie Info</title>\n"
                    "</head>\n<body>\n")
    return html_to_body


def footer():
    return "<p>Please, wait a few seconds...</p></body>\n</html>"

form_data = cgi.FieldStorage()
movie = form_data.getvalue("title_year")
stored_data = DataStorage()
no_movie_file_yet_list = str(stored_data.no_movie_yet())

print(start_response())
print('')
print(head())
print('')
e_html = EditHtml()
if isinstance(movie, list):
    for i in movie:
        if i in no_movie_file_yet_list:
            continue
        else:
            print('<p>')
            print("Marking {} as Seen on db...".format(i))
            print('</p>')
            stored_data.update_movie_watch('1', i)
            e_html.remove_m_html(i)

else:
    if movie in no_movie_yet_list:
        pass
    else:
        print('<p>')
        print("Marking {} as Seen on db...".format(movie))
        print('</p>')
        stored_data.update_movie_watch('1', movie)
        e_html.remove_m_html(movie)

print(footer())
