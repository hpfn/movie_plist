from unittest.mock import Mock

import pytest

from movie_plist.pyqt_gui.right_click_menu import RightClickMenu


# one test missing


@pytest.fixture
def create_obj(mocker):
    mocker.patch('movie_plist.pyqt_gui.right_click_menu.QMessageBox')
    # the class has three methods, mock the one with more QT stuff only
    mocker.patch.object(RightClickMenu, 'right_click', return_value=None)
    movie = 'Brave Heart - 1995'
    qt_list = Mock()
    qt_list.currentItem.return_value.text.return_value = movie
    qt_list.currentRow.return_value = 0
    right_click_menu = RightClickMenu({}, qt_list, {}, {movie: 'blabla'})
    right_click_menu.item = movie

    return right_click_menu


#     right_click_menu.item = 'Brave Heart - 1995'
#     # right_click_menu.us_dict = {right_click_menu.current_item: 'blabla'}
#     right_click_menu.us_dict = {right_click_menu.item: 'blabla'}
#     right_click_menu.s_dict = {}
#     right_click_menu.qt_list = Mock()
#     right_click_menu.qt_list.currentItem.return_value.text.return_value = right_click_menu.item
#     right_click_menu.qt_list.currentRow.return_value = 0
#     return right_click_menu


def test_mark_as_seen(create_obj):
    obj = create_obj
    obj.m_seen_movies()
    obj.qt_list.currentItem.assert_called_once_with()
    obj.qt_list.currentItem.return_value.text.assert_called_once_with()
    obj.qt_list.takeItem.assert_called_once_with(0)
    assert obj.us_dict == {}
    assert obj.s_dict == {obj.item: 'blabla'}


def test_rm_from_dict(create_obj):
    obj = create_obj
    obj.current_dict = obj.us_dict
    obj.m_rm_from_dict()
    obj.qt_list.currentItem.assert_called_once_with()
    obj.qt_list.currentItem.return_value.text.assert_called_once_with()
    obj.qt_list.takeItem.assert_called_once_with(0)
    assert obj.item not in obj.current_dict.keys()
    assert obj.current_dict == {}
