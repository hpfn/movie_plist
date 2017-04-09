import sqlite3
# import urllib.request
# from data import pimdbdata
import conf.global_conf

# http://stackoverflow.com/questions/21360271/pythons-sqlite3-module-exceptions-where-is-the-documentation
# https://www.python.org/dev/peps/pep-0249/#exceptions
# http://pythoncentral.io/introduction-to-sqlite-in-python/
# http://zetcode.com/db/sqlitepythontutorial/
class DataStorage(object):
    def __init__(self):
        try:
            path_to_db = conf.global_conf.movie_plist_stuff
            db_file = path_to_db + '/movile_plist-sqlite3.db'
            self.conn = sqlite3.connect(db_file)
            self.c = self.conn.cursor()
            self.c.execute('''create table if not exists movie_plist
            (url UNIQUE)''')
            self.conn.commit()
        except sqlite3.Error as err:
            if self.conn:
                self.conn.rollback()
            raise err

    def insert_data(self, url):
        """
         """
        try:
            with self.conn:
                # html = urllib.request.urlopen(url).read()
                # movie = pimdbdata.ParseImdbData(html)
                # m_data = [url, movie.title_year(), path]
                self.conn.execute('insert into movie_plist values (?)', url)
                self.conn.commit()
                return m_data
        except sqlite3.IntegrityError:
            if self.conn:
                self.conn.rollback()
            print("Record already exists")

    def movie_url(self):
        self.c.execute("select url from movie_plist")
        return str(self.c.fetchall())

    def movie_delete(self, url):
        self.conn.execute("delete from movie_plist where url=? ", (url))
        self.conn.commit()

    def exit_from_db(self):
        self.conn.close()
