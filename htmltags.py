# class HtmlParts:
#    def __init__(self):
#        self.name = "py movie info"

def top_header():
    name = "py movie info"
    print("<html>")
    print("<header>")
    print("<meta charset=\"UTF-8\">")
    print("<title>{}</title>" .format(name))
    print("</header>")
    print("<body>")
    print("<table border=\"1\" width=\"100%\" cellpadding=\"4\" cellspacing=\"0\">")

def inside_tabel(poster_jpg, movie_data, link):
    """
       poster_jpg: jpg file
       movie_data: list() with title, titleYear, director, writers, actors, synopsis
       link: link to the directory where the movie is stored
    """
    print("<tr valign=\"top\">")

    print("<td>")
    poster_jpg
    print("</td>")

    print("<td>")
    print("<p>")
    movie.title()
    movie.rate_value_and_votes()
    movie.director()
    movie.creator_writers()
    movie.actors()
    movie.synopsis()
    link
    print("</p>")
    print("</td>")

    print("</tr>")


def bottom_tags():
    print("</table>")
    print("</body>")
    print("</html>")


