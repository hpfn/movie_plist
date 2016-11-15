from html_file.htmltags import HtmlTags
from pathlib import Path
from info_in_db.movie_plist_sqlite3 import DataStorage


def generate_html(dscan_html, data_from_db):
    """
        if .html file exists and data_from_db has data
           put the new data in .html file

        if .html file does not exist but data_from_db has data
           create the .html file with data_from_db data

        if .html file does not exist and data_from_db is empty
            connect to db, get data and create the .html file

    """
    # movie_file = d_scan + "/pymovieinfo.html"
    movie_file_check = Path(dscan_html)

    if movie_file_check.is_file() and data_from_db:
        HtmlTags(dscan_html, 'inplace', data_from_db)
    elif not movie_file_check.is_file() and data_from_db:
        html_page = HtmlTags(dscan_html, 'w')
        html_page.top_header()
        html_page.parse_data_to_inside_table(data_from_db)
        html_page.bottom_tags()
    elif not movie_file_check.is_file() and not data_from_db:
        stored_data = DataStorage()
        data_from_db = stored_data.movie_unseen()
        html_page = HtmlTags(dscan_html, 'w')
        html_page.top_header()
        html_page.parse_data_to_inside_table(data_from_db)
        html_page.bottom_tags()
        stored_data.exit_from_db()


