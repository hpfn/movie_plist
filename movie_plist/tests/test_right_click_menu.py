from movie_plist.pyqt_gui.right_click_menu import RightClickMenu
from unittest.mock import Mock

# one test missing


def test_mark_as_seen(mocker):
    mocker.patch.object(RightClickMenu, '__init__', return_value=None)
    m_seen = RightClickMenu()
    # m_seen = Mock()
    m_seen.current_item = 'Whatever'
    m_seen.us_list = {'Whatever': ['http://fake', '/root']}
    m_seen.s_list = {}
    m_seen.qt_list = Mock()
    m_seen.m_seen_movies()
    assert 'Whatever' not in m_seen.us_list.keys()
    assert 'Whatever' in m_seen.s_list.keys()


# def m_seen_movies(self):
#     """
#     mark a movie as seen.
#     check unseen list and seen list
#     check on db if it is already a seen movie
#     """
#     if self.current_item in self.us_list:
#         title_year = self.current_item
#         self.qt_list.takeItem(self.qt_list.currentRow())
#         self.s_list[title_year] = self.us_list[title_year]
#         del self.us_list[title_year]
#
