import sqlite3
import os


class DataStorage:
    def __init__(self):
        self.conn = sqlite3.connect('movie_plist_sqlite3.db')
        self.c = self.conn.cursor()

        if os.path.getsize('movie_plist_sqlite3.db') is 0:
            print("zero size. building a .db file")
            self.c.execute('''create table movie_plist (url UNIQUE,
                           title_year TEXT, director,
                           writers_list, actors_list,
                           snps_txt TEXT, path, moviefile, watch INTEGER)''')
            self.conn.commit()

    def insert_data(self, data_s):
        """ data_s will have seven itens """
        self.c.execute('insert into movie_plist values (?,?,?,?,?,?,?,?,?)', data_s)
        self.conn.commit()

    def populate_db(self, url, path, moviefile, movie):
        # m_poster is not going to database !!!
        # m_poster = movie.movie_poster()
        title_year = movie.title_year()
        # rate_votes does not go to database !!!
        # rate_votes = movie.rate_value_and_votes()
        director = movie.director()
        writers_list = movie.creator_writers()
        actors_list = movie.actors()
        snps_txt = movie.synopsis()

        wrt_str = ""
        for w in writers_list:
            wrt_str = wrt_str + w + " "

        actr_str = ""
        for a in actors_list:
            actr_str = actr_str + a + " "

        m_data = [url, title_year, director, wrt_str, actr_str, snps_txt, path, moviefile, 0]
        self.insert_data(m_data)

    def show_data(self):
        self.c.execute('select * from movie_plist')
        return list(self.c.fetchall())

    def check_movie(self):
        self.c.execute('select url from movie_plist')
        return str(self.c.fetchall())

    def exit_from_db(self):
        self.c.close()
