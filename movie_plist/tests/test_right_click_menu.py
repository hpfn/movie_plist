import pytest

from movie_plist.pyqt_gui.right_click_menu import RightClickMenu
from unittest.mock import Mock

# one test missing


@pytest.fixture
def create_obj(mocker):
    mocker.patch('movie_plist.pyqt_gui.right_click_menu.QCursor')
    mocker.patch('movie_plist.pyqt_gui.right_click_menu.QMenu')
    mocker.patch('movie_plist.pyqt_gui.right_click_menu.QAction')
    mocker.patch('movie_plist.pyqt_gui.right_click_menu.QMessageBox')
    current_dict = {'Fake': ['http://fake', '/root']}
    m_seen = {}
    m_unseen = {'Whatever': ['http://whatever', '/dir']}

    return RightClickMenu(current_dict, Mock(), m_seen, m_unseen)
    # obj.current_item = 'Whatever'

    # return obj


def test_mark_as_seen(create_obj):
    create_obj.current_item = 'Whatever'
    create_obj.m_seen_movies()
    assert 'Whatever' not in create_obj.us_list.keys()
    assert 'Whatever' in create_obj.s_list.keys()


def test_rm_from_db(create_obj):
    create_obj.current_item = 'Fake'
    create_obj.m_rm_from_db()
    assert 'Whatever' not in create_obj.current_dict.keys()


# def test_mark_as_seen(mocker):
#     mocker.patch.object(RightClickMenu, '__init__', return_value=None)
#     m_seen = RightClickMenu()
#     # m_seen = Mock()
#     m_seen.current_item = 'Whatever'
#     m_seen.us_list = {'Whatever': ['http://fake', '/root']}
#     m_seen.s_list = {}
#     m_seen.qt_list = Mock()
#     m_seen.m_seen_movies()
#     assert 'Whatever' not in m_seen.us_list.keys()
#     assert 'Whatever' in m_seen.s_list.keys()
#
#
# def test_remove_from_db(mocker):
#     mocker.patch('movie_plist.pyqt_gui.right_click_menu.QMessageBox')
#     # mocker.patch('movie_plist.pyqt_gui.right_click_menu.RightClickMenu.qt_list')
#
#     mocker.patch.object(RightClickMenu, '__init__', return_value=None)
#     m_seen = RightClickMenu()
#     m_seen.current_item = 'Whatever'
#     m_seen.current_dict = {'Whatever': ['http://fake', '/root']}
#     m_seen.qt_list = Mock()
#     m_seen.m_rm_from_db()
#     assert 'Whatever' not in m_seen.current_dict.keys()
