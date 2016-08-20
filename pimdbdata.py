from bs4 import BeautifulSoup
import re


class ParseImdbData:
    def __init__(self, html):
        """ html is the url to be parsed """
        self.soup = BeautifulSoup(html, "lxml")

    def title_year(self):
        """
        :rtype: list() - two items # not anymore. simplicity is better :)

        """
        return self.soup.title.string[:-7]
        # title_year = self.soup.find(property="og:title")
        # print("propert: {}" .format(self.soup.title.string[:-6]))
        # name = self.soup.find(itemprop="name")
        # print("title: {}" .format(name.contents[0]), end=' ')
        # year = self.soup.find(id="titleYear")
        # re_year = re.compile("([0-9]+)")
        # year = re_year.search(str(name.contents[1]))
        # print(year.group())
        # return [name.contents[0].strip(), year.group()]

    def rate_value_and_votes(self):
        """

        :rtype: list() - two items
        """
        rate_value = self.soup.find(itemprop="ratingValue")
        # print("rate: {}" .format(rate_value.contents[0]))
        rate_count = self.soup.find(itemprop="ratingCount")
        # print("votes: {}" .format(rate_count.contents[0]))
        return [rate_value.contents[0], rate_count.contents[0]]

    def director(self):
        director = self.soup.find(itemprop="director")
        re_director = re.compile("([A-Z].*[a-z])</span></a>.*")
        result = re_director.search(str(director.contents[1]))
        # print("director: {}" .format(result.group(1)))
        return result.group(1)

    def creator_writers(self):
        """
        :rtype: list()
        """
        writer_cia = self.soup.find_all(itemprop="creator", itemtype="http://schema.org/Person")
        re_writer_cia = re.compile("([A-Z].*[a-z])</span></a>.*")
        # print("Writers: ", end=' ')
        writers = list()

        for i in writer_cia:
            result = re_writer_cia.search(str(i))
            # print(result.group(1), end="  ")
            writers.append(result.group(1))

        # print()
        return writers

    def actors(self):
        """
        :rtype: list()
        """
        actors_cia = self.soup.find_all(itemprop="actors", itemtype="http://schema.org/Person")
        re_actors = re.compile("([A-Z].*[a-z])</span></a>.*")
        # print("Actors: ", end=' ')
        actors = list()
        for i in actors_cia:
            result = re_actors.search(str(i))
            # print(result.group(1), end="  ")
            actors.append(result.group(1))

        # print("|  and others")
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
        # print("link to get poster: ")
        # print(result.group(0))
        # just_txt = 'link to get poster'
        return result.group(0)  # just_txt
