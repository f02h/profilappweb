# aluprofili

pip install bottle
pip3 install bottle
pip3 install bottle-mysql

#run db querys
python3 install.py

#create service
copy service.txt to /lib/systemd/system/aluprofili.service
systemctl enable aluprofili.service

#chromium kiosk
https://wolfgang-ziegler.com/blog/setting-up-a-raspberrypi-in-kiosk-mode-2020
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
/usr/bin/chromium-browser --kiosk  --disable-restore-session-state http://localhost:8080/zaga
