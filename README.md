![Kioku App](./logo.png)  
Kioku is a hotel manager assistance app that helps to know guests at reception faster. 

_Consider it as a proof of concept, first iteration MVP._  

---
![Kioku Demo](./kioku_demo.gif)  
1. recognize guests in a video stream;
2. show guest cards in UI: current photo with editable name, room & note fields;
3. autosave all the data: create new record for new guest or update existing one;

## Key concepts
- **App doesn't store photos.** Nuff said 😄  
  My core idea was to store only encodings, thus it required some additional work to make recognition more accurate: buffering encodings, finding the average, etc..  
  This way, even if the database is stolen, it's impossible to restore the original photos and match the data to real people.
- **Runs completely offline:** on a local network or laptop.  
  Inference is done on a local machine just as is frontend rendering.
  All the data is stored on the device.
- **Runs on any device** that supports Python: Jetson Nano, laptop and others.
- **Consumes streams from multiple sources simultaneously:** webcams, RTSP streams.  
  _However, simultaneous streams feature is less tested, requires some code-related enhancements and better be run on a powerful device (like Jetson)._
- **UI can be opened on tablet/laptop/phone**, any device with browser.

## Tech details 
- **Backend:** Python, Starlette, Uvicorn, face_recognition, OpenCV, Dlib, Numpy, SQLite.
- **Frontend:** Nuxt PWA app, Axios, long-polling.

### To try or develop locally
1. Clone the repo.
2. Install Python dependencies
3. Create `config.json` file (see `config.json.example`)
4. Run `app:app --reload --debug --host=0.0.0.0 --port=8000  --log-level=debug`
5. Open `http://localhost:8000` in browser.
6. Voila!

For frontend development you also need to install frontend dependencies: `cd client & npm i`

To set up more production like installation with Jetson and local network see [INSTALLATION.md](./INSTALLATION.md)  

---
> [!NOTE]  
> 
> All the code is provided as is, without any warranty.   
Both backend and frontend parts are designed and implemented by me.  
`Buffer` part was initially implemented by my friend [megaaction](https://github.com/megaaction), so big thanks to him!  
Kioku logo and related design elements are created and beloved a lot by me as well and I own the rights to them.