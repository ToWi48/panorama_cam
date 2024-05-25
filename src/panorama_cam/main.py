# -*- coding: utf-8 -*-

# @Time    : 25/05/2024
# @Author  : Tom Wießner
# @Software: Panorama Cam

import cv2
import time
import logging
import ftplib
from datetime import datetime

VIDEO_DURATION = 20  # sec

HOST = "www.black-mountain-bikepark.de"
USER = "f016a074"
PASSWORD = "C4etJ9uHZj2YpS2V9mxt"

UPLOAD_PATH = "webcam/tal/video.mp4"

class Main:
    def init_logger(self, name):
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        logger.addHandler(handler)
        logger.info("logger successfully initialized")

        return logger

    def __init__(self):
        self.logger = self.init_logger('root')

        self.img = cv2.imread('images/logo.png')

        try:
            while True:
                self.logger.info("start recording video ...")
                self.get_video()
                self.logger.info("start uploading video ...")
                self.upload_video()
                self.logger.info("finished! wait 3*60s")
                # wait 3 min
                time.sleep(3*60)
        except Exception as error:
            self.logger.error(error)

    def get_video(self):
        # Get Image dimensions
        img_height, img_width, _ = self.img.shape

        # start cam
        cap = cv2.VideoCapture(2)

        cap.set(3, 3000)
        cap.set(4, 3000)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
        size = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*'h264')
        out = cv2.VideoWriter('output/video_snapshot.mp4', fourcc, 30, size)

        x = width - self.img.shape[1] - 20
        print(width)
        print(self.img.shape)
        print(x)
        y = 20

        start = time.time()

        while((time.time()-start) <= VIDEO_DURATION):
            _, frame = cap.read()

            # add image to frame
            frame[ y:y+img_height , x:x+img_width ] = self.img

            frame = cv2.rectangle(frame, [20, height-20], [400, height-20-80], [255,255,255], -1) 

            # add time
            font                   = cv2.FONT_ITALIC
            bottomLeftCornerOfText = (40,height-50)
            fontScale              = 1
            fontColor              = (0,0,0)
            thickness              = 1
            lineType               = 0

            time_str = datetime.now().strftime("%H:%M:%S")
            cv2.putText(frame, f"LIVE - {time_str} Uhr", 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)

            out.write(frame)

        cap.release()
        out.release()

    def upload_video(self):
        session = ftplib.FTP(HOST, USER, PASSWORD)
        file = open("output/video_snapshot.mp4", "rb")
        session.storbinary("STOR " + UPLOAD_PATH, file)
        file.close()
        session.quit()

def main() -> Main:
    Main()