import time

import cv2
# import imutils # used to resize images in aspect ratio
import numpy as np

import wx
app = wx.App(False)
# width, height =
from pynput.mouse import Button, Controller
from BothHand_PalmLandMarkDetection import HandDetector

wCam, hCam = 640, 480
wScr, hScr = wx.GetDisplaySize()
frameR = 150
smoothing = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# cv2.namedWindow("MouseControl", cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("MouseControl", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

detector = HandDetector(detectionCon=0.8)
mouse = Controller()

while True:
    success, frame = cap.read()

    VideoFrame = cv2.flip(frame, 1)

    hands, Handgesture_Image = detector.findHands(VideoFrame, draw=False, flipType=False)

    if len(hands) == 1:
        cv2.rectangle(Handgesture_Image, (frameR, frameR), (wCam-frameR, hCam-frameR), (255,0, 255), 2)
        lmlist_detected_hand = hands[0]["lmList"]
        # print(lmlist_detected_hand)
        if len(lmlist_detected_hand) != 0:
            Draw_Hands = False
            fingers = detector.fingersUp(hands[0])

            if fingers[1] == 1 and fingers[2] == 0:
                Index_x, Index_y = lmlist_detected_hand[8]
                cv2.circle(Handgesture_Image, (Index_x, Index_y), 5, (0, 0, 255), cv2.FILLED)
                x3 = np.interp(Index_x, (frameR, wCam-frameR), (0, wScr))
                y3 = np.interp(Index_y, (frameR, hCam-frameR), (0, hScr))

                clocX = plocX + (x3 - plocX) / smoothing
                clocY = plocY + (y3 - plocY) / smoothing


                # Mid_x, Mid_y = lmlist_detected_hand[12]
                # cv2.circle(Handgesture_Image, (Mid_x, Mid_y), 5, (0, 0, 255), cv2.FILLED)
                #

                mouse.position = (clocX, clocY)
                plocX,plocY = clocX, clocY
                # mouse.move(50, -10)


            if fingers[1] == 1 and fingers[2] == 1:

                Index_x, Index_y = lmlist_detected_hand[8]

                cv2.circle(Handgesture_Image, (Index_x, Index_y), 5, (0, 0, 255), cv2.FILLED)

                Mid_x, Mid_y = lmlist_detected_hand[12]
                cv2.circle(Handgesture_Image, (Mid_x, Mid_y), 5, (0, 0, 255), cv2.FILLED)
                #
                dist, info, Handgesture_Image = detector.findDistance(lmlist_detected_hand[8], lmlist_detected_hand[12],
                                                                      Handgesture_Image)


                if dist<50:
                    mouse.click(Button.left, 1)
                    time.sleep(1)

    fontscale = 1.0
    # (B, G, R)
    color = (255, 255, 255)
    fontface = cv2.FONT_HERSHEY_COMPLEX_SMALL

    # win_size = cv2.getWindowImageRect("MouseControl")
    # cv2.rectangle(Handgesture_Image, (22, (int(win_size[-1]) - 117)), (22 + 320, (int(win_size[-1]) - 117) + 25),
    #               (0, 0, 0), -1)
    # cv2.putText(Handgesture_Image, "Press 'ESC' key to Exit...", (25, (int(win_size[-1]) - 100)), fontface, fontscale,
    #             color)
    cv2.imshow("MouseControl", Handgesture_Image)
    k = cv2.waitKey(1)
    try:
        if k == 27 or cv2.getWindowProperty('MouseControl', 0) < 0:
            break
    except:
        break


