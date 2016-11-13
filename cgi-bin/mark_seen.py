#!/usr/bin/python3

import cgi
import cgitb
cgitb.enable()

def start_response(resp="text/html"):
    return('Content-type: ' + resp + '\n\n')

form_data = cgi.FieldStorage()
movie = form_data.getvalue("title_year")

print(start_response())
print("{}" .format(movie))
