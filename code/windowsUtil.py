#!/usr/bin/env python3  
# -*- coding: utf-8 -*-
#encoding=utf-8
import os
import logging
import traceback
import win32gui
from win32.lib import win32con
title='照片查看器'
def handle_window(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd):
        if title in win32gui.GetWindowText(hwnd):
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
def closeWin():
    print('开始关闭图片查看器....')
    win32gui.EnumWindows(handle_window, None)
    print('关闭完成！')
if __name__ == '__main__':
    closeWin()