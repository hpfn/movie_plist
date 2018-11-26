import os
from unittest.mock import Mock, patch

import pytest

from movie_plist.pyqt_gui.right_click_menu import (
    MOVIE_SEEN, MOVIE_UNSEEN, RightClickMenu
)


@pytest.fixture
def create_obj(mocker):
    mocker.patch('movie_plist.pyqt_gui.right_click_menu.QMessageBox')
    # silence the method that lunch the menu only
    mocker.patch.object(RightClickMenu, 'right_click', return_value=None)
    current_item = 'Brave Heart - 1995'
    # un_seen = {current_item: 'blabla'}
    right_click_menu = RightClickMenu({}, Mock())
    right_click_menu.qt_list.currentItem.return_value.text.return_value = current_item
    right_click_menu.qt_list.currentRow.return_value = 0
    return right_click_menu


def test_mark_as_seen(create_obj):
    MOVIE_UNSEEN['Brave Heart - 1995'] = 'blabla'
    obj = create_obj
    obj.m_seen_movies()

    assert not MOVIE_UNSEEN.get('Brave Heart - 1995', 0)
    obj.qt_list.takeItem.assert_called_once_with(0)
    assert obj.qt_list.currentItem().text() in MOVIE_SEEN.keys()


@patch('subprocess.call')
def test_rm_from_dict(call, create_obj, mocker):
    mocker.patch.object(os.path, 'isfile', return_value=False)
    current_item = 'Brave Heart - 1995'
    current_dict = {current_item: 'blabla'}

    obj = create_obj
    obj.current_dict = current_dict
    obj.m_rm_from_dict()

    obj.qt_list.takeItem.assert_called_once_with(0)
    assert obj.qt_list.currentItem().text() not in obj.current_dict.keys()
    assert obj.current_dict == {}
    assert call.call_count == 0


@patch('os.system')
def test_rm_from_cache(call, create_obj, mocker):
    mocker.patch.object(os.path, 'isfile', return_value=True)
    current_item = 'Brave Heart - 1995'
    current_dict = {current_item: 'blabla'}

    obj = create_obj
    obj.current_dict = current_dict
    obj.m_rm_from_dict()

    obj.qt_list.takeItem.assert_called_once_with(0)
    assert obj.qt_list.currentItem().text() not in obj.current_dict.keys()
    assert obj.current_dict == {}
    assert call.call_count == 1


@patch('movie_plist.pyqt_gui.right_click_menu.QMenu')
@patch('movie_plist.pyqt_gui.right_click_menu.QAction')
def test_menu(qaction, qmenu):
    # current_item = 'Brave Heart - 1995'
    # un_seen = {current_item: 'blabla'}
    RightClickMenu({}, Mock())
    assert qmenu.call_count == 1
    qaction.assert_has_calls(qmenu)
    assert qaction.call_count == 2
