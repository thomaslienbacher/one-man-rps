# One Man Rock Paper Scissors

#### Unsere Diplomarbeit
Mittels eines Raspberry Pi's und einer Pi Camera soll man gegen einen Computer Schere Stein Papier
spielen können.

#### Prescientific Academic Work
Using a Raspberry Pi and a Pi Camera you can play rock paper scissors againt a computer

## How to setup Raspberry Pi

You will need to install various Python 3 packages and compile OpenCV.

#### 1. Compiling and installing OpenCV

Follow this tutorial [Install OpenCV 4 on your Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) **BUT** use OpenCV version **4.0.1**!

##### Remarks:

* Don't use a virtual Python environment, instead install it globaly
* In the later stages of compiling stop the process and restart with only one thread  `-j1`


#### 2. Python 3 packages

* numpy
* matplotlib
* picamera
* tensorflow

`$ pip3 install numpy matplotlib "picamera[array]" tensorflow `

#### 3. Enable Camera
1. `$ sudo raspi-config`
2. Interfacing options
3. Camera
4. Enable

#### 4. Clone this repository
`$ git clone git@github.com:thomaslienbacher/one-man-rps.git`
`$ git clone https://github.com/thomaslienbacher/one-man-rps.git`

