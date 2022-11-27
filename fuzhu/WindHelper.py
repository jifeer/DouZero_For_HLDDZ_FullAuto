import win32gui
import win32con


def get_child_windows(parent_hand):
    """获得parent的所有子窗口句柄 返回子窗口句柄列表"""
    if not parent_hand:
        return
    child_list = []
    win32gui.EnumChildWindows(parent_hand, lambda hwnd, param: param.append(hwnd), child_list)
    return child_list


def close_spec_window(class_name, title_name):
    """关闭窗口"""
    win32gui.PostMessage(win32gui.findWindow(class_name, title_name), win32con.WM_CLOSE, 0, 0)
    return True
