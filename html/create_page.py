from html.htmltags import HtmlTags

def generate_html(d_scan, stored_data):
    html_page = HtmlTags(d_scan)
    html_page.top_header()
    # stored_data = DataStorage()
    # get data from db and close the db
    m_data = stored_data.show_data()
    # stored_data.exit_from_db()
    # send data to the table in the .html file
    html_page.parse_data_to_inside_table(m_data)
    # final html tags
    html_page.bottom_tags()