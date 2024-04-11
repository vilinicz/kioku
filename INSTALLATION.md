## Kioku app


#### Local

build and push 

---
#### Jetson setup
  
set hostname and install nano:
```
sudo hostnamectl set-hostname kioku
sudo apt-get install nano
```
global deps:
```
sudo apt-get update
sudo apt-get install python3-pip cmake libopenblas-dev liblapack-dev libjpeg-dev
```
Swap file:
```
git clone https://github.com/JetsonHacksNano/installSwapfile
./installSwapfile/installSwapfile.sh
```

#### Reboot now

----
Install Numpy (check for version 17), maybe with sudo:
```
pip3 install numpy
```
Download Dlib, apply fix and compile:
```
wget http://dlib.net/files/dlib-19.19.tar.bz2 
tar jxvf dlib-19.19.tar.bz2
cd dlib-19.19

nano dlib/cuda/cudnn_dlibapi.cpp
// Comment out this line & save! 
// ~#854 forward_algo = forward_best_algo;

sudo python3 setup.py install
```

#### NEXT:
2) mkdir projects/kioku and cd
3) git clone kioku repo
4) create config.json
5) install project deps:
```
pip3 install uvicorn
pip3 install starlette
pip3 install face_recognition
```

---
#### Autostart:
```
cd /etc/systemd/system
sudo nano kioku.service
```
Paste:
```
[Unit]
Description=Kioku app
After=network.target

[Service]
User=developer
WorkingDirectory=/home/developer/projects/kioku
ExecStart=/usr/bin/python3 /home/developer/projects/kioku/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Enable:
```
sudo systemctl daemon-reload
sudo systemctl enable kioku
sudo service kioku start
```
---
#### NGINX:
```
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/kioku.conf
```
Paste:
```
server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```
next:
```
sudo ln -s /etc/nginx/sites-available/kioku.conf /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
```
-----
#### Reboot