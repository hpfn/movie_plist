from bs4 import BeautifulSoup
import re


class ParseImdbData(object):
    def __init__(self, html):
        """ html is the url to be parsed """
        self.soup = BeautifulSoup(html, 'html.parser')

    def title_year(self):
        """
        :rtype:

        """
        return self.soup.title.string[:-7]

    def rate_value_and_votes(self):
        """

        :rtype: list() - two items
        """
        try:
            rate_value = self.soup.find(itemprop="ratingValue")
            rate_count = self.soup.find(itemprop="ratingCount")
            return [rate_value.contents[0], rate_count.contents[0]]
        except AttributeError:
            print('{}: no contents for rate and votes' .format(self.soup.title.string[:-7]))
            return ['?', '?']

    def director(self):
        try:
            director = self.soup.find(itemprop="director")
            re_director = re.compile("([A-Z].*[a-z])</span></a>.*")
            result = re_director.search(str(director.contents[1]))
            return result.group(1)
        except AttributeError:
            print('{}: must improve search to find the director' .format(self.soup.title.string[:-7]))
            return " ? "

    def creator_writers(self):
        """
        :rtype: list()
        """
        try:
            writer_cia = self.soup.find_all(itemprop="creator", itemtype="http://schema.org/Person")
            re_writer_cia = re.compile("([A-Z].*[a-z])</span></a>.*")
            writers = list()
            for i in writer_cia:
                result = re_writer_cia.search(str(i))
                writers.append(result.group(1))
            return writers
        except AttributeError:
            print('{}: must improve search to find the writers' .format(self.soup.title.string[:-7]))
            return " ? "

    def actors(self):
        """
        :rtype: list()
        """
        actors_cia = self.soup.find_all(itemprop="actors", itemtype="http://schema.org/Person")
        re_actors = re.compile("([A-Z].*[a-z])</span></a>.*")

        actors = list()
        for i in actors_cia:
            result = re_actors.search(str(i))
            actors.append(result.group(1))

        actors.append(" and others")
        return actors

    def synopsis(self):
        description = self.soup.find(itemprop="description")
        raw_txt = description.contents[0].strip()
        # maybe split() is better than this
        # count = 0
        # for i in raw_txt:
        #     if count < 70 or i is not ' ':
        #         print(i, end='')
        #     else:
        #         if i is ' ':
        #             print()
        #             count = 0
        #             continue
        #    count += 1

        # print()
        return raw_txt

    def movie_poster(self):
        poster = self.soup.find(itemprop="image")
        re_poster = re.compile("http.*\.jpg")
        result = re_poster.search(str(poster))
        return result.group(0)
