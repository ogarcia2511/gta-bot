import win32gui
import win32ui 
import win32con
import win32api
import cv2
import numpy as np


def capture(area=None):
    # get a handle to main desktop window
    dt_handle = win32gui.GetDesktopWindow()

    # area is (left, top, right, bottom)
    if area is not None:
        left, top, right, bottom = area
        width = right - left
        height = bottom - top
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    dt_dc = win32gui.GetWindowDC(dt_handle)
    img_dc = win32ui.CreateDCFromHandle(dt_dc)

    mem_dc = img_dc.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(bitmap)
    
    # copy screen's bits into memory device context
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    # create image from bitmap
    arr = bitmap.GetBitmapBits(True)
    screenshot = np.fromstring(arr, dtype='uint8')

    # from 1D to 3D (2D + color)
    screenshot.shape = (height, width, 4)

    # print(screenshot.shape)

    img_dc.DeleteDC()

    mem_dc.DeleteDC()
    win32gui.ReleaseDC(dt_handle, dt_dc)
    win32gui.DeleteObject(bitmap.GetHandle())
    
    return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2RGB)