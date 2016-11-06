from html_file.htmltags import HtmlTags
from pathlib import Path

def generate_html(d_scan, data_from_db):
    """
        create the html file:
          - put the first tags
          - get the info from the db
          - put final tags

        or

        append to .html file a new movie after
        seek(195) - after the top_header method.
    """
    movie_file_check = d_scan + "/pymovieinfo.html"
    movie_file_check = Path(movie_file_check)
    if not movie_file_check.is_file():
        html_page = HtmlTags(d_scan, 'w')
        html_page.top_header()
        html_page.parse_data_to_inside_table(data_from_db)
        html_page.bottom_tags()
    else:
        HtmlTags(d_scan, 'inplace', data_from_db)

