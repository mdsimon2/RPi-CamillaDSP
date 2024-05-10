# RPi-CamillaDSP

## Introduction
Intent of this project is to provide guidance for setting up [CamillaDSP](https://github.com/HEnquist/camilladsp) on a RPi4/5. There is a lot of good information scattered through [ASR](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/), [DIYAudio](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) and the [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp) but there also appears to be a lot of apprehension. My goal is to give concrete examples of how to use CamillaDSP with a variety of hardware to ease some of that apprehension. This tutorial originally lived at ASR, but in May 2024 I decided to migrate it to GitHub to make version management easier and provide a more universal location.

I would like to especially thank @HenrikEnquist for developing CamillaDSP. I’ve long been skeptical of computer-based DSP but CamillaDSP is a game changer. It runs on minimal hardware, is easy to interface with a variety of devices and is exceptionally well designed. I’ve replaced all of my miniDSP systems with RPi4s running CamillaDSP and could not be happier.

I am not a programmer or DSP expert, my primary motivation is finding better ways to implement DIY active speakers. If you see a better way of doing something or want further explanation please speak up! These instructions have been developed as I learned how to implement CamillaDSP and found better ways to set it up but I am always learning.

Prior to GitHub, I archived older versions of the tutorial at the links below.

- [10/20/2022 Archive](https://drive.google.com/file/d/1y-vULEbXNjza7W4X1vQyIIH1r1GOCVpN/view?usp=sharing)
- [12/12/2023 Archive](https://drive.google.com/file/d/1MbB300dAJUEtBld14Qd4loA6hD94v67B/view?usp=share_link)

## Background

### Why would I want to use CamillaDSP on a RPi?

This tutorial is geared towards 2 channel audio as it is somewhat difficult to get multichannel audio in to a RPi. Typical applications are DIY active speakers / subwoofers such as Directiva R1 (4+ channels), LXmini + sub(s) or LX 521.4 (8+ channels). Another good application is passive stereo speakers with 3+ subwoofers. Although it is possible to use other hardware with CamillaDSP, a RPi4 offers GPIO pins which are useful for integrating a display and has the ability to be used as a USB gadget.

### At a high level how does this work?

Starting point is a RPi4 or RPi5 running either Raspberry Pi OS Lite or Ubuntu Server 64 bit. I recommend the RPi4 over the RPi5 due to lower cost and better thermal performance. However, a RPi5 is required for multichannel I2S applications such as the HifiBerry DAC8x.

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

This part describes how to get a working CamillaDSP setup. For reference, a complete install should take just under 1 hour (including display and FLIRC IR receiver setup), most of that time is waiting for things to download / install.

### 1) Write Raspberry Pi OS Lite (recommended) or Ubuntu Server 64 bit to micro SD card using Raspberry Pi Imager and login via SSH

Download and install Raspberry Pi Imager from the links below for your OS.

- [Raspberry Pi Imager for Ubuntu](https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb)
- [Raspberry Pi Imager for Windows](https://downloads.raspberrypi.org/imager/imager_latest.exe)
- [Raspberry Pi Imager for macOS](https://downloads.raspberrypi.org/imager/imager_latest.dmg)

A brief note on micro SD cards, I've been using a 32 GB Sandisk Extreme Pro, others have mentioned they have had good experience with 32 GB Sandisk Ultras. I do not think the specific micro SD card is super important but if things seem slow or you have data corruption issues you might try one of the cards mentioned above. I've also had good luck with USB SSDs but prefer SD cards as they keep everything tidier.

Open Raspberry Pi Imager, select your desired RPi, OS and micro SD card. Setup your hostname, username, password, SSH and wifi settings and click the Write button to write OS to micro SD card.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/raspberrypi_imager_settings.png" alt="raspberrypi_imager_settings" width="300"/>

This install assumes you are managing the RPi remotely via SSH. If you are running Mac or Linux you will have terminal installed by default and can enter the commands shown in subsequent steps in this tutorial in terminal without issue.

If you are running Windows 10 or 11 I recommend installing Windows Subsystem for Linux (WSL). Instruction below are condensed version of this -> https://docs.microsoft.com/en-us/windows/wsl/install.

Open PowerShell as administrator as shown below.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/powershell.png" alt="powershell" width="300"/>

Run wsl --install in PowerShell and restart.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/wsl_install.png" alt="wsl_install" width="500"/>

Once you restart open Ubuntu which will give you a terminal to enter commands.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/Ubuntu.png" alt="Ubuntu" width="500"/>

### 2) Update / upgrade RPi

Open terminal and log in to RPi using your username and hostname.

```
ssh username@hostname
```

```
sudo apt update
sudo apt full-upgrade
```

Say yes to any prompts asking if you want to upgrade. You may be prompted about restarting services, if so just hit enter.

### 3) Install CamillaDSP

Make a camilladsp folder as well as folders for CamillaDSP to reference stored coefficients and configurations.

```
mkdir ~/camilladsp ~/camilladsp/coeffs ~/camilladsp/configs
```

Install alsa-utils and git. This will give you access to helpful ALSA tools like aplay and amixer, it will also install libasound2 as a dependency which is required by CamillaDSP. git is useful for downloading files from GitHub.

```
sudo apt install alsa-utils git
```

Download and unpack CamillaDSP. The commands below will install V2.0.3 in /usr/local/bin/.

```
wget https://github.com/HEnquist/camilladsp/releases/download/v2.0.3/camilladsp-linux-aarch64.tar.gz -P ~/camilladsp/
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/
```

### 4) Create CamillaDSP service

```
sudo nano /lib/systemd/system/camilladsp.service
```

Paste text below in to nano, modify username to reflect your username. 

```
[Unit]
After=syslog.target
StartLimitIntervalSec=10
StartLimitBurst=10

[Service]
Type=simple
User=username
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
```

When done, enter 'ctrl + x' to exit nano, when prompted with Save modified buffer? enter 'Y' and when prompted with File Name to Write: /lib/systemd/system/camilladsp.service hit Enter key. You will do the same when editing files in nano elsewhere in this tutorial.

Enable camilladsp service.

```
sudo systemctl enable camilladsp
```

Start camilladsp service.

```
sudo service camilladsp start
```

"-s camilladsp/statefile.yml" tells CamillaDSP you are specifying a configuration via the GUI. You must also add "-w" to tell CamillaDSP to wait for a configuration to be applied via web socket if using the GUI.

“-g-40” sets CamillaDSP volume control to -40 dB every time it starts to avoid accidentally playing something really loud after a system restart. If you are NOT using CamillaDSP volume control please delete “-g-40”.

"-p 1234" is only necessary if you are using the GUI.

"-o camilladsp/camilladsp.log" will create a log file that you can view in the GUI for troubleshooting. You can increase the verbosity of this log by adding "-l debug".

### 5) Install python and dependencies

```
sudo apt install python3 python3-pip python3-websocket python3-aiohttp python3-jsonschema python3-numpy python3-matplotlib unzip
```

### 6) Install pycamilladsp

Download pycamilladsp and install. 

```
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp.git --break-system-packages
```

### 7) Install pycamilladsp-plot

Download pyamilladsp-plot and install. 

```
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp-plot.git --break-system-packages
```

### 8) Install GUI server

Commands below will install V2.1.1 of the GUI.

```
wget https://github.com/HEnquist/camillagui-backend/releases/download/v2.1.1/camillagui.zip -P ~/camilladsp/
unzip ~/camilladsp/camillagui.zip -d ~/camilladsp/camillagui
```

### 9) Create service to start GUI

```
sudo nano /lib/systemd/system/camillagui.service
```

Past text below in to nano, modify username to reflect your username.

```
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
```

Enable camillagui service.

```
sudo systemctl enable camillagui
```

Start camillagui service.

```
sudo service camillagui start
```

### 10) Assign active configuration in GUI

Configurations are explained in more detail in Part 3 of this tutorial. Pre-made configurations for the DACs in this tutorial can be downloaded by navigating to the [configs](https://github.com/mdsimon2/RPi-CamillaDSP/tree/main/configs) folder of this repository. Alternatively you can download the entire repository by clicking [here](https://github.com/mdsimon2/RPi-CamillaDSP/archive/refs/heads/main.zip) or using git clone.

On a computer that is on the same network as your RPi navigate your browser to http://hostname:5005.

Navigate to Files tab of GUI and upload your desired configuration using the up arrow in the Configs section. Set this configuration as active by pressing the "star" next to the configuration. From now on CamillaDSP and the GUI will start with this configuration loaded. Click the "Apply and Save" button in the lower left to load the configuration to DSP.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/configs.png" alt="configs" width="600"/>

Congratulations, you now have CamillaDSP up and running!

### 11) Upgrading to future versions

If you would like to upgrade to a new version of CamillaDSP simply remove your old CamillaDSP binary and tar and download and extract a new one.

```
rm ~/camilladsp/camilladsp-linux-aarch64.tar.gz
wget https://github.com/HEnquist/camilladsp/releases/download/v2.0.3/camilladsp-linux-aarch64.tar.gz -P ~/camilladsp/
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/
sudo service camilladsp restart
```

Upgrading the GUI is a similar process.

```
rm -r ~/camilladsp/camillagui ~/camilladsp/camillagui.zip
wget https://github.com/HEnquist/camillagui-backend/releases/download/v2.1.1/camillagui.zip -P ~/camilladsp/
unzip ~/camilladsp/camillagui.zip -d ~/camilladsp/camillagui
sudo service camilladsp restart
sudo service camillagui restart
```

For upgrades to pycamilladsp and pycamilladsp-plot, re-run the original install commands to get the new versions. 

```
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp.git --break-system-packages
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp-plot.git --break-system-packages
sudo service camillagui restart
```

## Streamer Applications

There are two basic ways to use CamillaDSP, either use RPi as a streamer (AirPlay, squeezelite, spotify, bluetooth, etc) or use an external physical input like TOSLINK, SPDIF, AES or analog. I will document configuration files for both streamer and external inputs for each of the recommended DACs in this tutorial. The configurations are simple and route 2 channel input to all available outputs.

For streamer applications I am assuming your player is outputting 44.1 kHz and resampling everything that is not 44.1 kHz to accomplish this. Before we get started I will show you how to install shairport-sync (Airplay) and squeezelite as these are the players that I use in my streamer setup and how to best configure them.

### shairport-sync


```
sudo apt install shairport-sync libsoxr-dev
```

After you install there are some configuration items we will need to change.

```
sudo nano /etc/shairport-sync.conf
```

Uncomment the following lines (delete // from start of line) and make changes shown below.

```
interpolation = "soxr";
output_device = "hw:Loopback,1";
```

Using SOX for interpolation should avoid audible artifacts from clock syncing. The last line sets the output device to your ALSA loopback device 1. Airplay will automatically resample to 44.1 kHz sample rate by default.

Restart shairport-sync service to reflect changes in shairport-sync.conf

```
sudo service shairport-sync restart
```

### squeezelite

```
sudo apt install squeezelite
```

Like shairport-sync we need to make a few changes to the squeezelite configuration. Copy and paste the lines shown below to the end of the file using nano.

```
sudo nano /etc/default/squeezelite
```

```
SL_SOUNDCARD="hw:Loopback,1"
SB_EXTRA_ARGS="-W -C 5 -r 44100-44100 -R hLE:::28"
```

Restart squeezelite service to reflect changes.

```
sudo service squeezelite restart
```

These changes set your ALSA loopback device 1 as squeezelite playback device, resample all files to 44.1 kHz using a high quality resampling algorithm and stop squeezelite after 5 seconds of inactivity.

## CamillaDSP Configurations

All configurations use maximum amount of output channels for a given device. If you do not need an output channel remove it from the mixer as each extra channel requires additional processing resource. Configuration files can be found in the [configs](https://github.com/mdsimon2/RPi-CamillaDSP/tree/main/configs) folder of this repository.

The naming convention for my configuration files is dac_input_capturerate_playbackrate. For example, a configuration for a MOTU Ultralite Mk5, TOSLINK input with 96 kHz capture and 96 kHz playback rates is ultralitemk5_toslink_96c_96p.

### ASRC Options
CamillaDSP expects a constant capture sample rate and cannot accommodate rate changes without a restart. If you have a variable sample rate physical digital source like TOSLINK, AES or SPDIF or have multiple physical digital sources with different rates, a good option is to add a device that has an ASRC to convert to a consistent rate. miniDSP offer many devices with this capability which are summarized summarized below.

- [nanoDIGI](https://www.minidsp.com/images/documents/nanoDIGI%202x8%20User%20Manual.pdf) - $170, discontinued in 2021 but possible to find used, SPDIF / TOSLINK input, SPDIF output, 96 kHz
- [2x4HD](https://www.minidsp.com/products/minidsp-in-a-box/minidsp-2x4-hd) - $225, TOSLINK / analog input, USB output, 96 kHz
- [miniDSP OpenDRC-DI](https://www.minidsp.com/products/opendrc-series/opendrc-di) - $325, AES / SPDIF / TOSLINK input and output, 48 or 96 kHz
- [Flex Digital](https://www.minidsp.com/products/minidsp-in-a-box/flex) - $495, SPDIF / TOSLINK / USB / analog / bluetooth input, SPDIF / TOSLINK / USB output, 96 kHz
- [Flex Analog](https://www.minidsp.com/products/minidsp-in-a-box/flex) $495-470, SPDIF / TOSLINK / analog / bluetooth input, USB Output, 96 kHz
- [SHD Studio](https://www.minidsp.com/products/streaming-hd-series/shd-studio) - $900, AES / SPDIF / TOSLINK / USB / streamer input, SPDIF / AES / USB output, 96 kHz
- [SHD](https://www.minidsp.com/products/streaming-hd-series/shd) - $1250, AES / SPDIF / TOSLINK / USB / streamer / analog input, SPDIF / AES / USB output, 96 kHz

All of these devices can do IR volume control, although not all have displays for volume / input identification.

2x4HD and Flex can be upgraded with Dirac but sample rate will change from 96 kHz to 48 kHz.

In order to use USB output of devices like 2x4HD, Flex and SHD you need to set them as the CamillaDSP capture device. Unfortunately this ties up the USB input and makes it unusable. Still, this is a good approach to add extra input functionality to basic USB DACs like the MOTU M4 or Topping DM7 which only have USB input.

If you have a constant sample rate digital source the following devices work well. Compared to other solutions like the HiFiBerry Digi+ I/O they handle signal interruptions gracefully. These devices are used in a similar way to the miniDSPs with USB outputs, the device is set as the CamillaDSP capture device. Note, that although the S2 digi also has a TOSLINK output, I don't recommend using I've experienced audible dropouts when using it as an output.

- [hifime S2 digi (SA9227)](https://hifimediy.com/product/s2-digi/) - $40, TOSLINK input, USB output, sample rates up to 192 kHz
- [hifime UR23](https://hifimediy.com/product/hifime-ur23-spdif-optical-to-usb-converter/) - $25, TOSLINK input, USB output, does NOT work with RPi5, sample rates up to 96 kHz

### Okto dac8 PRO

These configurations assume you are NOT using CamillaDSP volume control as the Okto has a nice volume display with knob and IR control. As volume control is downstream of CamillaDSP, digital clipping in CamillaDSP is more of an issue. As a result, I have added 1 dB attenuation on all output channels of configurations that implement resampling to help avoid clipping. In general, if you add boost in your configuration you will want to offset that boost by attenuating the output further. Use the CamillaDSP clipping indicator to gauge if you have enough attenuation to avoid digital clipping.

#### okto_streamer.yml

Set Okto to “Pure USB” mode. As mentioned previously all streamer configurations expect 44.1 kHz input. As the ALSA loopback has a different clock from the Okto, these configurations have rate adjust enabled to allow CamillaDSP to adjust the ALSA loopback to match the Okto clock and avoid buffer under/over runs, you will see this approach in all further streamer configurations. I have also included configurations that upsample to 96 kHz and 192 kHz.

#### okto_aes.yml

Set Okto to “USB / AES” mode. This configuration assumes you are using 2 channel input with 8 channel output. If you would like to use more input channels you can modify the mixer to do so. No rate adjust is enabled as the Okto is clocked by AES input in this mode. All configurations use the same input and output sample rate as it is not possible to use different sample rates. Configurations are provided for 48, 96 and 192 kHz sample rates.

### MOTU Ultralite Mk5

This DAC requires a small amount of setup, either while connected to a Mac or Windows computer. Install Cuemix 5 and set up channel routing such that USB 1-2 are routed to analog output 1-2, USB 3-4 to analog output 3-4, etc. Make sure no other channel routing is in place as we will do all channel routing in CamillaDSP. Check your levels in the Output tab as my Ultralite Mk5 came with all channels set to -20 dB by default. If you want to use the Mk5 volume knob then select which analog channels (knob will only work on analog channels) you want controlled by the knob in the Output tab. See screenshots below for what this should look like.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/cuemix_main_1-2.png" alt="cuemix_main_1-2" width="500"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/cuemix_main_3-4.png" alt="cuemix_main_3-4" width="500"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/cuemix_output.png" alt="cuemix_output" width="500"/>


It is a good idea to update the firmware at this time. After you do this initial setup in Cuemix you will not need to use it again in the future unless you want to upgrade the firmware.

Input / output channels are described below, however not all channels are present at all sample rates. At 44.1/48 kHz all channels are available, at 88.2/96 kHz only inputs 0-15 and outputs 0-17 are available and at 176.4/192 kHz only inputs 0-9 and outputs 0-9 are available.

Inputs:
- 0-7: analog 1-8
- 8-9: loopback 1-2
- 10-11: SPDIF 1-2
- 12-13: TOSLINK/ADAT 1-2
- 14-15: ADAT 3-4
- 16-17: ADAT 5-6
- 18-19: ADAT 7-8

Outputs:
- 0-9: analog 1-10
- 10-11: headphone 1-2
- 12-13: SPDIF 1-2
- 14-15: TOSLINK/ADAT 1-2
- 16-17: ADAT 3-4
- 18-19: ADAT 5-6
- 20-21: ADAT 7-8

Once you have channel routing setup in Cuemix this DAC is very similar to the Okto in terms of setup just with more inputs / output options. Although it has a volume knob, I like to use CamillaDSP for volume control with the Mk5 as it does not have an IR receiver. I use a FLIRC USB IR receiver and separate display for volume indication as described in Part 4.

#### ultralitemk5_streamer.yml

- Set clock source to internal via Ultralite Mk5 front panel. 
- All streamer configurations expect 44.1 kHz input. 
- Due to clock difference between loopback and Ultralite Mk5, rate adjust is enabled.
- Configurations provided for 44.1, 96 and 192 kHz output sample rates.

#### ultralitemk5_toslink.yml

- Set clock source to optical and optical input setting to TOSLINK via Ultralite Mk5 front panel. 
- No rate adjust is enabled as Ultralite Mk5 is clocked by TOSLINK input in this mode.
- It is not possible to use different input and output sample rates when using Ultralite Mk5 as capture device.
- Configurations provided for 48 and 96 kHz sample rates.
#### ultralitemk5_spdif.yml

- Set clock source to SPDIF via Ultralite Mk5 front panel. 
- No rate adjust is enabled as Ultralite Mk5 is clocked by SPDIF input in this mode. 
- It is not possible to use different input and output sample rates when using Ultralite Mk5 as capture device.
- Configurations provided for 48 and 96 kHz sample rates.

#### ultralitemk5_analog.yml

- Set clock source to internal via Ultralite Mk5 front panel.
- This configuration uses analog 3 and 4 as inputs but you can add/change to other inputs as needed.
- It is not possible to use different input and output sample rates when using Ultralite Mk5 as capture device.
- Configurations provided for 48, 96 and 192 kHz sample rates.

### MOTU M4

This is the easiest of the bunch to setup as it has limited I/O functionality. Like the Ultralite Mk5 I use CamillaDSP volume control with this DAC. Due limited input functionality I show how to use a variety of external devices with this DAC, similar configurations can be used with any DAC in this tutorial.

#### m4_streamer.yml

- All streamer configurations expect 44.1 kHz input. 
- Due to clock difference between loopback and M4, rate adjust is enabled. 
- Configurations provided for 44.1, 96 and 192 kHz sample rates.

#### m4_analog.yml

- This configuration uses analog inputs 3 and 4 but you can use others if needed. 
- It is not possible to use different input and output sample rates when using Ultralite Mk5 as capture device. 
- Configurations provided for 48, 96 and 192 kHz sample rates.

#### m4_2x4hd.yml

- This configuration uses a miniDSP 2x4HD as capture device. 
- Due to clock difference between loopback and M4, rate adjust and asynchronous resampling are enabled.
- Capture sample rate set to 96 kHz to match miniDSP 2x4HD sample rate. 
- Configuration provided for 96 kHz playback sample rate, but can be changed to any rate supported by M4.

#### m4_sa9227.yml

- This configuration uses a hifime S2 digi (SA9227) as capture device. 
- Due to clock difference between S2 digi and M4, rate adjust and asynchronous resampling are enabled. 
- Configurations provided for 44.1 and 192 kHz capture sample rate, but can be changed to match your source.

#### m4_ur23.yml

- This configuration uses a hifime UR23 as capture device. Rate adjust and asynchronous resampling are enabled to prevent buffer under/over runs as the UR23 and M4 have separate clocks and unlike an ALSA Loopback CamillaDSP has no ability to adjust the UR23 clock. Configurations are provided for 44.1 kHz and 192 kHz capture sample rates but this can be changed to match your source. Both provided configurations use a 192 kHz playback sample rate but this can be changed as desired as capture and playback devices are separate.
