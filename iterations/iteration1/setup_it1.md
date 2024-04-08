# Catberry Pi
## Iteration 1

---

**Hardware**

- Raspberry Pi 3 Model B Rev 1.2
- Raspberry Pi Camera V2
- Raspberry Pi Sense HAT

**Software**
- Debian/GNU Linux 11 (bullseye) aarch64 (Raspberry Pi OS (Legacy, 64-Bit))
- Python 3.9.2
- OpenCV 4.9.0 (Main Modules Package)
- RealVNC Server 7.5.1 (r50075) ARMv8-A (Optional)
- RealVNC Viewer 7.10.0 (r52294) ARMv8-A (Optional)

---

**Setup**

1. Connect [Raspberry Pi Camera](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/2) and [Sense HAT](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat/2) to Raspbery Pi.

2. Using the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) flash your SD Card with Raspberry Pi OS (Legacy, 64-Bit)

3. Once in Raspberry Pi OS open the Terminal and run `sudo apt-get update && sudo apt-get upgrade`

4. Install the Sense HAT Packages by running `sudo apt-get install sense-hat` and reboot Pi `sudo reboot`

5. Several system packages need to be installed:
   `sudo apt install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5 python3-dev`

6. Install Python Package for Raspberry Pi Camera `pip install "picamera[array]"

7. Install OpenCV `pip install opencv-python` (This may take some time)

8. To confirm OpenCV has installed properly:
   `python` , `import cv2` , `cv2.\_\_version\_\_` 
   This should display the version of OpenCV installed.

9. You are now ready to run `iteration1.py`
   ( `python3 iteration1.py` ) 

---

*Optional: Run this Setup Headlessly*

1. On your Raspberry Pi run `sudo raspi-config` use the arrow keys to navigate to `Interface Options`, `VNC` and select `Yes` then exit `raspi-config`

2. On your Desktop/Laptop install [RealVNC Viewer](https://www.realvnc.com/en/connect/download/viewer)

3. Once installed, open RealVNC Viewer on your Desktop/Laptop. (Note: Raspberry Pi and Desktop/Laptop must be connected to the same SSID)

4. In RealVNC Viewer click `File` and `New Connection`

5. Enter your Raspberry Pi's IP Address and click `Ok`

6. You should now see your Raspberry Pi listed.

7. Click on your Raspberry Pi and enter your Raspberry Pi's username and password.

8. You should now see your GUI interface displayed!
