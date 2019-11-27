import platform
from base64 import b64encode
from datetime import timedelta, datetime
from timeit import default_timer as timer
import logging
import cv2
from threading import Thread
import face_recognition
import numpy as np

from db import faces, insert

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

face_locations = []
face_encodings = []
buffer = 4
buffer_time = datetime.now()


def detect(frame):
    global face_locations, face_encodings, \
        buffer, buffer_time

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
            if len(face_encodings) == 0:
                buffer_time = datetime.now()
                face_encodings.append(fe)
                face_locations.append(fl[0])
                logger.debug('Start collection')
            else:
                match = face_recognition.compare_faces(face_encodings, fe,
                                                       tolerance=0.55)

                if ((datetime.now() - buffer_time).seconds > 0.8) or (
                        len(face_encodings) > buffer):
                    face_encodings = []
                    face_locations = []
                    logger.debug('Clear encoding array due timeout')
                elif all(match):
                    face_encodings.append(fe)
                    face_locations.append(fl[0])
                    logger.debug('Collect encoding №: %s', len(face_encodings))
                else:
                    logger.debug('Skip encoding')
                    pass

    if len(face_encodings) >= buffer:
        logger.debug('Running DB Search')
        if len(faces()) > 0:
            for face in faces():
                match = face_recognition.compare_faces(face_encodings,
                                                       face['encoding'],
                                                       tolerance=0.6)
                if sum(match) > buffer / 2:
                    current_face = face
                    logger.debug('Match with: %s, %s', face['name'], face['id'])
                    matched = True
                    break

            if not matched:
                insert('', face_encodings[3])
        else:
            insert('', face_encodings[3])

        top, right, bottom, left = face_locations[3]
        top = top * 4 - 100
        right = right * 4 + 100
        bottom = bottom * 4 + 100
        left = left * 4 - 50

        frame_face = frame[top:bottom, left:right]

        ok, encoded = cv2.imencode(".jpg", frame_face)
        fbytes = b64encode(encoded)
        fstring = fbytes.decode('utf-8')
        current_face['image'] = fstring

        logging.debug('Return current face and clear buffer')
        face_encodings = []
        face_locations = []
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
        self.stream = open_stream(url, lat, width, height)
        self.frame = None
        self.frame_face = None
        self.current_face = {}
        self.current_face_time = datetime.now()

        self.stopped = False

        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True

        if not self.stream.isOpened():
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

            # if g:
            #     assert not isinstance(f, type(None)), 'frame not found'
            # else:
            #     continue

            if np.shape(f) == () or np.sum(f) == 0:
                continue

            count += 1
            if count < 4:
                continue
            count = 0

            self.frame = f.copy()

            try:
                ok, ff, cf = detect(f)
                if ok:
                    self.frame_face = ff
                    self.current_face = cf
                    self.current_face_time = datetime.now()
                elif (datetime.now() - self.current_face_time).seconds > 5:
                    self.current_face = {}
            except Exception as e:
                print(e)
                continue

    async def frames(self, only_faces: bool = False):
        while not self.stopped:
            if only_faces:
                ok, encoded = cv2.imencode(".jpg", self.frame_face.copy())
                if not ok:
                    continue
                yield encoded.tobytes()
            else:
                f = cv2.resize(self.frame.copy(), (0, 0), fx=0.5, fy=0.5)
                ok, encoded = cv2.imencode(".jpg", f)
                if not ok:
                    continue
                yield encoded.tobytes()
            # await asyncio.sleep(0.01)

    def stop(self):
        self.stopped = True

    def release(self):
        self.stopped = True
        self.stream.release()
        self.thread.join()
        print('Stream', self.cid, 'stopped:', not self.stream.isOpened())
