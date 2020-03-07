# One Man Rock Paper Scissors

#### Unsere Diplomarbeit
Mittels eines Raspberry Pi's und einer Pi Camera soll man gegen einen Computer Schere Stein Papier
spielen können.

#### Prescientific Academic Work
Using a Raspberry Pi and a Pi Camera you can play rock paper scissors againt a computer

## How to setup Raspberry Pi

#### 1. Update and upgrade

1. `$ sudo apt update`
2. `$ sudo apt upgrade`

#### 2. Install dependencies

First install apt packages:

* libqtgui4
* libqt4-test
* libhdf5-dev
* libjasper-dev
* libatlas-base-dev

`$ sudo apt install libqtgui4 libqt4-test libhdf5-dev libjasper-dev libatlas-base-dev`

Then install Python 3 packages:

* opencv-contrib-python (4.0.1.24)
* numpy
* matplotlib
* picamera
* tensorflow

`$ pip3 install numpy matplotlib opencv-contrib-python==4.0.1.24 "picamera[array]" tensorflow `

#### 3. Enable Camera

1. `$ sudo raspi-config`
2. Interfacing options
3. Camera
4. Enable

#### 4. Clone this repository

It's best to clone into the home directory (`/home/pi`).

`$ git clone git@github.com:thomaslienbacher/one-man-rps.git`

or

`$ git clone https://github.com/thomaslienbacher/one-man-rps.git`

#### 5. Basic test

Run a Python file to test if the main dependecies can be imported.

`$ python3 one-man-rps/prototype-scripts/src/check_dependencies.py`

#### 6. Install JetBrains Mono font

1. Download [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
2. Put the `JetBrainsMono-Regular.ttf` into `/usr/share/fonts/`
3. `$ sudo fc-cache -v -f`

#### 7. Add to auto start
Edit `/etc/xdg/lxsession/LXDE-pi/autostart` and add this line at the end `@/usr/bin/python3 /home/pi/one-man-rps/prototype-scripts/src/rps_robot.py`.
