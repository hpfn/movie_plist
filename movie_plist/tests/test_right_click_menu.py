import pytest

from movie_plist.pyqt_gui.right_click_menu import RightClickMenu
from unittest.mock import Mock, patch


# one test missing


@pytest.fixture
def create_obj(mocker):
    mocker.patch('movie_plist.pyqt_gui.right_click_menu.QMessageBox')
    # silence the method that lunch the menu only
    mocker.patch.object(RightClickMenu, 'right_click', return_value=None)
    current_item = 'Brave Heart - 1995'
    un_seen = {current_item: 'blabla'}
    right_click_menu = RightClickMenu({}, Mock(), {}, un_seen)
    right_click_menu.current_item = current_item
    right_click_menu.qt_list.currentRow.return_value = 0
    return right_click_menu


def test_mark_as_seen(create_obj):
    obj = create_obj
    obj.m_seen_movies()
    obj.qt_list.takeItem.assert_called_once_with(0)
    assert obj.us_dict == {}
    assert obj.current_item in obj.s_dict.keys()


def test_rm_from_dict(create_obj):
    obj = create_obj
    obj.current_dict = obj.us_dict
    obj.m_rm_from_dict()
    obj.qt_list.takeItem.assert_called_once_with(0)
    assert obj.current_item not in obj.current_dict.keys()
    assert obj.current_dict == {}


@patch('movie_plist.pyqt_gui.right_click_menu.QMenu')
@patch('movie_plist.pyqt_gui.right_click_menu.QAction')
def test_menu(qaction, qmenu):
    current_item = 'Brave Heart - 1995'
    un_seen = {current_item: 'blabla'}
    RightClickMenu({}, Mock(), {}, un_seen)
    assert qmenu.call_count == 1
    qaction.assert_has_calls(qmenu)
    assert qaction.call_count == 2
