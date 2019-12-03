import time
import datetime

import uvicorn
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from camera import Camera
from config import cameras as cc
from db import Face

cameras = []


async def get_faces(request):
    res = Face.all_public()
    return JSONResponse(res)


async def get_face(request):
    fid = request.path_params['fid']
    res = Face.find(fid)
    return JSONResponse(res)


async def update_face(request):
    fid = request.path_params['fid']
    payload = await request.json()
    name = payload['name']

    res = await Face.update(fid, name)
    return JSONResponse(res.json())


async def get_current_face(request):
    cid = request.path_params['cid']
    camera = next(filter(lambda c: c.cid == cid, cameras), None)
    cf = camera.current_face
    if 'encoding' in cf:
        del cf['encoding']
    res = cf

    return JSONResponse(res)


async def stop(request):
    global cameras
    print('Trying to stop all streams')
    for c in cameras:
        c.release()


async def stream(request):
    cid = request.path_params['cid']
    camera = next(filter(lambda c: c.cid == cid, cameras), None)
    if not camera:
        raise HTTPException(404)
    only_faces = request.query_params and request.query_params['of']

    async def generator(c):
        print('Running Generator')
        async for frame in c.frames(only_faces):
            if await request.is_disconnected():
                print('Stop Generator')
                break

            data = b"".join(
                [
                    b"--frame\r\n",
                    b"Content-Type: image/jpeg\r\n\r\n",
                    frame,
                    b"\r\n",
                ]
            )
            yield data

    return StreamingResponse(generator(camera),
                             media_type='multipart/x-mixed-replace; '
                                        'boundary=frame')


def startup():
    global cameras
    for c in cc:
        ccc = Camera(c['id'], c['url'], c['lat'], c['width'], c['height'])
        ccc.start()
        cameras.append(
            ccc
        )
    print('Started Cameras:', list(map(lambda cam: cam.cid, cameras)))


def shutdown():
    global cameras
    print('Trying to stop all streams')
    for c in cameras:
        c.release()
    time.sleep(1.0)


routes = [
    Route("/faces/{fid:int}", endpoint=get_face, methods=["GET"]),
    Route('/faces/{fid:int}', endpoint=update_face, methods=['PATCH']),
    Route("/faces/", endpoint=get_faces, methods=["GET"]),
    Route("/current_face/{cid:int}", endpoint=get_current_face,
          methods=["GET"]),
    Route("/stream/{cid:int}", endpoint=stream, methods=["GET"]),
    Route("/stop", endpoint=stop, methods=["GET"]),
    Mount('/', app=StaticFiles(directory='client/dist', html=True),
          name="client"),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup],
                on_shutdown=[shutdown])

app.add_middleware(CORSMiddleware,
                   allow_origins=['*', 'http://localhost:8080',
                                  'http://192.168.1.254:8080',
                                  '*'
                                  ],
                   )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
