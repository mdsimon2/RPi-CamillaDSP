# RPi-CamillaDSP

## Introduction
Intent of this project is to provide guidance for setting up [CamillaDSP](https://github.com/HEnquist/camilladsp) on a RPi4/5. There is a lot of good information scattered through [ASR](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/), [DIYAudio](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) and the [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp) but there also appears to be a lot of apprehension. My goal is to give concrete examples of how to use CamillaDSP with a variety of hardware to ease some of that apprehension. This tutorial originally lived at ASR, but in May 2024 I decided to migrate it to GitHub to make version management easier and provide a more universal location.

I would like to especially thank @HenrikEnquist for developing CamillaDSP. I’ve long been skeptical of computer-based DSP but CamillaDSP is a game changer. It runs on minimal hardware, is easy to interface with a variety of devices and is exceptionally well designed. I’ve replaced all of my miniDSP systems with RPi4s running CamillaDSP and could not be happier.

I am not a programmer or DSP expert, my primary motivation is finding better ways to implement DIY active speakers. If you see a better way of doing something or want further explanation please speak up! These instructions have been developed as I learned how to implement CamillaDSP and found better ways to set it up but I am always learning.

Prior to GitHub, I archived older versions of the tutorial at the links below.

- [10/20/2022 Archive](https://drive.google.com/file/d/1y-vULEbXNjza7W4X1vQyIIH1r1GOCVpN/view?usp=sharing)
- [12/12/2023 Archive](https://drive.google.com/file/d/1MbB300dAJUEtBld14Qd4loA6hD94v67B/view?usp=share_link)

## Background

### Why would I want to use CamillaDSP on a RPi4?

This tutorial is geared towards 2 channel audio as it is somewhat difficult to get multichannel audio in to a RPi. Typical applications are DIY active speakers / subwoofers such as Directiva R1 (4+ channels), LXmini + sub(s) or LX 521.4 (8+ channels). Another good application is passive stereo speakers with 3+ subwoofers. Although it is possible to use other hardware with CamillaDSP, a RPi4 offers GPIO pins which are useful for integrating a display and has the ability to be used as a USB gadget.

### At a high level how does this work?

Starting point is a RPi4 or RPi5 running either Ubuntu Server 64 bit or Raspberry Pi OS Lite. I recommend a RPi4 due to lower cost and better thermal performance unless you are using the HifiBerry DAC8x which is only supported by the RPi5.

Originally this tutorial used Ubuntu Server as it offered a newer kernel and better compatibility with multichannel DACs (notable the MOTU Ultralite Mk5). However, as of Bookworm Raspberry Pi OS works with all DACs in this tutorial. Currently Ubuntu 24.04 does NOT work with the RPi5 + HifiBerry DAC8x, and Raspberry Pi OS must be used.

We will set up CamillaDSP such that it is always running on the RPi as a service. A web browser based GUI is available to configure CamillaDSP after initial setup. 

CamillaDSP requires a capture device and playback device, the capture device is your input and playback device is your output. 

The capture device can be a variety of things, it can be the RPi itself with software audio players such as squeezelite or shairport-sync playing to an ALSA loopback, it can be the same device as the playback device in the case of an audio interface with analog/digital inputs or it can be a separate device such as a TOSLINK to USB card. The main point here is that CamillaDSP is NOT limited to applications that use a RPi as a source.

The playback device is either a USB DAC/DDC, HDMI output of the RPi or HAT DAC/DDC. This tutorial will focus on USB DACs. Between the capture device and the playback device is where the magic happens, CamillaDSP can implement channel routing, IIR filters, FIR filters, volume control (w/ dynamic loudness), resampling and delay. The RPi is surprising powerful and is able to do much more than any miniDSP product that exists today.

### What DACs are recommended?

1) [Okto dac8 PRO](https://www.oktoresearch.com/dac8pro.htm) - €1289, 8 channel balanced analog output, 8 channel AES digital input, 2 channel AES digital output, 1RU full-rack, volume knob, IR remote control, 5 V trigger, large display, excellent analog performance and overall design. [Okto dac8 PRO ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/review-and-measurements-of-okto-dac8-8ch-dac-amp.7064/).

2) [MOTU Ultralite Mk5](https://motu.com/en-us/products/gen5/ultralite-mk5/) - $650, 10 channel balanced analog output, 8 channel balanced analog input, TOSLINK input / output (also supports ADAT), SPDIF input / output, volume knob capable of controlling all analog outputs, 1RU half-rack, overall good analog performance.  [MOTU Ultralite Mk5 ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/motu-ultralite-mk5-review-audio-interface.24777/).

3) [MOTU M4](https://motu.com/en-us/products/m-series/m4/) - $250, 4 channel unbalanced/balanced analog output, 4 channel balanced analog input, good analog performance, USB powered. Good budget option for 2.1/2.2 or 2 way active systems, I/O functionality is rather limited. [MOTU M4 ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/motu-m4-audio-interface-review.15757/).

5) [HifiBerry DAC8x](https://www.hifiberry.com/shop/boards/hifiberry-dac8x/) - $65, requires a RPi5, 8, HAT, channel unbalanced analog output, good analog noise performance, acceptable distortion performance. Ultimate budget option! [HifiBerry DAC8x Measurements](https://www.audiosciencereview.com/forum/index.php?threads/8ch-hifiberry-hat-dac-for-rpi5.53672/post-1966410).

6) Whatever you have on hand! Part of the beauty of a CamillaDSP / RPi setup is that it is cheap and if you want to try CamillaDSP with another USB DAC it is rather easy to do so. Obviously I will not be able to provide specific configuration files but this tutorial should help you get started.

Although I am not providing configuration files for the following devices, I have used them successfully with CamillaDSP on a RPi4 and can help you with them if needed. In particular the MCHstreamer / USBstreamer are very useful as they allow you to use old pro audio interfaces with ADAT inputs to achieve 8 channels of output at 44.1/48 kHz.

- [miniDSP MCHstreamer](https://www.minidsp.com/products/usb-audio-interface/mchstreamer)
- [miniDSP USBstreamer](https://www.minidsp.com/products/usb-audio-interface/usbstreamer)
- [Focusrite 18i20 2nd gen](https://store.focusrite.com/en-gb/product/scarlett-18i20-2nd-gen/)
- [DIYINHK multichannel XMOS](https://www.diyinhk.com/shop/audio-kits/142-xmos-multichannel-high-quality-usb-tofrom-i2sdsd-spdif-pcb.html)

Below are other good sources of information related to CamillaDSP.

- [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp) - Henrik has done a great job with the GitHub and it is an excellent reference. Almost everything I present here can also be found there.

- [CamillaDSP DIYAudio Thread](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) - If you want to ask a question about CamillaDSP this is where I would ask it. A good thread to search if you have questions on a particular topic.

- [RPi4 + CamillaDSP Tutorial ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/) - This tutorial originally lived in this thread. It is a good place to discuss using CamillaDSP on a RPi as well as display / remote control integrations.

- [Pi4 + CamillaDSP + MOTU M4 ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/pi4-camilladsp-audio-interface-motu-m4-phenomal-dsp-streamer.24493/) - This thread got me started with CamillaDSP.

- [Budget Standalone Toslink > DSP > Toslink with CamillaDSP ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/budget-standalone-toslink-dsp-toslink-with-camilladsp-set-up-instructions-for-newbies.30830/) - Great thread by @MarcosCh showing how to make a low cost (< 50€ !) TOSLINK input / output stereo room correction DSP using CamillaDSP.

- [Using a Raspberry Pi as equaliser in between an USB Source and USB DAC](https://www.audiosciencereview.com/forum/index.php?threads/using-a-raspberry-pi-as-equaliser-in-between-an-usb-source-ipad-and-usb-dac.25414/page-3#post-1180356) - Great thread from @DeLub on how to use a RPi as a USB gadget. Note, if you are using a recent version of Ubuntu or Raspberry Pi OS, steps 1-6 can be skipped (no need to compile kernel).

## CamillaDSP Setup

This part describes how to get a working CamillaDSP setup. Values in bold are user defined such as desired hostname and/or username for your RPi, everything else is universal and can be copy / pasted as-is. Items entered in code snippets are intended to be entered in terminal unless they are in italics in which case they are meant to be copy / pasted in to the file being edited in nano.

For reference, a complete install should take just under 1 hour (including display and FLIRC IR receiver setup), most of that time is waiting for things to download / install.

### 1-4) Write Raspberry Pi OS Lite (recommended) or Ubuntu Server 64 bit to micro SD card using Raspberry Pi Imager and login via SSH

Download and install Raspberry Pi Imager from the links below for your OS.

- [Raspberry Pi Imager for Ubuntu](https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb)
- [Raspberry Pi Imager for Windows](https://downloads.raspberrypi.org/imager/imager_latest.exe)
- [Raspberry Pi Imager for macOS](https://downloads.raspberrypi.org/imager/imager_latest.dmg)

A brief note on micro SD cards, I've been using a 32 GB Sandisk Extreme Pro, others have mentioned they have had good experience with 32 GB Sandisk Ultras. I do not think the specific micro SD card is super important but if things seem slow or you have data corruption issues you might try one of the cards mentioned above. I've also had good luck with USB SSDs but prefer SD cards as they keep everything tidier.

Open Raspberry Pi Imager and select your desired OS and micro SD card. Setup your hostname, username, password, SSH and wifi settings and click the Write button to write OS to micro SD card.

Raspberry Pi Imager Settings.png

This install assumes you are managing the RPi remotely via SSH. If you are running Mac or Linux you will have terminal installed by default and can enter the commands shown in subsequent steps in this tutorial in terminal without issue.

If you are running Windows 10 or 11 I recommend installing Windows Subsystem for Linux (WSL). Instruction below are condensed version of this -> https://docs.microsoft.com/en-us/windows/wsl/install.

Open PowerShell as administrator as shown below.

PowerShell.png

Run wsl --install in PowerShell and restart.

wsl install.png

Once you restart open Ubuntu which will give you a terminal to enter commands.

Ubuntu.png

Before we get started a few notes about using copy / paste in terminal and/or nano. On Mac this is straight forward you can use cmd + v or right click + Paste likely you normally would. On Windows running WSL it is a little weird, I have not found a keyboard shortcut that works but if you right click it will paste what is in your clipboard.

### 5) Update / upgrade RPi

Open terminal and log in to RPi remotely via 
<pre>
ssh <b>username</b>@<b>hostname</b>
</pre>

<pre>
sudo apt update
sudo apt full-upgrade
</pre>

Say yes to any prompts asking if you want to upgrade. You may be prompted about restarting services, if so just hit enter.

### 6) Install CamillaDSP

Make a camilladsp folder as well as folders for CamillaDSP to reference stored coefficients and configurations.

<pre>
mkdir ~/camilladsp ~/camilladsp/coeffs ~/camilladsp/configs
</pre>

Install alsa-utils and git. This will give you access to helpful ALSA tools like aplay and amixer, it will also install libasound2 as a dependency which is required by CamillaDSP.

<pre>
sudo apt install alsa-utils git
</pre>

Download and unpack CamillaDSP. The commands below will install V2.0.3 in /usr/local/bin/.

<pre>
wget https://github.com/HEnquist/camilladsp/releases/download/v2.0.3/camilladsp-linux-aarch64.tar.gz -P ~/camilladsp/
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/
</pre>

### 7-9) Steps removed for simplicity

### 10) Create CamillaDSP service

<pre>
sudo nano /lib/systemd/system/camilladsp.service
</pre>

Paste text below in to nano, modify username to reflect your username. When done, enter 'ctrl + x' to exit nano, enter 'Y' when prompted to Save modified buffer?, hit Enter key when prompted with File Name to Write: /lib/systemd/system/camilladsp.service. You will do the same when editing files in nano elsewhere in this tutorial.

<pre>
[Unit]
After=syslog.target
StartLimitIntervalSec=10
StartLimitBurst=10

[Service]
Type=simple
User=<b>username</b>
WorkingDirectory=~
ExecStart=camilladsp -s camilladsp/statefile.yml -w -g-40 -o camilladsp/camilladsp.log -p 1234
Restart=always
RestartSec=1
StandardOutput=journal
StandardError=journal
SyslogIdentifier=camilladsp
CPUSchedulingPolicy=fifo
CPUSchedulingPriority=10

[Install]
WantedBy=multi-user.target
</pre>

Enable camilladsp service.

<pre>
sudo systemctl enable camilladsp
</pre>

Start camilladsp service.

<pre>
sudo service camilladsp start
</pre>

"-s camilladsp/statefile.yml" tells CamillaDSP you are specifying a configuration via the GUI. You must also add "-w" to tell CamillaDSP to wait for a configuration to be applied via web socket if using the GUI.

“-g-40” sets CamillaDSP volume control to -40 dB every time it starts to avoid accidentally playing something really loud after a system restart. If you are NOT using CamillaDSP volume control please delete “-g-40”.

"-p 1234" is only necessary if you are using the GUI.

"-o camilladsp/camilladsp.log" will create a log file that you can view in the GUI for troubleshooting. You can increase the verbosity of this log by adding "-l debug".

### 11) Install python and dependencies

Rich (BB code):
sudo apt install python3 python3-pip python3-websocket python3-aiohttp python3-jsonschema python3-numpy python3-matplotlib unzip

If you are using Ubuntu Server 22.04 LTS, upgrade pip3. This is not required for Ubuntu Server 23.10.

Rich (BB code):
sudo pip3 install --upgrade pip

### 12) Install pycamilladsp

Download pycamilladsp and install. If you are using Ubuntu 22.04 LTS use the command below.

Rich (BB code):
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp.git

If using Ubuntu 23.10 add "--break-system-packages" to install packages not contained in the system repository. Note, adding "--break-system-packages" will cause the installation to fail if used on Ubuntu 22.04 LTS.

Rich (BB code):
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp.git --break-system-packages

### 13) Install pycamilladsp-plot

Download pyamilladsp-plot and install. If you are using Ubuntu 22.04 LTS use the command below.

Rich (BB code):
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp-plot.git

If using Ubuntu 23.10 add "--break-system-packages" to install packages not contained in the system repository. Note, adding "--break-system-packages" will cause the installation to fail if used on Ubuntu 22.04 LTS.

Rich (BB code):
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp-plot.git --break-system-packages

### 14) Install GUI server

Commands below will install V2.1.0 of the GUI.

Rich (BB code):
wget https://github.com/HEnquist/camillagui-backend/releases/download/v2.1.0/camillagui.zip -P ~/camilladsp/
unzip ~/camilladsp/camillagui.zip -d ~/camilladsp/camillagui

### 15) Try starting GUI

As with CamillaDSP itself it is good practice to start the GUI directly from terminal before proceeding to creating service.

Rich (BB code):
python3 ~/camilladsp/camillagui/main.py

If all goes well you will see the following output. GUI is accessed via http://hostname:5005 from any web browser on your network. Note V1 used port 5000 and v2 now uses port 5005.

Again, use crtl + c to exit.

Rich (BB code):
username@hostname:~$ python3 ~/camilladsp/camillagui/main.py
======== Running on http://0.0.0.0:5005 ========
(Press CTRL+C to quit)

### 16) Create service to start GUI

Rich (BB code):
sudo nano /lib/systemd/system/camillagui.service

Update the User field to reflect your username.

Rich (BB code):
[Unit]
Description=CamillaDSP Backend and GUI
After=multi-user.target

[Service]
Type=idle
User=username
WorkingDirectory=~
ExecStart=python3 camilladsp/camillagui/main.py

[Install]
WantedBy=multi-user.target

Enable camillagui service.

Rich (BB code):
sudo systemctl enable camillagui

Start camillagui service.

Rich (BB code):
sudo service camillagui start

### 17) Assign active configuration in GUI

On a computer that is on the same network as your RPi navigate your browser to http://hostname:5005.

Navigate to Files tab of GUI and set your desired configuration as active by pressing the "star" next to the configuration you want. From now on CamillaDSP and the GUI will start with this configuration loaded. Click the "Apply and Save" button in the lower left to load the configuration to DSP.

Screenshot 2023-12-15 083736.png

Congratulations, you now have CamillaDSP up and running!

If you would like to upgrade to a new version of CamillaDSP simply remove your old CamillaDSP binary and tar and download and extract a new one.

Code:
rm ~/camilladsp/camilladsp ~/camilladsp/camilladsp-linux-aarch64.tar.gz
wget https://github.com/HEnquist/camilladsp/releases/download/v2.0.3/camilladsp-linux-aarch64.tar.gz -P ~/camilladsp/
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/
sudo service camilladsp restart

Upgrading the GUI is a similar process.

Code:
rm -r ~/camilladsp/camillagui ~/camilladsp/camillagui.zip
wget https://github.com/HEnquist/camillagui-backend/releases/download/v2.1.0/camillagui.zip -P ~/camilladsp/
unzip ~/camilladsp/camillagui.zip -d ~/camilladsp/camillagui
sudo service camilladsp restart
sudo service camillagui restart

For upgrades to pycamilladsp and pycamilladsp-plot, re-run the original install commands to get the new versions. For example, running the following will give the most recent versions on Ubuntu 22.04 LTS.

Code:
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp.git
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp-plot.git
sudo service camillagui restart

For upgrades on Ubuntu 23.10 you need to add "--break-system-packages".

Code:
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp.git --break-system-packages
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp-plot.git --break-system-packages
sudo service camillagui restart

