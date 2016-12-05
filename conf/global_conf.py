import os
from pathlib import Path
from subprocess import call, Popen

# user
user_name = os.environ['USER']
# path to httpd, index.html,  cgi, sqlite3.db
# first, main path
movie_plist_stuff = '/home/' + user_name + '/.config/movie_plist'
movie_plist_stuff_html_dir = movie_plist_stuff + '/html_dir'

# links to be created
movie_plist_stuff_cgi_dir = movie_plist_stuff_html_dir + '/cgi-bin'
movie_plist_stuff_httpd = movie_plist_stuff_html_dir + '/simple_httpd.py'

# link target
target_cgi_dir = '/home/' + user_name + '/Documentos/Programacao/python/movie_plist/cgi-bin/cgi-bin'
target_httpd = '/home/' + user_name + '/Documentos/Programacao/python/movie_plist/cgi-bin/simple_httpd.py'

# complete link command
target_to_cgi = '/bin/ln -s ' + target_cgi_dir + ' ' + movie_plist_stuff_cgi_dir
target_httpd_file = '/bin/ln -s ' + target_httpd + ' ' + movie_plist_stuff_httpd

# if path to movie_plist does not exist create one
check_path = Path(movie_plist_stuff)
if not check_path.is_dir():
    os.system('/bin/mkdir -p ' + movie_plist_stuff_html_dir)
    os.system(target_to_cgi)
    os.system(target_httpd_file)

# httpd port
PORT = 8123

# skip url part
