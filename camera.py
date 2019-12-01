import asyncio
import logging
import platform
from base64 import b64encode
from collections import deque
from datetime import datetime
from threading import Thread

import cv2
import face_recognition
import numpy as np

from db import faces, insert

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# TODO buffer size should be in config.json
buffer_size = 10
buffer_time = datetime.now()
face_locations = deque(maxlen=buffer_size)
face_encodings = deque(maxlen=buffer_size)
average = None


def detect(frame):
    global average, face_locations, face_encodings, \
        buffer_size, buffer_time

    current_face = {}

    matched = False

    process_this_frame = True

    try:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
    except Exception as e:
        process_this_frame = False
        print(str(e))

    if process_this_frame:
        # Add to params model='cnn' to detect on GPU
        fl = face_recognition.face_locations(rgb_small_frame)

        if any(fl):
            fe = face_recognition.face_encodings(rgb_small_frame,
                                                 [fl[0]])[0]

            # Clear buffer if last frame is older then 1 second
            if (datetime.now() - buffer_time).seconds > 1:
                logger.debug('Clearing Buffer due timeout')
                face_encodings.clear()
                face_locations.clear()

            face_encodings.append(fe)
            face_locations.append(fl[0])
            buffer_time = datetime.now()

            if len(face_encodings) == buffer_size:
                average = np.mean(np.array(face_encodings), axis=0)

                match = face_recognition.compare_faces(face_encodings,
                                                       average,
                                                       tolerance=0.3)
                if sum(match) > buffer_size / 1.5:
                    # logger.debug('Running DB Search.')
                    if len(faces()) > 0:
                        for face in faces():
                            match = face_recognition.compare_faces(
                                [average],
                                face['encoding'],
                                tolerance=0.6)
                            if all(match):
                                current_face = face
                                logger.debug('Match with: %s, %s',
                                             face['name'], face['id'])
                                matched = True
                                break

                        if not matched:
                            print('No Match. Insert new face')
                            insert('', average)
                    else:
                        print('DB is empty. Insert first face')
                        insert('', average)

                    top, right, bottom, left = face_locations[buffer_size - 1]
                    top = int(top * 4 * 0.6)
                    right = int(right * 4 * 1.08)
                    bottom = int(bottom * 4 * 1.05)
                    left = int(left * 4 * 0.92)

                    frame_face = frame[top:bottom, left:right]

                    ok, encoded = cv2.imencode(".jpg", frame_face)
                    fbytes = b64encode(encoded)
                    fstring = fbytes.decode('utf-8')
                    current_face['image'] = fstring

                    return True, frame_face, current_face

    return False, None, current_face


def open_stream(url, lat, width, height):
    gst_str = ('rtspsrc location={} latency={} ! queue ! '
               'rtph264depay ! h264parse ! omxh264dec ! '
               'nvvidconv ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink drop=true sync=false').format(url, lat,
                                                                     width,
                                                                     height)
    if platform.machine() == "aarch64":
        print('Running on Jetson')
        return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
    else:
        print('Running locally')
        vs = cv2.VideoCapture(url)
        vs.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        vs.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        return vs


class Camera:
    def __init__(self, cid, url, lat, width, height):
        self.cid = cid
        self.url = url
        self.lat = lat
        self.width = width
        self.height = height

        self.stream = open_stream(url, lat, width, height)
        self.frame = None
        self.frame_face = None
        self.current_face = {}
        self.current_face_time = datetime.now()

        self.jpeg_quality = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        self.placeholder = []

        self.stopped = False

        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True

        with open("placeholder.jpg", "rb") as image:
            print("Load placeholder")
            f = image.read()
            self.placeholder = f

        if not self.stream.isOpened():
            # TODO maybe retry instead of raise error
            raise RuntimeError("Could not start video.")
        else:
            print(self.stream.isOpened())

    def start(self):
        self.thread.start()
        return self

    def run(self):
        count = 0
        while not self.stopped:
            (g, f) = self.stream.read()

            if not g:
                self.stream = open_stream(self.url, self.lat,
                                          self.width, self.height)
                continue

            if np.shape(f) == () or np.sum(f) == 0:
                continue

            count += 1
            if count < 4:
                continue
            count = 0

            self.frame = f

            try:
                ok, ff, cf = detect(f)
                if ok:
                    self.frame_face = ff
                    self.current_face = cf
                    self.current_face_time = datetime.now()
                elif (datetime.now() - self.current_face_time).seconds > 5:
                    self.current_face = {}
                    self.frame_face = None
            except Exception as e:
                print(e)
                continue

    async def frames(self, only_faces: bool = False):
        while not self.stopped:
            if only_faces:
                if self.frame_face is not None:
                    ok, encoded = cv2.imencode(".jpg", self.frame_face,
                                               self.jpeg_quality)
                    if not ok:
                        continue
                    yield encoded.tobytes()
                else:
                    yield self.placeholder
                    await asyncio.sleep(0.5)
            else:
                f = cv2.resize(self.frame.copy(), (0, 0), fx=0.5, fy=0.5)
                ok, encoded = cv2.imencode(".jpg", f, self.jpeg_quality)
                if not ok:
                    continue
                yield encoded.tobytes()

    def stop(self):
        self.stopped = True

    def release(self):
        self.stopped = True
        self.stream.release()
        self.thread.join()
        print('Stream', self.cid, 'stopped:', not self.stream.isOpened())
