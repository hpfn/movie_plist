"""
   only inside_table receive args and job is done
"""

class HtmlTags:
    def __init__(self):
        self.file_name = 'pymovieinfo.html'
        self.open_file = open(self.file_name, 'w+')

    def top_header(self):
        """ from <html> tag until <table> tag """
        head="""
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Py Movie Info</title>
        </head>
        <body>
        <table border="1" width="100%" cellpadding="4" cellspacing="0">
        """
        print(head, file=self.open_file)

    def inside_table(self, poster_jpg, movie_data, link, file=None):
        """
        poster_jpg: jpg file
        movie_data: list() with title, titleYear, director, writers, actors, synopsis
        link: link to the directory where the movie is stored
        """

        print("<tr valign=\"top\">", file=self.open_file)
        print("<td>{}<br></td><td><p>" .format(poster_jpg), file=self.open_file)
        for i in movie_data:
            print("{}<br>" .format(i), file=self.open_file)
        print("<a href=\"{}\">{}</a>" .format(link + '/' + file, link), file=self.open_file) # last arg
        # last lines
        last_lines="""
        </p>
        </td>
        </tr>
        <tr valign="top">
        <td>
        ----------------<br>
        </td>
        </tr>
        """
        print(last_lines, file=self.open_file)

    def bottom_tags(self):
        """ from </table> to </html> """
        bottom="""
        </table>
        </body>
        </html>
        """
        print(bottom, file=self.open_file)
        self.open_file.close()
