"""
   edit the .html file to remove a movie entry
"""

def EditHtml(movie_title):
    start_line = ''
    end_line = ''
    count = 0
    with open('/home/zaza/Vídeos/index.html', 'r') as html_file:
        html_file_lines = html_file.readlines()

    mark_start = 'start ' + movie_title
    mark_end = 'end ' + movie_title
    for unwanted in html_file_lines:
        if mark_start in unwanted:
            start_line = count
        if mark_end in unwanted:
            end_line = count
        count += 1

    print("remove from {} to {}" .format(start_line, end_line))
    del html_file_lines[start_line:end_line+1]

    f = open('/home/zaza/Vídeos/index.html', 'w')
    f.writelines(html_file_lines)
    f.close()