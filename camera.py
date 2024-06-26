import asyncio
import logging
import platform
from base64 import b64encode
from datetime import datetime
from threading import Thread

import cv2
import face_recognition
import numpy as np

from db import Face
from buffer import Buffer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

buffer = Buffer(size=5)


def detect(frame, resize):
    global buffer

    current_face = {}
    current_faces = []

    frame_face = None

    matched = False

    process_this_frame = True

    try:
        small_frame = cv2.resize(frame, (0, 0), fx=1 / resize, fy=1 / resize)
        rgb_small_frame = small_frame[:, :, ::-1]
    except Exception as e:
        process_this_frame = False
        print(e)

    if process_this_frame:
        # Add to params model='cnn' to detect on GPU
        face_locs = face_recognition.face_locations(rgb_small_frame)

        if any(face_locs):
            face_encs = face_recognition.face_encodings(rgb_small_frame, face_locs)
            for fe, fl in zip(face_encs, face_locs):
                buffer.add(face=(fe, fl, frame))

            from_buffer = buffer.get_active_groups()

            if len(from_buffer) > 0:
                for group in from_buffer:
                    face_encodings = []
                    face_locations = []
                    face_frames = []
                    for face_data in group:
                        fe, fl, fr = face_data
                        face_encodings.append(fe)
                        face_locations.append(fl)
                        face_frames.append(fr)

                    average = np.mean(np.array(face_encodings), axis=0)

                    match = face_recognition.compare_faces(face_encodings,
                                                           average,
                                                           tolerance=0.29)
                    if sum(match) > len(face_encodings) / 1.5:
                        matched_encodings = []
                        matched_locations = []
                        matched_frames = []
                        for fe, fl, fr, m in zip(face_encodings, face_locations,
                                                 face_frames, match):
                            if m:
                                matched_encodings.append(fe)
                                matched_locations.append(fl)
                                matched_frames.append(fr)

                        matched_average = np.mean(np.array(matched_encodings),
                                                  axis=0)
                        if not Face.all():
                            print('DB is empty. Insert first face')
                            Face.create('', matched_average)
                        else:
                            for face in Face.all():
                                match = face_recognition.compare_faces(
                                    [matched_average],
                                    face['encoding'],
                                    tolerance=0.55)
                                if all(match):
                                    current_face = face.copy()
                                    matched = True
                                    break

                            if not matched:
                                print('No Match. Insert new face')
                                Face.create('', matched_average)

                        top, right, bottom, left = matched_locations[-3]
                        # This is a hack to get the person's face a bit bigger
                        # and better centered in the interface
                        top = int(top * resize * 0.8)
                        right = int(right * resize * 1.08)
                        bottom = int(bottom * resize * 1.05)
                        left = int(left * resize * 0.92)

                        frame_face = matched_frames[-3][top:bottom, left:right]

                        ok, encoded = cv2.imencode(".jpg", frame_face)
                        fbytes = b64encode(encoded)
                        fstring = fbytes.decode('utf-8')
                        current_face['image'] = fstring
                        current_faces.append(current_face)

                return True, frame_face, current_faces

    return False, None, current_faces


def open_stream(ctype, url, lat, width, height):
    g_rtsp = ('rtspsrc location={} latency={} ! queue ! '
              'rtph264depay ! h264parse ! omxh264dec ! '
              'nvvidconv ! '
              'video/x-raw, width=(int){}, height=(int){}, '
              'format=(string)BGRx ! '
              'videoconvert ! appsink drop=true sync=false').format(url, lat,
                                                                    width,
                                                                    height)
    # TODO Gstreamer not working
    g_usb = ('v4l2src device=/dev/video{} ! '
             'image/jpeg, width={}, height={}, framerate={}/1, format=MJPG ! '
             'jpegdec ! xvimagesink ! appsink').format(url,
                                             width,
                                             height, 30)

    def decode_fourcc(v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

    if platform.machine() == "aarch64":
        print("Running on Jetson")
        if ctype == 'rtsp':
            vs = cv2.VideoCapture(g_rtsp, cv2.CAP_GSTREAMER)
            return vs
        else:
            vs = cv2.VideoCapture(url)
            # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            # vs.set(cv2.CAP_PROP_FOURCC, fourcc)
            # vs.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            # vs.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            # vs.set(cv2.CAP_PROP_FPS, 5.0)
            print("Resolution:", vs.get(cv2.CAP_PROP_FRAME_WIDTH), 'x',
                  vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print("FPS", vs.get(cv2.CAP_PROP_FPS))
            c = vs.get(cv2.CAP_PROP_FOURCC)
            print('Fourcc:', decode_fourcc(c))
            print("Format", vs.get(cv2.CAP_PROP_FORMAT))

            return vs
    else:
        print("Running Locally")
        vs = cv2.VideoCapture(url)
        return vs


class Camera:
    def __init__(self, cid, ctype, url, lat, width, height, resize):
        self.resize = resize
        self.ctype = ctype
        self.cid = cid
        self.url = url
        self.lat = lat
        self.width = width
        self.height = height

        self.stream = open_stream(self.ctype, self.url, self.lat, self.width,
                                  self.height)

        self.frame = None
        self.frame_face = None
        self.current_faces = []
        self.current_face_time = datetime.now()

        self.jpeg_quality = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        self.placeholder = []

        self.stopped = False

        # TODO not sure if we need Threads at all
        # For multiple cameras it may be more useful to use multiprocessing
        self.thread = Thread(target=self.run, args=())
        self.thread.daemon = True

        if not self.stream.isOpened():
            # TODO maybe retry instead of raise error
            raise RuntimeError("Could not start video.")
        else:
            print(self.stream.isOpened())

        with open("placeholder.jpg", "rb") as image:
            print("Load placeholder")
            f = image.read()
            self.placeholder = f

    def start(self):
        self.thread.start()
        return self

    def run(self):
        while not self.stopped:
            (g, f) = self.stream.read()

            if not g:
                print(
                    "FAILED TO TAKE FRAME"
                )
                self.stream = open_stream(self.ctype, self.url, self.lat,
                                          self.width, self.height)
                continue

            if np.shape(f) == () or np.sum(f) == 0:
                continue

            self.frame = f.copy()

            try:
                ok, ff, cf = detect(f, self.resize)
                if ok:
                    self.frame_face = ff
                    self.current_faces = cf
                    self.current_face_time = datetime.now()
                elif (datetime.now() - self.current_face_time).seconds > 2:
                    self.current_faces = []
                    self.frame_face = None
            except Exception as e:
                print('Frame detect() error', e)
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
                # f = cv2.resize(self.frame.copy(), (0, 0), fx=0.5, fy=0.5)
                f = self.frame.copy()
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
