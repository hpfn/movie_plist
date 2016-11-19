import re

def EditHtmlUpdate(file_name, movie_title):
    """
       :param file_name: name of the movie file
       :return: nothing
    """
    with open('/home/zaza/Vídeos/index.html', 'r') as html_file:
        html_file_lines = html_file.readlines()

    mark_start = 'start ' + movie_title
    count_l = 0
    # probably can be better
    for line in html_file_lines:
        if mark_start in line:
            sub_count = count_l
            for sub_line in html_file_lines[count_l:]:
                if sub_line.startswith('<a href'):
                    get_string = re.compile('No_movie_file_yet')
                    html_file_lines[sub_count] = get_string.sub(file_name, sub_line, count=2)
                    break
                sub_count += 1
        count_l += 1

    f = open('/home/zaza/Vídeos/index.html', 'w')
    f.writelines(html_file_lines)
    f.close()

