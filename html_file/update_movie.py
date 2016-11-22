import re
import getpass

def EditHtmlUpdate(file_name, movie_title):
    """
       :param file_name: name of the movie file
       :return: nothing
    """
    path_html_file = '/home/' + getpass.getuser() + 'Vídeos/index.html'
    with open(path_html_file, 'r') as html_file:
        html_file_lines = html_file.readlines()

    mark_start = '<!-- start ' + movie_title + ' -->\n'
    count_l = html_file_lines.index(mark_start)
    sub_count = count_l
    for sub_line in html_file_lines[count_l:]:
        if sub_line.startswith('<a href'):
            get_string = re.compile('No_movie_file_yet')
            html_file_lines[sub_count] = get_string.sub(file_name, sub_line, count=2)
            break
        sub_count += 1

    f = open(path_html_file, 'w')
    f.writelines(html_file_lines)
    f.close()

