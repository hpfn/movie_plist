import pytest

from movie_plist.pyqt_gui.right_click_menu import RightClickMenu
from unittest.mock import Mock


# one test missing


@pytest.fixture
def create_obj(mocker):
    mocker.patch('movie_plist.pyqt_gui.right_click_menu.QMessageBox')
    mocker.patch.object(RightClickMenu, '__init__', return_value=None)
    right_click_menu = RightClickMenu()
    right_click_menu.current_item = 'Brave Heart - 1995'
    right_click_menu.us_dict = {right_click_menu.current_item: 'blabla'}
    right_click_menu.s_dict = {}
    right_click_menu.qt_list = Mock()
    right_click_menu.qt_list.currentRow.return_value = right_click_menu.current_item
    return right_click_menu


def test_mark_as_seen(create_obj):
    obj = create_obj
    obj.m_seen_movies()
    obj.qt_list.takeItem.assert_called_once_with(obj.current_item)
    assert obj.us_dict == {}
    assert obj.s_dict == {obj.current_item: 'blabla'}


def test_rm_from_dict(create_obj):
    obj = create_obj
    obj.current_dict = obj.us_dict
    obj.m_rm_from_dict()
    obj.qt_list.takeItem.assert_called_once_with(obj.current_item)
    assert obj.current_item not in obj.current_dict.keys()
    assert obj.current_dict == {}
