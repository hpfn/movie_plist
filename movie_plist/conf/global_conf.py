import json
import os

# user
home_user = os.environ['HOME']
# first, main path
MOVIE_PLIST_CACHE = os.path.join(home_user, '.cache/movie_plist')
MOVIE_PLIST_STUFF = os.path.join(home_user, '.config/movie_plist')
CFG_FILE = os.path.join(MOVIE_PLIST_STUFF, 'movie_plist.cfg')
SEEN_JSON_FILE = os.path.join(MOVIE_PLIST_STUFF, 'seen_movies.json')
UNSEEN_JSON_FILE = os.path.join(MOVIE_PLIST_STUFF, 'unseen_movies.json')


def check_movie_plist_dirs():
    if not os.path.isdir(MOVIE_PLIST_CACHE):
        os.system('/bin/mkdir -p ' + MOVIE_PLIST_CACHE)

    if not os.path.isdir(MOVIE_PLIST_STUFF):
        os.system('/bin/mkdir -p ' + MOVIE_PLIST_STUFF)


def load_from_json(json_file):
    if os.path.isfile(json_file):
        with open(json_file) as json_data:
            return json.load(json_data)

    return dict()


MOVIE_SEEN = load_from_json(SEEN_JSON_FILE)
MOVIE_UNSEEN = load_from_json(UNSEEN_JSON_FILE)


def dump_json_movie(movie_dic, json_file):
    with open(json_file, 'w') as outfile:
        json.dump(movie_dic, outfile)
