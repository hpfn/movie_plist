import re
import urllib
from bs4 import BeautifulSoup
import pyscan
import pimdbdata
import htmltags

obtain_url = pyscan.dir_to_scan()
m_data = list()
htmltags.top_header()
for url in obtain_url:
    html = urllib.request.urlopen(url).read()
    movie = pimdbdata.ParseImdbData(html)
    # print("<tr valign=\"top\">")

    # print("<td>")
    m_poster = movie.movie_poster()
    # print("</td>")

    # print("<td>")
    # print("<p>")
    title, year = movie.title_year()
    m_data.append(title)
    m_data.append(year)
    # htmltags.inside_table(m_data)
    rate, votes = movie.rate_value_and_votes()
    m_data.append(rate)
    m_data.append(votes)
    director = movie.director()
    m_data.append(director)
    writers_list = movie.creator_writers()
    m_data.append(writers_list)
    actors_list = movie.actors()
    m_data.append(actors_list)
    # htmltags.inside_table(m_data)
    snps_txt =movie.synopsis()
    m_data.append(snps_txt)
    htmltags.inside_table(m_poster, m_data)
    m_data = list()
    # print("</p>")
    # print("</td>")

    # print("</tr>")


htmltags.bottom_tags()
quit(0)
url = 'http://www.imdb.com/title/tt3691740'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "lxml")

# rate value and votes
rate_value = soup.find(itemprop="ratingValue")
print("rate: {}" .format(rate_value.contents[0]))
rate_count = soup.find(itemprop="ratingCount")
print("votes: {}" .format(rate_count.contents[0]))

# people

# director
director = soup.find(itemprop="director")
re_director = re.compile("([A-Z].*[a-z])</span></a>.*")
result = re_director.search(str(director.contents[1]))
print("director: {}" .format(result.group(1)))

# creator "Writers"
writer_cia = soup.find_all(itemprop="creator", itemtype="http://schema.org/Person")
re_writer_cia = re.compile("([A-Z].*[a-z])</span></a>.*")
print("Writers: ", end=' ')
for i in writer_cia:
    result = re_writer_cia.search(str(i))
    print(result.group(1), end="  ")
print()

# actors
actors = soup.find_all(itemprop="actors", itemtype="http://schema.org/Person")
re_actors = re.compile("([A-Z].*[a-z])</span></a>.*")
print("Actors: ", end=' ')
for i in actors:
    result = re_actors.search(str(i))
    print(result.group(1), end="  ")
print("|  and others")
# end people

# movie description
description = soup.find(itemprop="description")
raw_txt = description.contents[0].strip()
# maybe split() is better than this
count = 0
for i in raw_txt:
    if count < 70 or i is not ' ':
        print(i, end='')
    else:
        if i is ' ':
            print()
            count = 0
            continue
    count += 1
print()

# movie poster
poster = soup.find(itemprop="image")
re_poster = re.compile("http.*\.jpg")
result = re_poster.search(str(poster))
print("link to get poster: ")
print(result.group(0))
