#!/usr/bin/python3
# -*- coding: utf-8 -*-

# how to pass the path to .html file
# how to update the seen list on combobox
# with a module ?
from info_in_db.movie_plist_sqlite3 import DataStorage
import time
import cgi
import cgitb

cgitb.enable()


def start_response(resp="text/html"):
    return 'Content-type: ' + resp + '\n\n'


def head():
    html_to_body = ("<html>\n<head>\n"
                    "<meta http-equiv=\"Content-Type\" content=\"text/html_file; charset=utf-8\">\n"
                    "<title>Py Movie Info</title>\n"
                    "</head>\n<body>\n")
    return html_to_body


def footer():
    return "<p>Please, wait a few seconds, right click on mouse and 'Go Back'</p></body>\n</html>"


def edit_html(movie_title):
    start_line = ''
    end_line = ''
    count = 0
    with open('/home/zaza/Vídeos/index.html', 'r') as html_file:
        html_file_lines = html_file.readlines()

    mark_start = 'start ' + movie_title
    mark_end = 'end ' + movie_title
    for unwanted in html_file_lines:
        if mark_start in unwanted:
            start_line = count
        if mark_end in unwanted:
            end_line = count
        count += 1

    print("remove from {} to {}" .format(start_line, end_line))
    del html_file_lines[start_line:end_line+1]

    f = open('/home/zaza/Vídeos/index.html', 'w')
    f.writelines(html_file_lines)
    f.close()


form_data = cgi.FieldStorage()
movie = form_data.getvalue("title_year")
stored_data = DataStorage()

print(start_response())
print('')
print(head())
print('')
if isinstance(movie, list):
    for i in movie:
        print('<p>')
        print("Marking {} as Seen on db...".format(i))
        print('</p>')
        stored_data.update_movie_watch('1', i)
        edit_html(i)
        time.sleep(1)
else:
    print('<p>')
    print("Marking {} as Seen on db...".format(movie))
    print('</p>')
    stored_data.update_movie_watch('1', movie)
    edit_html(movie)
    time.sleep(1)
time.sleep(2)
print(footer())
