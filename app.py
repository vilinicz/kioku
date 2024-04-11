import time

import uvicorn
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from camera import Camera
from config import cameras as camera_configs
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
    room = payload['room']
    note = payload['note']

    res = Face.update(fid, name, room, note)
    return JSONResponse(res)


# Renders current faces for a given camera
async def get_current_faces(request):
    cid = request.path_params['cid']
    camera = next(filter(lambda c: c.cid == cid, cameras), None)
    current_faces = camera.current_faces
    for current_face in current_faces:
        if 'encoding' in current_face:
            del current_face['encoding']
    res = current_faces

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
    Face.create_table()
    for config in camera_configs:
        camera = Camera(config['id'], config['type'], config['url'], config['lat'],
                        config['width'], config['height'], config['resize'])
        cameras.append(camera.start())
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
    Route("/faces", endpoint=get_faces, methods=["GET"]),
    Route("/current_faces/{cid:int}", endpoint=get_current_faces,
          methods=["GET"]),
    Route("/stream/{cid:int}", endpoint=stream, methods=["GET"]),
    Route("/stop", endpoint=stop, methods=["GET"]),
    Mount('/', app=StaticFiles(directory='client/dist', html=True),
          name="client"),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup],
                on_shutdown=[shutdown])

# TODO it's dangerous to allow all origins. Restrict origins for prod.
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
