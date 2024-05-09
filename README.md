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

1) Okto dac8 PRO - €1295, 8 channel balanced analog output, 8 channel AES digital input, 2 channel AES digital output, 1RU full-rack, volume knob, IR remote control, 5 V trigger, large display, excellent analog performance and overall design. Probably the highest performance 8 channel DAC. Okto dac8 PRO ASR Review.

2) MOTU Ultralite Mk5 - $600, 10 channel balanced analog output, 8 channel balanced analog input, TOSLINK input / output (also supports ADAT), SPDIF input / output, volume knob capable of controlling all analog outputs, 1RU half-rack, overall good analog performance. I recommend this DAC for most applications due to good analog performance, superior I/O functionality, reasonable price and smaller form factor. MOTU Ultralite Mk5 ASR Review.

3) MOTU M4 - $250, 4 channel unbalanced/balanced analog output, 4 channel balanced analog input, good analog performance. Good budget option for 2.1/2.2 or 2 way active systems, I/O functionality is rather limited. MOTU M4 ASR Review.

5) HifiBerry DAC8x - 

6) Whatever you have on hand! Part of the beauty of a CamillaDSP / RPi4 setup is that a RPi4 is cheap and available and if you want to try it out with another USB DAC it is rather easy to do so. Obviously I will not be able to provide specific configuration files but this tutorial should help you get started.

Although I am not providing configuration files for the following devices, I have used them successfully with CamillaDSP on a RPi4 and can help you with them if needed. In particular the MCHstreamer / USBstreamer are very useful as they allow you to use old pro audio interfaces with ADAT inputs to achieve 8 channels of output at 44.1/48 kHz.

- miniDSP MCHstreamer
- miniDSP USBstreamer
- Focusrite 18i20 2nd gen
- DIYINHK multichannel XMOS

Besides this tutorial what are other good sources of information?

[CamillaDSP GitHub](https://github.com/HEnquist/camilladsp)
Henrik has done a great job with the GitHub and it is an excellent reference. Almost everything I present here can also be found there.

[CamillaDSP DIYAudio Thread](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/)
If you want to ask a question about CamillaDSP this is where I would ask it. A good thread to search if you have questions on a particular topic.

[RPi4 + CamillaDSP Tutorial ASR Thread]https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/
This tutorial originally lived in this thread. It is a good place to discuss using CamillaDSP on a RPi as well as display / remote control integrations.

[Pi4 + CamillaDSP + MOTU M4 ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/pi4-camilladsp-audio-interface-motu-m4-phenomal-dsp-streamer.24493/)
This thread got me started with CamillaDSP.

[Budget Standalone Toslink > DSP > Toslink with CamillaDSP ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/budget-standalone-toslink-dsp-toslink-with-camilladsp-set-up-instructions-for-newbies.30830/)
Great thread by @MarcosCh showing how to make a low cost (< 50€ !) TOSLINK input / output stereo room correction DSP using CamillaDSP.

[Using a Raspberry Pi as equaliser in between an USB Source and USB DAC](https://www.audiosciencereview.com/forum/index.php?threads/using-a-raspberry-pi-as-equaliser-in-between-an-usb-source-ipad-and-usb-dac.25414/page-3#post-1180356)
Great thread from @DeLub on how to use a RPi as a USB gadget. Note, if you are using a recent version of Ubuntu or Raspberry Pi OS, steps 1-6 can be skipped (no need to compile kernel).

## CamillaDSP Setup

This part describes how to get a working CamillaDSP setup. Values in bold are user defined such as desired hostname and/or username for your RPi, everything else is universal and can be copy / pasted as-is. Items entered in code snippets are intended to be entered in terminal unless they are in italics in which case they are meant to be copy / pasted in to the file being edited in nano.

For reference, a complete install should take just under 1 hour (including display and FLIRC IR receiver setup), most of that time is waiting for things to download / install.

1-4) Write Raspberry Pi OS Lite (recommended) or Ubuntu Server 64 bit to micro SD card using Raspberry Pi Imager and login via SSH

Download and install Raspberry Pi Imager from the links below for your OS.

Raspberry Pi Imager for Ubuntu
Raspberry Pi Imager for Windows
Raspberry Pi Imager for macOS

A brief note on micro SD cards, I've been using a 32 GB Sandisk Extreme Pro, others have mentioned they have had good experience with 32 GB Sandisk Ultras. I do not think the specific micro SD card is super important but if things seem slow or you have data corruption issues you might try one of the cards mentioned above. I've also had good luck with USB SSDs but prefer SD cards as they keep everything tidier.

Open Raspberry Pi Imager and select your desired OS and micro SD card.

Setup your hostname, username, password, SSH and wifi settings and click the Write button to write OS to micro SD card.

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

5) Update / upgrade RPi

Open terminal and log in to RPi remotely via SSH.

Rich (BB code):
ssh username@hostname

Rich (BB code):
sudo apt update
sudo apt full-upgrade

Say yes to any prompts asking if you want to upgrade. You may be prompted about restarting services, if so just hit enter.

6) Install CamillaDSP

Make a camilladsp folder as well as folders for CamillaDSP to reference stored coefficients and configurations.

Rich (BB code):
mkdir ~/camilladsp ~/camilladsp/coeffs ~/camilladsp/configs

Install alsa-utils and git. This will give you access to helpful ALSA tools like aplay and amixer, it will also install libasound2 as a dependency which is required by CamillaDSP.

Rich (BB code):
sudo apt install alsa-utils git

Download and unpack CamillaDSP. The commands below will install V2.0.3 in /usr/local/bin/.

Rich (BB code):
wget https://github.com/HEnquist/camilladsp/releases/download/v2.0.3/camilladsp-linux-aarch64.tar.gz -P ~/camilladsp/
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/

7) Create CamillaDSP yml configuration file

Assuming you are using one of the DACs listed in this tutorial, see Part 3 for configuration files for a variety of use cases. Download the appropriate configuration file from the end of Part 3, for example for a MOTU Ultralite Mk5 streamer setup using a 44 kHz capture rate and a 96 kHz playback rate use "ultralitemk5_streamer_44c_96p_v2_12142023.yml". In Windows open this file up with notepad or wordpad, in Mac use textedit.

Copy the text in the configuration file and use nano to create an yml configuration file on your RPi. Paste the text from your configuration file in to nano and save the yml configuration file. Here is an example of creating a configuration file called ultralitemk5_streamer.yml but you can name the configuration file anything you like, it just needs to end in .yml.

Rich (BB code):
nano ~/camilladsp/configs/ultralitemk5_streamer.yml

As an alternative to using copy / paste in nano you can directly transfer the files to the RPi using scp. To do this you need to be in terminal on your local machine and NOT logged in to the RPi via SSH.

As an example for the Ultralite Mk5:

Rich (BB code):
sudo scp /path/to/configuration/on/local/machine/ultralitemk5_streamer_44c_96p_v2_12142023.yml username@hostname:/home/username/camilladsp/configs/ultralitemk5_streamer.yml

If you have a local copy of the file you are trying to get on the RPi you can use scp as an alternative to copy / pasting in nano anywhere in this tutorial. Many find nano difficult to use while text editors on Mac and PC are in general more user friendly and you have the benefit of a mouse.

As a reference for those using WSL you can navigate to the home directory of your WSL Ubuntu installation by going to \\wsl.localhost\Ubuntu\home in Windows Explorer and drag and drop the files you want to transfer there so they can easily be referenced in WSL.

8) Set up ALSA loopback

If you are using a physical input (AES, TOSLINK, SPDIF, analog) you can skip this step.

An ALSA loopback is a virtual soundcard that has two devices (0 and 1). A software player can be directed to play to Loopback device 1 which will then be rerouted to Loopback device 0, in this case Loopback device 0 now acts as a source that can be used as a CamillaDSP capture device.

By default, ALSA loopback is not installed on Ubuntu Server 64 bit. Run command below to install it.

Rich (BB code):
sudo apt install linux-modules-extra-raspi

Use nano to create snd-aloop.conf.

Rich (BB code):
sudo nano /etc/modules-load.d/snd-aloop.conf

Add line below to snd-aloop.conf and save.

Rich (BB code):
snd-aloop

Reboot RPi.

Rich (BB code):
sudo reboot

Log back in to RPi.

Rich (BB code):
ssh username@hostname

9) Try starting CamillaDSP

We will eventually install a service to automatically start CamillaDSP, but first try to start directly from terminal to make sure everything is working as expected. This example assumes a configuration file called ultralitemk5_streamer.yml, please update to the name of your configuration file.

Rich (BB code):
camilladsp -g-40 -p 1234 ~/camilladsp/configs/ultralitemk5_streamer.yml -v

You should see an output similar to what is shown below in terminal. As we added "-v" there will be a lot of good debugging information that can help you troubleshoot in case of an error. To exit enter crtl + c.

Rich (BB code):
username@hostname:~$ camilladsp -g-40 -p 1234 ~/camilladsp/configs/ultralitemk5_streamer.yml -v
2023-12-15 14:07:07.225478 INFO [src/bin.rs:683] CamillaDSP version 2.0.0
2023-12-15 14:07:07.225541 INFO [src/bin.rs:684] Running on linux, aarch64
2023-12-15 14:07:07.225656 DEBUG [src/bin.rs:728] Loaded state: None
2023-12-15 14:07:07.225678 DEBUG [src/bin.rs:732] Using command line argument for initial volume
2023-12-15 14:07:07.225691 DEBUG [src/bin.rs:755] Using default initial mute
2023-12-15 14:07:07.225702 DEBUG [src/bin.rs:765] Initial mute: [false, false, false, false, false]
2023-12-15 14:07:07.225716 DEBUG [src/bin.rs:766] Initial volume: [-40.0, -40.0, -40.0, -40.0, -40.0]
2023-12-15 14:07:07.225734 DEBUG [src/bin.rs:768] Read config file Some("/home/michael5/camilladsp/configs/ultralitemk5_streamer.yml")
2023-12-15 14:07:07.265438 DEBUG [src/bin.rs:808] Config is valid
2023-12-15 14:07:07.266044 DEBUG [src/socketserver.rs:432] Start websocket server on 127.0.0.1:1234
2023-12-15 14:07:07.266382 DEBUG [src/bin.rs:994] Wait for config
2023-12-15 14:07:07.266410 DEBUG [src/bin.rs:1010] Waiting to receive a command
2023-12-15 14:07:07.266426 DEBUG [src/bin.rs:1013] Config change command received
2023-12-15 14:07:07.266440 DEBUG [src/bin.rs:999] New config is available and there are no queued commands, continuing
2023-12-15 14:07:07.266453 DEBUG [src/bin.rs:1036] Config ready, start processing
2023-12-15 14:07:07.267173 DEBUG [src/bin.rs:157] Using channels [true, true]
2023-12-15 14:07:07.269284 DEBUG [src/filters.rs:488] Build new pipeline
2023-12-15 14:07:07.272542 DEBUG [src/processing.rs:19] build filters, waiting to start processing loop
2023-12-15 14:07:07.383996 DEBUG [src/alsadevice.rs:334] Available Playback devices: [("hw:Loopback,0,0", "Loopback, Loopback PCM, subdevice #0"), ("hw:Loopback,0,1", "Loopback, Loopback PCM, subdevice #1"), ("hw:Loopback,0,2", "Loopback, Loopback PCM, subdevice #2"), ("hw:Loopback,0,3", "Loopback, Loopback PCM, subdevice #3"), ("hw:Loopback,0,4", "Loopback, Loopback PCM, subdevice #4"), ("hw:Loopback,0,5", "Loopback, Loopback PCM, subdevice #5"), ("hw:Loopback,0,6", "Loopback, Loopback PCM, subdevice #6"), ("hw:Loopback,0,7", "Loopback, Loopback PCM, subdevice #7"), ("hw:Loopback,1,0", "Loopback, Loopback PCM, subdevice #0"), ("hw:Loopback,1,1", "Loopback, Loopback PCM, subdevice #1"), ("hw:Loopback,1,2", "Loopback, Loopback PCM, subdevice #2"), ("hw:Loopback,1,3", "Loopback, Loopback PCM, subdevice #3"), ("hw:Loopback,1,4", "Loopback, Loopback PCM, subdevice #4"), ("hw:Loopback,1,5", "Loopback, Loopback PCM, subdevice #5"), ("hw:Loopback,1,6", "Loopback, Loopback PCM, subdevice #6"), ("hw:Loopback,1,7", "Loopback, Loopback PCM, subdevice #7"), ("hw:Headphones,0,0", "bcm2835 Headphones, bcm2835 Headphones, subdevice #0"), ("hw:Headphones,0,1", "bcm2835 Headphones, bcm2835 Headphones, subdevice #1"), ("hw:Headphones,0,2", "bcm2835 Headphones, bcm2835 Headphones, subdevice #2"), ("hw:Headphones,0,3", "bcm2835 Headphones, bcm2835 Headphones, subdevice #3"), ("hw:Headphones,0,4", "bcm2835 Headphones, bcm2835 Headphones, subdevice #4"), ("hw:Headphones,0,5", "bcm2835 Headphones, bcm2835 Headphones, subdevice #5"), ("hw:Headphones,0,6", "bcm2835 Headphones, bcm2835 Headphones, subdevice #6"), ("hw:Headphones,0,7", "bcm2835 Headphones, bcm2835 Headphones, subdevice #7"), ("hw:UltraLitemk5,0,0", "UltraLite-mk5, USB Audio, subdevice #0"), ("null", "Discard all samples (playback) or generate zero samples (capture)"), ("hw:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\nDirect hardware device without any conversions"), ("hw:CARD=Loopback,DEV=1", "Loopback, Loopback PCM\nDirect hardware device without any conversions"), ("plughw:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\nHardware device with all software conversions"), ("plughw:CARD=Loopback,DEV=1", "Loopback, Loopback PCM\nHardware device with all software conversions"), ("default:CARD=Loopback", "Loopback, Loopback PCM\nDefault Audio Device"), ("sysdefault:CARD=Loopback", "Loopback, Loopback PCM\nDefault Audio Device"), ("front:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\nFront output / input"), ("surround21:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\n2.1 Surround output to Front and Subwoofer speakers"), ("surround40:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\n4.0 Surround output to Front and Rear speakers"), ("surround41:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\n4.1 Surround output to Front, Rear and Subwoofer speakers"), ("surround50:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\n5.0 Surround output to Front, Center and Rear speakers"), ("surround51:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\n5.1 Surround output to Front, Center, Rear and Subwoofer speakers"), ("surround71:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\n7.1 Surround output to Front, Center, Side, Rear and Woofer speakers"), ("dmix:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\nDirect sample mixing device"), ("dmix:CARD=Loopback,DEV=1", "Loopback, Loopback PCM\nDirect sample mixing device"), ("hw:CARD=Headphones,DEV=0", "bcm2835 Headphones, bcm2835 Headphones\nDirect hardware device without any conversions"), ("plughw:CARD=Headphones,DEV=0", "bcm2835 Headphones, bcm2835 Headphones\nHardware device with all software conversions"), ("default:CARD=Headphones", "bcm2835 Headphones, bcm2835 Headphones\nDefault Audio Device"), ("sysdefault:CARD=Headphones", "bcm2835 Headphones, bcm2835 Headphones\nDefault Audio Device"), ("dmix:CARD=Headphones,DEV=0", "bcm2835 Headphones, bcm2835 Headphones\nDirect sample mixing device"), ("hw:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nDirect hardware device without any conversions"), ("plughw:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nHardware device with all software conversions"), ("default:CARD=UltraLitemk5", "UltraLite-mk5, USB Audio\nDefault Audio Device"), ("sysdefault:CARD=UltraLitemk5", "UltraLite-mk5, USB Audio\nDefault Audio Device"), ("front:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nFront output / input"), ("surround21:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\n2.1 Surround output to Front and Subwoofer speakers"), ("surround40:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\n4.0 Surround output to Front and Rear speakers"), ("surround41:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\n4.1 Surround output to Front, Rear and Subwoofer speakers"), ("surround50:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\n5.0 Surround output to Front, Center and Rear speakers"), ("surround51:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\n5.1 Surround output to Front, Center, Rear and Subwoofer speakers"), ("surround71:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\n7.1 Surround output to Front, Center, Side, Rear and Woofer speakers"), ("iec958:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nIEC958 (S/PDIF) Digital Audio Output"), ("dmix:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nDirect sample mixing device")]
2023-12-15 14:07:07.390260 DEBUG [src/alsadevice.rs:352] Playback: supported channels, min: 10, max: 22, list: [10, 18, 22]
2023-12-15 14:07:07.390303 DEBUG [src/alsadevice.rs:353] Playback: setting channels to 10
2023-12-15 14:07:07.390405 DEBUG [src/alsadevice.rs:357] Playback: supported samplerates: Discrete([176400, 192000])
2023-12-15 14:07:07.390417 DEBUG [src/alsadevice.rs:358] Playback: setting rate to 192000
2023-12-15 14:07:07.390491 DEBUG [src/alsadevice.rs:362] Playback: supported sample formats: [S24LE3]
2023-12-15 14:07:07.390510 DEBUG [src/alsadevice.rs:363] Playback: setting format to S24LE3
2023-12-15 14:07:07.390592 DEBUG [src/alsadevice_buffermanager.rs:43] Setting buffer size to 8192 frames
2023-12-15 14:07:07.390643 DEBUG [src/alsadevice_buffermanager.rs:57] Device is using a buffer size of 8192 frames
2023-12-15 14:07:07.390654 DEBUG [src/alsadevice_buffermanager.rs:65] Setting period size to 1024 frames
2023-12-15 14:07:07.394799 DEBUG [src/alsadevice.rs:387] Opening Playback device "hw:UltraLitemk5" with parameters: HwParams { channels: Ok(10), rate: "Ok(192000) Hz", format: Ok(S243LE), access: Ok(RWInterleaved), period_size: "Ok(1024) frames", buffer_size: "Ok(8192) frames" }, SwParams(avail_min: Ok(4096) frames, start_threshold: Ok(1) frames, stop_threshold: Ok(8192) frames)
2023-12-15 14:07:07.394887 DEBUG [src/alsadevice.rs:392] Playback device "hw:UltraLitemk5" successfully opened
2023-12-15 14:07:07.395058 DEBUG [src/bin.rs:265] Playback thread ready to start
2023-12-15 14:07:07.394857 DEBUG [src/alsadevice.rs:334] Available Capture devices: [("hw:Loopback,0,0", "Loopback, Loopback PCM, subdevice #0"), ("hw:Loopback,0,1", "Loopback, Loopback PCM, subdevice #1"), ("hw:Loopback,0,2", "Loopback, Loopback PCM, subdevice #2"), ("hw:Loopback,0,3", "Loopback, Loopback PCM, subdevice #3"), ("hw:Loopback,0,4", "Loopback, Loopback PCM, subdevice #4"), ("hw:Loopback,0,5", "Loopback, Loopback PCM, subdevice #5"), ("hw:Loopback,0,6", "Loopback, Loopback PCM, subdevice #6"), ("hw:Loopback,0,7", "Loopback, Loopback PCM, subdevice #7"), ("hw:Loopback,1,0", "Loopback, Loopback PCM, subdevice #0"), ("hw:Loopback,1,1", "Loopback, Loopback PCM, subdevice #1"), ("hw:Loopback,1,2", "Loopback, Loopback PCM, subdevice #2"), ("hw:Loopback,1,3", "Loopback, Loopback PCM, subdevice #3"), ("hw:Loopback,1,4", "Loopback, Loopback PCM, subdevice #4"), ("hw:Loopback,1,5", "Loopback, Loopback PCM, subdevice #5"), ("hw:Loopback,1,6", "Loopback, Loopback PCM, subdevice #6"), ("hw:Loopback,1,7", "Loopback, Loopback PCM, subdevice #7"), ("hw:UltraLitemk5,0,0", "UltraLite-mk5, USB Audio, subdevice #0"), ("null", "Discard all samples (playback) or generate zero samples (capture)"), ("hw:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\nDirect hardware device without any conversions"), ("hw:CARD=Loopback,DEV=1", "Loopback, Loopback PCM\nDirect hardware device without any conversions"), ("plughw:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\nHardware device with all software conversions"), ("plughw:CARD=Loopback,DEV=1", "Loopback, Loopback PCM\nHardware device with all software conversions"), ("default:CARD=Loopback", "Loopback, Loopback PCM\nDefault Audio Device"), ("sysdefault:CARD=Loopback", "Loopback, Loopback PCM\nDefault Audio Device"), ("front:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\nFront output / input"), ("dsnoop:CARD=Loopback,DEV=0", "Loopback, Loopback PCM\nDirect sample snooping device"), ("dsnoop:CARD=Loopback,DEV=1", "Loopback, Loopback PCM\nDirect sample snooping device"), ("hw:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nDirect hardware device without any conversions"), ("plughw:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nHardware device with all software conversions"), ("default:CARD=UltraLitemk5", "UltraLite-mk5, USB Audio\nDefault Audio Device"), ("sysdefault:CARD=UltraLitemk5", "UltraLite-mk5, USB Audio\nDefault Audio Device"), ("front:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nFront output / input"), ("dsnoop:CARD=UltraLitemk5,DEV=0", "UltraLite-mk5, USB Audio\nDirect sample snooping device")]
2023-12-15 14:07:07.396101 DEBUG [src/alsadevice.rs:352] Capture: supported channels, min: 1, max: 32, list: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
2023-12-15 14:07:07.396129 DEBUG [src/alsadevice.rs:353] Capture: setting channels to 2
2023-12-15 14:07:07.396167 DEBUG [src/alsadevice.rs:357] Capture: supported samplerates: Range(8000, 192000)
2023-12-15 14:07:07.396176 DEBUG [src/alsadevice.rs:358] Capture: setting rate to 44100
2023-12-15 14:07:07.396202 DEBUG [src/alsadevice.rs:362] Capture: supported sample formats: [S16LE, S24LE, S24LE3, S32LE, FLOAT32LE]
2023-12-15 14:07:07.396210 DEBUG [src/alsadevice.rs:363] Capture: setting format to S32LE
2023-12-15 14:07:07.396243 DEBUG [src/alsadevice_buffermanager.rs:43] Setting buffer size to 2048 frames
2023-12-15 14:07:07.396277 DEBUG [src/alsadevice_buffermanager.rs:57] Device is using a buffer size of 2048 frames
2023-12-15 14:07:07.396286 DEBUG [src/alsadevice_buffermanager.rs:65] Setting period size to 256 frames
2023-12-15 14:07:07.396476 DEBUG [src/alsadevice.rs:387] Opening Capture device "hw:Loopback,0" with parameters: HwParams { channels: Ok(2), rate: "Ok(44100) Hz", format: Ok(S32LE), access: Ok(RWInterleaved), period_size: "Ok(256) frames", buffer_size: "Ok(2048) frames" }, SwParams(avail_min: Ok(940) frames, start_threshold: Ok(0) frames, stop_threshold: Ok(2048) frames)
2023-12-15 14:07:07.396531 DEBUG [src/alsadevice.rs:392] Capture device "hw:Loopback,0" successfully opened
2023-12-15 14:07:07.396725 DEBUG [src/bin.rs:275] Capture thread ready to start
2023-12-15 14:07:07.396749 DEBUG [src/bin.rs:278] Both capture and playback ready, release barrier
2023-12-15 14:07:07.396770 DEBUG [src/bin.rs:280] Supervisor loop starts now!
2023-12-15 14:07:07.396792 DEBUG [src/alsadevice.rs:951] Starting playback loop
2023-12-15 14:07:07.396810 DEBUG [src/alsadevice.rs:415] Playback loop uses a buffer of 4096 frames
2023-12-15 14:07:07.396808 DEBUG [src/processing.rs:21] Processing loop starts now!
2023-12-15 14:07:07.396918 DEBUG [src/alsadevice.rs:1037] Starting captureloop
2023-12-15 14:07:07.397451 INFO [src/alsadevice.rs:648] Capture device supports rate adjust
2023-12-15 14:07:07.397475 DEBUG [src/alsadevice.rs:657] Capture loop uses a buffer of 2048 frames
2023-12-15 14:07:07.397524 DEBUG [src/alsadevice.rs:253] Starting capture from state: SND_PCM_STATE_PREPARED, Ready to start
2023-12-15 14:07:07.439499 INFO [src/alsadevice.rs:142] PB: Starting playback from Prepared state
2023-12-15 14:07:07.461259 DEBUG [src/countertimer.rs:240] Number of values changed. New 10, prev 2. Clearing history.
2023-12-15 14:07:07.461344 DEBUG [src/countertimer.rs:240] Number of values changed. New 10, prev 2. Clearing history.
2023-12-15 14:07:08.577701 DEBUG [src/countertimer.rs:42] Pausing processing

10) Create CamillaDSP service

There is a significant change between CamillaDSP V1 and V2 in that V2 no longer uses the active_config.yml symlink. If upgrading to V2 please update your service.

Change the User field to reflect your username, as of V2 this service no longer runs as root. If run as root, CamillaDSP will create a statefile with root as owner and the GUI will NOT be able to modify it, running as a normal user prevents this.

"-s camilladsp/statefile.yml" tells CamillaDSP you are specifying a configuration via the GUI. You must also add "-w" to tell CamillaDSP to wait for a configuration to be applied via web socket if using the GUI.

“-g-40” sets CamillaDSP volume control to -40 dB every time it starts to avoid accidentally playing something really loud after a system restart. If you are NOT using CamillaDSP volume control please delete “-g-40”.

"-p 1234" is only necessary if you are using the GUI.

"-o camilladsp/camilladsp.log" will create a log file that you can view in the GUI for troubleshooting. You can increase the verbosity of this log by adding "-l debug".

Rich (BB code):
sudo nano /lib/systemd/system/camilladsp.service

Rich (BB code):
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

Enable camilladsp service.

Rich (BB code):
sudo systemctl enable camilladsp

Start camilladsp service.

Rich (BB code):
sudo service camilladsp start

11) Install python and dependencies

Rich (BB code):
sudo apt install python3 python3-pip python3-websocket python3-aiohttp python3-jsonschema python3-numpy python3-matplotlib unzip

If you are using Ubuntu Server 22.04 LTS, upgrade pip3. This is not required for Ubuntu Server 23.10.

Rich (BB code):
sudo pip3 install --upgrade pip

12) Install pycamilladsp

Download pycamilladsp and install. If you are using Ubuntu 22.04 LTS use the command below.

Rich (BB code):
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp.git

If using Ubuntu 23.10 add "--break-system-packages" to install packages not contained in the system repository. Note, adding "--break-system-packages" will cause the installation to fail if used on Ubuntu 22.04 LTS.

Rich (BB code):
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp.git --break-system-packages

13) Install pycamilladsp-plot

Download pyamilladsp-plot and install. If you are using Ubuntu 22.04 LTS use the command below.

Rich (BB code):
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp-plot.git

If using Ubuntu 23.10 add "--break-system-packages" to install packages not contained in the system repository. Note, adding "--break-system-packages" will cause the installation to fail if used on Ubuntu 22.04 LTS.

Rich (BB code):
sudo pip3 install git+https://github.com/HEnquist/pycamilladsp-plot.git --break-system-packages

14) Install GUI server

Commands below will install V2.1.0 of the GUI.

Rich (BB code):
wget https://github.com/HEnquist/camillagui-backend/releases/download/v2.1.0/camillagui.zip -P ~/camilladsp/
unzip ~/camilladsp/camillagui.zip -d ~/camilladsp/camillagui

15) Try starting GUI

As with CamillaDSP itself it is good practice to start the GUI directly from terminal before proceeding to creating service.

Rich (BB code):
python3 ~/camilladsp/camillagui/main.py

If all goes well you will see the following output. GUI is accessed via http://hostname:5005 from any web browser on your network. Note V1 used port 5000 and v2 now uses port 5005.

Again, use crtl + c to exit.

Rich (BB code):
username@hostname:~$ python3 ~/camilladsp/camillagui/main.py
======== Running on http://0.0.0.0:5005 ========
(Press CTRL+C to quit)

16) Create service to start GUI

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

17) Assign active configuration in GUI

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

