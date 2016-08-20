"""
   only inside_table receive args and job is done
"""


class HtmlTags:
    def __init__(self, path):
        self.file_name = path + '/pymovieinfo.html'
        try:
            self.open_file = open(self.file_name, 'w')
        except IOError as ioerr:
            print("Error when trying to open .html file: " + str(ioerr))
            print("Correct path ?")
            return (None)

    def top_header(self):
        """ from <html> tag until <table> tag """
        head = """
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
        movie_data: list() with title titleYear, director, writers, actors, synopsis
        link: link to the directory where the movie is stored
        """
        fields = ['title:', 'rate/votes:', 'director:', 'writer:', 'actors:', 'synopsis:']
        print("<tr valign=\"top\">", file=self.open_file)
        print("<td><img src=\"{}\" width=\"226\" height=\"300\"><br></td><td><p>".format(poster_jpg),
              file=self.open_file)
        for f, m_d in zip(fields, movie_data):
            print("{} {}<br>".format(f, m_d), file=self.open_file)
        print("<a href=\"{}\">{}</a>".format(link + '/' + file, file), file=self.open_file)  # last arg
        # last lines
        last_lines = """
        </p>
        </td>
        </tr>
        <tr>
        <td colspan="2" style="border-top: none; border-bottom: none; border-left: none; border-right: none; padding-top: 0.5cm; padding-bottom: 0.5cm; padding-left: 0.1cm; padding-right: 0.1cm" valign="top" width="100%">
          <center>-------------------------------------------------------</center>
        </td>
        </tr>
        """
        print(last_lines, file=self.open_file)

    def bottom_tags(self):
        """ from </table> to </html> """
        bottom = """
        </table>
        </body>
        </html>
        """
        print(bottom, file=self.open_file)
        self.open_file.close()
