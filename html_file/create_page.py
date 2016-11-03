from html_file.htmltags import HtmlTags


def generate_html(d_scan, stored_d):
    """ create the html file:
          - put the first tags
          - get the info from the db
          - put final tags
    """
    html_page = HtmlTags(d_scan, 'w')
    html_page.top_header()
    # m_data = stored_d.show_data()
    html_page.parse_data_to_inside_table(stored_d.show_data())
    html_page.bottom_tags()
