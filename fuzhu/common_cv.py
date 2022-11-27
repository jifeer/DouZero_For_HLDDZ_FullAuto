# -*- coding: utf-8 -*-
# Created by: Eric
import logging
import traceback
import ctypes
import os
import win32gui
import pyautogui
import win32ui
from ctypes import windll
from PIL import Image
import cv2
import numpy as np
import os
import sys
import time
import WindHelper
from PyQt5.QtWidgets import QApplication
import kaiduan

runpath = os.path.abspath(".")


class CommonGameHelper:
    def __init__(self):
        self.ScreenZoomRate = 1
        self.Pics = {}
        self.PicsCV = {}
        st = time.time()
        self.Handle = 0
        self.Interrupt = False
        self.RealRate = (600, 338)
        # self.GetZoomRate()

    def Screenshot(self, region=None):  # -> (im, (left, top))
        try_count = 1
        success = False
        app = QApplication(sys.argv)
        while try_count > 0 and not success:
            try:
                try_count -= 1
                parent_handle = win32gui.FindWindow("LDPlayerMainFrame", "雷电模拟器-3")
                child_handle = WindHelper.get_child_windows(parent_handle)
                hwnd = child_handle[0]

                screen = QApplication.primaryScreen()
                img2 = screen.grabWindow(hwnd, 0, 0, 600, 338).toImage()
                img2.save("screenshot2.png")
                time.sleep(0.2)
                img2 = screen.grabWindow(hwnd, 33, 206, 499, 95).toImage()
                img2.save("mycards.png")
                cv2.resize(img2,(img2.shape[0], img2.shape[1], img2.shape[2]), interpolation=cv2.INTER_AREA)
                time.sleep(0.2)
                self.get_cards(img2)
            except Exception as e:
                print("截图时出现错误:", repr(e))

        return None, (0, 0)

    def Screenshot2(self, region=None):  # -> (im, (left, top))
        try_count = 3
        success = False
        while try_count > 0 and not success:
            try:
                try_count -= 1
                # im = Image.open(r"C:\Users\Vincentzyx\Desktop\Snipaste_2021-12-22_22-58-02.png")
                # im = im.resize((1796, 1047))
                # if region is not None:
                #     im = im.crop((region[0], region[1], region[0] + region[2], region[1] + region[3]))
                # ShowImg(im)
                # return im, (0,0)
                # self.GetZoomRate()
                parent_handle = win32gui.FindWindow("LDPlayerMainFrame", "雷电模拟器-3")
                child_handle = WindHelper.get_child_windows(parent_handle)

                self.Handle = parent_handle
                hwnd = self.Handle
                left, top, right, bot = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bot - top
                self.RealRate = (width, height)
                width = int(width / self.ScreenZoomRate)
                height = int(height / self.ScreenZoomRate)
                hwndDC = win32gui.GetWindowDC(hwnd)
                mfcDC = win32ui.CreateDCFromHandle(hwndDC)
                saveDC = mfcDC.CreateCompatibleDC()
                saveBitMap = win32ui.CreateBitmap()
                saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
                saveDC.SelectObject(saveBitMap)
                result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)
                im = Image.frombuffer(
                    "RGB",
                    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                    bmpstr, 'raw', 'BGRX', 0, 1)
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwndDC)
                im.save("mycards1.png")
                if region is not None:
                    im = im.crop((region[0], region[1], region[0] + region[2], region[1] + region[3]))
                    # im = im.resize((600, 338))
                    im.save("afterresize.png")
                if result:
                    success = True
                    return im, (left, top)
            except Exception as e:
                print("截图时出现错误:", repr(e))
                self.sleep(200)
        return None, (0,0)

    def get_cards(self, image):
        st = time.time()
        imgCv = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        tryCount = 10
        cardStartPos = pyautogui.locate(needleImage=self.Pics["card_edge"], haystackImage=image,
                                        region=kaiduan.MyCardsPos, confidence=0.80)
        while cardStartPos is None and tryCount > 0:
            self.LeftClick((900, 550))
            self.sleep(150)
            cardStartPos = pyautogui.locate(needleImage=self.Pics["card_edge"], haystackImage=image,
                                            region=kaiduan.MyCardsPos, confidence=0.80)
            print("找不到手牌起始位置")
            tryCount -= 1
        if cardStartPos is None:
            return [],[]
        sx = cardStartPos[0] + 10
        AllCardsNC = ['rD', 'bX', '2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
        hand_cards = []
        select_map = []
        cardSearchFrom = 0
        sy, sw, sh = 770, 50, 55
        for i in range(0, 20):
            # haveWhite = pyautogui.locate(needleImage=self.Pics["card_white"], haystackImage=image,
            #                              region=(sx + 50 * i, sy, 60, 60), confidence=0.8)
            haveWhite = LocateOnImage(imgCv, self.PicsCV["card_white"], region=(sx + 50 * i, sy, 60, 60), confidence=0.88)
            if haveWhite is not None:
                break
            result = LocateOnImage(imgCv, self.PicsCV["card_upper_edge"], region=(sx + 50 * i, 720, sw, 50), confidence=0.88)
            # result = pyautogui.locate(needleImage=self.Pics["card_upper_edge"], haystackImage=image,
            #                           region=(sx + 50 * i, 720, sw, 50), confidence=0.9)
            checkSelect = 0
            if result is not None:
                # result = pyautogui.locate(needleImage=self.Pics['card_overlap'], haystackImage=image,
                #                           region=(sx + 50 * i, 750, sw, 50), confidence=0.85)
                result = LocateOnImage(imgCv, self.PicsCV["card_overlap"], region=(sx + 50 * i, 750, sw, 50), confidence=0.83)
                if result is None:
                    checkSelect = 1
            select_map.append(checkSelect)
            currCard = ""
            forBreak = False
            ci = cardSearchFrom
            while ci < len(AllCardsNC):
                if "r" in AllCardsNC[ci] or "b" in AllCardsNC[ci]:
                    outerBreak = False
                    result = LocateOnImage(imgCv, self.PicsCV["m" + AllCardsNC[ci]], region=(sx + 50 * i, sy - checkSelect * 25, sw, sh), confidence=0.89)
                    # result = pyautogui.locate(needleImage=self.Pics["m" + AllCardsNC[ci]], haystackImage=image,
                    #                           region=(sx + 50 * i, sy - checkSelect * 25, sw, sh), confidence=0.9)
                    if result is not None:
                        cardPos = (sx + 50 * i + sw // 2, sy - checkSelect * 25 + sh // 2)
                        cardSearchFrom = ci
                        currCard = AllCardsNC[ci][1]
                        cardInfo = (currCard, cardPos)
                        hand_cards.append(cardInfo)
                        outerBreak = True
                        break
                else:
                    outerBreak = False
                    for card_type in ["r", "b"]:
                        result = LocateOnImage(imgCv, self.PicsCV["m" + card_type + AllCardsNC[ci]], region=(sx + 50 * i, sy - checkSelect * 25, sw, sh), confidence=0.91)
                        # result = pyautogui.locate(needleImage=self.Pics["m" + card_type + AllCardsNC[ci]],
                        #                           haystackImage=image,
                        #                           region=(sx + 50 * i, sy - checkSelect * 25, sw, sh), confidence=0.9)
                        if result is not None:
                            cardPos = (sx + 50 * i + sw // 2, sy - checkSelect * 25 + sh // 2)
                            cardSearchFrom = ci
                            currCard = AllCardsNC[ci]
                            cardInfo = (currCard, cardPos)
                            hand_cards.append(cardInfo)
                            outerBreak = True
                            break
                    if outerBreak:
                        break
                    if ci == len(AllCardsNC) - 1 and checkSelect == 0:
                        checkSelect = 1
                        ci = cardSearchFrom - 1
                ci += 1
                if ci == len(AllCardsNC):
                    forBreak = True
            if forBreak:
                break

        return hand_cards, select_map


def LocateOnImage(image, template, region=None, confidence=0.9):
    if region is not None:
        x, y, w, h = region
        imgShape = image.shape
        image = image[y:y+h, x:x+w,:]
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    if (res >= confidence).any():
        return True
    else:
        return None


def LocateAllOnImage(image, template, region=None, confidence=0.9):
    if region is not None:
        x, y, w, h = region
        imgShape = image.shape
        image = image[y:y+h, x:x+w,:]
    w, h = image.shape[1], image.shape[0]
    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= confidence)
    points = []
    for pt in zip(*loc[::-1]):
        points.append((pt[0], pt[1], w, h))
    return points


if __name__ == '__main__':
    cg = CommonGameHelper()
    img, _ = cg.Screenshot2(kaiduan.MyCardsPos)
    cg.get_cards(img)
