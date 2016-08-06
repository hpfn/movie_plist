""" only inside_table receive args """

def top_header():
    """ from <html> tag until <table> tag """
    name = "py movie info"
    print("<html>")
    print("<header>")
    print("<meta charset=\"UTF-8\">")
    print("<title>{}</title>" .format(name))
    print("</header>")
    print("<body>")
    print("<table border=\"1\" width=\"100%\" cellpadding=\"4\" cellspacing=\"0\">")

def inside_table(poster_jpg, movie_data):
    """
       poster_jpg: jpg file
       movie_data: list() with title, titleYear, director, writers, actors, synopsis
       link: link to the directory where the movie is stored
    """
    print("<tr valign=\"top\">")

    print("<td>")
    print("{}<br>" .format(poster_jpg))
    print("</td>")

    print("<td>")
    print("<p>")
    #movie.title_year()
    for i in movie_data:
        print("{}<br>" .format(i))
    #movie.rate_value_and_votes()
    #movie.director()
    #movie.creator_writers()
    #movie.actors()
    #movie.synopsis()
    # link # last arg
    print("</p>")
    print("</td>")

    print("</tr>")
    print("<tr valign=\"top\">")
    print("<td>")
    print("----------------<br>")
    print("</td>")
    print("</tr>")


def bottom_tags():
    """ from </table> to </html> """
    print("</table>")
    print("</body>")
    print("</html>")


