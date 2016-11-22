import re
import getpass


class EditHtml(object):
    def __init__(self, action):
        # self.movie = movie_name_year
        # self.file = file_name
        self.path_html_file = '/home/' + getpass.getuser() + '/Vídeos/index.html'
        self.to_do = action
        self.html_file_lines = None

        self.to_do_list = {'update': self.update,
                           'remove': self.remove}

    def edithtmlaction(self, movie, file=None):
        """
           :param movie: name and year of the movie
           :param file: name of the movie file. .avi, .mp4, mkv
           :return: nothing
        """
        # path_html_file = '/home/' + getpass.getuser() + 'Vídeos/index.html'
        with open(self.path_html_file, 'r') as html_file:
            self.html_file_lines = html_file.readlines()

        self.to_do_list[self.to_do](movie, file)

        f = open(self.path_html_file, 'w')
        f.writelines(self.html_file_lines)
        f.close()

    def update(self, u_movie, u_file):
        mark_start = '<!-- start ' + u_movie + ' -->\n'
        count_l = self.html_file_lines.index(mark_start)
        sub_count = count_l
        for sub_line in self.html_file_lines[count_l:]:
            if sub_line.startswith('<a href'):
                get_string = re.compile('No_movie_file_yet')
                self.html_file_lines[sub_count] = get_string.sub(u_file, sub_line, count=2)
                break
            sub_count += 1

    def remove(self, r_movie, f=None):
        """
            :param r_movie: movie name and year
            :param f: is not used
            :return: nothing
        """
        mark_start = '<!-- start ' + r_movie + ' -->\n'
        mark_end = '<!-- end ' + r_movie + ' -->\n'
        start_line = self.html_file_lines.index(mark_start)
        end_line = self.html_file_lines.index(mark_end)

        print("remove from {} to {}".format(start_line, end_line))
        del self.html_file_lines[start_line:end_line + 1]
