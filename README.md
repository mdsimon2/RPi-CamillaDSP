# RPi-CamillaDSP

## Introduction
Intent of this project is to provide guidance on implementing [CamillaDSP](https://github.com/HEnquist/camilladsp) on a RPi4/5. There is a lot of good information on [ASR](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/), [DIYAudio](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) and the [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp), but there also appears to be a lot of apprehension. My goal is to give concrete examples of how to use CamillaDSP with a variety of hardware to ease some of that apprehension. This tutorial originally lived at ASR, but in May 2024 I decided to migrate it to GitHub to make version management easier and provide a more universal location.

I would like to especially thank [@HEnquist](https://github.com/HEnquist) for developing CamillaDSP. I’ve long been skeptical of computer-based DSP but CamillaDSP is a game changer. It runs on minimal hardware, is easy to interface with a variety of devices and is exceptionally well designed. I’ve replaced all of my miniDSP systems with RPi4s running CamillaDSP and could not be happier.

I am not a programmer or DSP expert, my primary motivation is finding better ways to implement DIY active speakers. If you see a better way of doing something or want further explanation please speak up! These instructions have been developed as I learned how to implement CamillaDSP and found better ways to set it up, but I am always learning.

For archived versions of the tutorial that pre-date the migration to Github, see links below.

- [20-Oct-2022 Archive](https://drive.google.com/file/d/1y-vULEbXNjza7W4X1vQyIIH1r1GOCVpN/view?usp=sharing)
- [12-Dec-2023 Archive](https://drive.google.com/file/d/1MbB300dAJUEtBld14Qd4loA6hD94v67B/view?usp=share_link)
- [13-May-2024 Archive](https://drive.google.com/file/d/1SS70Ra2lkjtfXbIT7be4-WIjYCXNgC9c/view?usp=share_link)

## Background

### Why use CamillaDSP on a RPi?

This tutorial is geared towards 2 channel audio as it is somewhat difficult to get multichannel audio in to a RPi. Typical applications are DIY active speakers / subwoofers such as Directiva R1 (4+ channels), LXmini + sub(s) or LX 521.4 (8+ channels). Another good application is passive stereo speakers with 3+ subwoofers. Although it is possible to use other hardware with CamillaDSP, a RPi offers GPIO pins which are useful for [display](https://github.com/mdsimon2/RPi-CamillaDSP#oled-display) integration and has the ability to be used as a USB gadget.

### How does it work?

Starting point is a RPi4 or RPi5 running either Raspberry Pi OS Lite 64 bit or Ubuntu Server 64 bit. RPi4 is recommended over RPi5 due to lower cost and better thermal performance. However, RPi5 is required for multichannel I2S applications such as the HifiBerry DAC8x.

CamillaDSP will be installed such that it is always running on the RPi as a service. A web browser based GUI is available to configure CamillaDSP after initial setup.

CamillaDSP requires a capture device and playback device, the capture device is the input and playback device is the output. 

The capture device can be a variety of things, it can be the RPi itself with software audio players such as squeezelite or shairport-sync playing to an ALSA loopback, the same device as the playback device in the case of an audio interface with analog/digital inputs, or a separate device such as a TOSLINK to USB card. The main point here is that CamillaDSP is NOT limited to applications that use a RPi as a source.

The playback device is either a USB DAC/DDC, HDMI output of the RPi or HAT DAC/DDC. Between the capture device and the playback device is where the magic happens, CamillaDSP can implement channel routing, IIR filters, FIR filters, volume control (w/ dynamic loudness), resampling and delay. The RPi is surprising powerful and is able to do much more than any miniDSP product that exists today.

### What DACs are recommended?

1) [Okto dac8 PRO](https://www.oktoresearch.com/dac8pro.htm) - €1289, 8 channel balanced analog output, 8 channel AES digital input, 2 channel AES digital output, 1RU full-rack, volume knob, IR remote control, 5 V trigger, large display, excellent analog performance and overall design. [Okto dac8 PRO ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/review-and-measurements-of-okto-dac8-8ch-dac-amp.7064/).

2) [MOTU Ultralite Mk5](https://motu.com/en-us/products/gen5/ultralite-mk5/) - $650, 10 channel balanced analog output, 8 channel balanced analog input, TOSLINK input / output (also supports ADAT), SPDIF input / output, volume knob capable of controlling all analog outputs, 1RU half-rack, overall good analog performance.  [MOTU Ultralite Mk5 ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/motu-ultralite-mk5-review-audio-interface.24777/).

3) [MOTU M4](https://motu.com/en-us/products/m-series/m4/) - $250, 4 channel unbalanced/balanced analog output, 4 channel balanced analog input, good analog performance, USB powered. Good budget option for 2.1/2.2 or 2 way active systems, I/O functionality is rather limited. [MOTU M4 ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/motu-m4-audio-interface-review.15757/).

5) [HifiBerry DAC8x](https://www.hifiberry.com/shop/boards/hifiberry-dac8x/) - $65, requires a RPi5, HAT, 8 channel unbalanced analog output, good analog noise performance, acceptable distortion performance. Ultimate budget option! [HifiBerry DAC8x Measurements](https://www.audiosciencereview.com/forum/index.php?threads/8ch-hifiberry-hat-dac-for-rpi5.53672/post-1966410).

6) Whatever you have on hand! Part of the beauty of a CamillaDSP / RPi setup is that it is cheap and if you want to try CamillaDSP with another USB DAC it is rather easy to do so. 

Although configurations are not provided for the following devices, they have been used successfully with CamillaDSP on a RPi4. In particular the MCHstreamer / USBstreamer are very useful as they allow the use old pro audio interfaces with ADAT inputs to achieve 8 channels of output at 44.1/48 kHz.

- [miniDSP MCHstreamer](https://www.minidsp.com/products/usb-audio-interface/mchstreamer)
- [miniDSP USBstreamer](https://www.minidsp.com/products/usb-audio-interface/usbstreamer)
- [Focusrite 18i20 2nd gen](https://store.focusrite.com/en-gb/product/scarlett-18i20-2nd-gen/)
- [DIYINHK multichannel XMOS](https://www.diyinhk.com/shop/audio-kits/142-xmos-multichannel-high-quality-usb-tofrom-i2sdsd-spdif-pcb.html)

Below are other good sources of information related to CamillaDSP.

- [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp) - Henrik has done a great job with the GitHub and it is an excellent reference. Almost everything presented in this tutorial can also be found there.

- [CamillaDSP DIYAudio Thread](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) - If you want to ask a question about CamillaDSP this is the place to ask it. Also a great thread to search for further information on any CamillaDSP topic.

- [RPi4 + CamillaDSP Tutorial ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/) - This tutorial originally lived in this thread. It is a good place to discuss using CamillaDSP on a RPi as well as display / remote control integrations.

- [Pi4 + CamillaDSP + MOTU M4 ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/pi4-camilladsp-audio-interface-motu-m4-phenomal-dsp-streamer.24493/) - Excellent thread by [@armigo](https://www.audiosciencereview.com/forum/index.php?members/armigo.20011/) that helped inspire this tutorial. 

- [Budget Standalone Toslink > DSP > Toslink with CamillaDSP ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/budget-standalone-toslink-dsp-toslink-with-camilladsp-set-up-instructions-for-newbies.30830/) - Great thread by [@MCH](https://www.audiosciencereview.com/forum/index.php?members/mch.30254/) showing how to make a low cost (< 50€ !) TOSLINK input / output stereo room correction DSP using CamillaDSP.

- [Using a Raspberry Pi as equaliser in between an USB Source and USB DAC](https://www.audiosciencereview.com/forum/index.php?threads/using-a-raspberry-pi-as-equaliser-in-between-an-usb-source-ipad-and-usb-dac.25414/page-3#post-1180356) - Great thread from [@DeLub](https://www.audiosciencereview.com/forum/index.php?members/delub.16965/) on how to use a RPi as a USB gadget. Note, with Raspberry Pi OS Bookworm or Ubuntu Server 24.04, steps 1-6 can be skipped (no need to compile kernel).

## CamillaDSP Setup

This part describes how to get a working CamillaDSP setup. For reference, a complete install should take under 1 hour (including [OLED display](https://github.com/mdsimon2/RPi-CamillaDSP#oled-display) and [FLIRC IR receiver](https://github.com/mdsimon2/RPi-CamillaDSP#flirc-usb-ir-receiver) setup), most of that time is waiting for things to download / install.

### 1) Write OS to micro SD card and login to RPi via SSH

Raspberry Pi OS Lite 64 bit Bookworm is the recommended OS. Ubuntu Server 24.04 LTS 64 bit can also be used but does not currently work with the HifiBerry DAC8x.

Download and install Raspberry Pi Imager from the links below for your OS.

- [Raspberry Pi Imager for Ubuntu](https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb)
- [Raspberry Pi Imager for Windows](https://downloads.raspberrypi.org/imager/imager_latest.exe)
- [Raspberry Pi Imager for macOS](https://downloads.raspberrypi.org/imager/imager_latest.dmg)

Open Raspberry Pi Imager, select the desired RPi, OS and micro SD card. Setup your hostname, username, password, SSH and wifi settings and click the Write button to write OS to micro SD card.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/raspberrypi_imager_settings.png" alt="raspberrypi_imager_settings" width="300"/>

This install assumes the RPi will be managed remotely via SSH from a separate computer. With Mac or Linux, terminal will installed by default and commands in subsequent steps of this tutorial can be in terminal without issue.

With Windows 10 or 11 it is recommended to install Windows Subsystem for Linux (WSL). Instruction below are condensed version of this -> https://docs.microsoft.com/en-us/windows/wsl/install.

Open PowerShell as administrator as shown below.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/powershell.png" alt="powershell" width="300"/>

Run wsl --install in PowerShell and restart.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/wsl_install.png" alt="wsl_install" width="500"/>

Following the restart Ubuntu can be used for terminal access.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/Ubuntu.png" alt="Ubuntu" width="500"/>

### 2) Update / upgrade RPi

Open terminal and log in to RPi using your username and hostname.

```
ssh username@hostname
```

Update / upgrade RPi and install necessary tools and dependencies.

```
sudo apt update
sudo apt full-upgrade
sudo apt install alsa-utils git python3 python3-pip python3-websocket python3-aiohttp python3-jsonschema python3-numpy python3-matplotlib unzip
```

Say yes to any upgrade prompts. If prompted about restarting services, hit enter.

### 3) Install CamillaDSP

Make a camilladsp folder, as well as folders for CamillaDSP to reference stored FIR filters and configurations. Download and unpack CamillaDSP. The commands below will install V2.0.3 in /usr/local/bin/.

```
mkdir ~/camilladsp ~/camilladsp/coeffs ~/camilladsp/configs
wget https://github.com/HEnquist/camilladsp/releases/download/v2.0.3/camilladsp-linux-aarch64.tar.gz -P ~/camilladsp/
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/
```

### 4) Install CamillaDSP service

```
sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/camilladsp.service -P /lib/systemd/system/
```

Open CamillaDSP service in nano and update username to reflect your username.

```
sudo nano /lib/systemd/system/camilladsp.service
```

When done, enter ctrl + x to exit nano, when prompted with 'Save modified buffer?' enter Y and when prompted with 'File Name to Write: /lib/systemd/system/camilladsp.service' hit Enter key. This same technique will be used elsewhere in this tutorial when editing files in nano.

Enable and start camilladsp service.

```
sudo systemctl enable camilladsp
sudo service camilladsp start
```

See below for a brief explanation of the CamillaDSP flags applied in ExecStart of the service.


"-s camilladsp/statefile.yml" tells CamillaDSP a configuration will be specified via the GUI.

"-w" tells CamillaDSP to wait for a configuration to be applied via the GUI.

“-g-40” sets CamillaDSP volume control to -40 dB every time it starts to avoid accidentally playing something really loud after a system restart. If not using CamillaDSP volume control please delete “-g-40”.

"-p 1234" is needed to connect to the GUI.

"-o camilladsp/camilladsp.log" creates a log file that can be viewed in the GUI for troubleshooting. Verbosity of this log can be increased by adding "-l debug".

### 5) Install GUI server

```
wget https://github.com/HEnquist/camillagui-backend/releases/download/v2.1.1/camillagui.zip -P ~/camilladsp/
unzip ~/camilladsp/camillagui.zip -d ~/camilladsp/camillagui
```

### 6) Install GUI service

```
sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/camillagui.service -P /lib/systemd/system/
```

Open GUI service in nano and update username to reflect your username.

```
sudo nano /lib/systemd/system/camillagui.service
```

Enable and start camillagui service.

```
sudo systemctl enable camillagui
sudo service camillagui start
```

4) Enable ALSA loopback (optional)

This step is only required for [streamer applications](https://github.com/mdsimon2/RPi-CamillaDSP#streamer-applications) using an ALSA loopback.

```
echo 'snd-aloop' | sudo tee -a /etc/modules-load.d/snd-aloop.conf > /dev/null
```

Restart RPi for the change to take effect.

```
sudo reboot now
```

### 5) Enable USB gadget (optional)

The RPi4/5 can be used as USB input / output device, this is known as a USB gadget. This step is only required for configurations using the USB gadget as capture device. See USB gadget configuration section for more detail.

Open config.txt in nano.

```
sudo nano /boot/firmware/config.txt
```

Add the line below.

```
dtoverlay=dwc2
```

Create usb_g_audio.conf with desired parameters

```
echo 'options g_audio c_srate=44100 c_ssize=4 c_chmask=3 p_chmask=0' | sudo tee -a /etc/modprobe.d/usb_g_audio.conf > /dev/null 
```
"c_srate" sets the capture rates that will be offered to the USB host. Feel free to add / delete rates as necessary. It is important to note that your USB host must be set to the same rate as the CamillaDSP capture rate. There are tools that can automatically switch the CamillaDSP capture rate such as [gaudio_ctl](https://github.com/pavhofman/gaudio_ctl) and [camilladsp-setrate](https://github.com/marcoevang/camilladsp-setrate) but they are outside the scope of this tutorial.

"c_ssize" sets the capture rate format offered to the USB host. 4 = S32_LE.

"c_chmask" sets the number of capture channels. Format is 2^(number of channels) - 1. Therefore, 3 = 2 channels, 63 = 6 channels and 255 = 8 channels.

"p_chmask" sets the number of playback channels offered to the RPi. This is set to 0 as as the gadget is typically only used as a capture device.

Restart RPi for the change to take effect.

```
sudo reboot now
```

### 6) Assign active configuration in GUI

Configurations are explained in more detail in the [CamillaDSP Configurations](https://github.com/mdsimon2/RPi-CamillaDSP#camilladsp-configurations) section of this tutorial. Pre-made configurations for the DACs in this tutorial can be downloaded by navigating to the [configs](https://github.com/mdsimon2/RPi-CamillaDSP/tree/main/configs) folder of this repository. Alternatively, download the entire repository by clicking [here](https://github.com/mdsimon2/RPi-CamillaDSP/archive/refs/heads/main.zip) or using git clone.

On a computer that is on the same network as the RPi, navigate browser to http://hostname:5005.

Navigate to Files tab of GUI and upload desired configuration using the up arrow in the Configs section. Set this configuration as active by pressing the "star" next to the configuration. From now on CamillaDSP and the GUI will start with this configuration loaded. Click the "Apply and Save" button in the lower left to load the configuration to DSP.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/configs.png" alt="configs" width="600"/>

Congratulations, CamillaDSP is now up and running!

### 7) Upgrading to future versions

To upgrade to a new version of CamillaDSP, simply remove the old CamillaDSP binary and tar and download and extract a new one.

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

For streamer applications this tutorial assumes the software player outputs 44.1 kHz and resamples everything that is not 44.1 kHz to accomplish this. 

This tutorial covers how to install shairport-sync and squeezelite. Other players can be used as long as they output 44.1 kHz and can play to an ALSA loopback.

### shairport-sync

Install shairport-sync and SOX.

```
sudo apt install shairport-sync libsoxr-dev
```

After installation there are some items which require configuration.

Open shairport-sync.conf in nano.

```
sudo nano /etc/shairport-sync.conf
```

Uncomment the following lines (delete // from start of line) and make changes shown below.

```
interpolation = "soxr";
output_device = "hw:Loopback,1";
```

Using SOX for interpolation should avoid audible artifacts from clock syncing. The last line sets the output device to ALSA loopback device 1. Airplay will automatically resample to 44.1 kHz sample rate by default.

Restart shairport-sync service to reflect changes in shairport-sync.conf

```
sudo service shairport-sync restart
```

### squeezelite

Install squeezelite.

```
sudo apt install squeezelite
```

Like shairport-sync, a few changes are required to the squeezelite configuration. Copy and paste the lines shown below to the end of the file using nano.

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

These changes set ALSA loopback device 1 as squeezelite playback device, resample all files to 44.1 kHz using a high quality resampling algorithm and stop squeezelite after 5 seconds of inactivity.

## CamillaDSP Configurations

All configurations use maximum amount of output channels for a given playback device. If an output channel is not needed remove it from the mixer as each extra channel requires additional processing resources. Configuration files can be found in the [configs](https://github.com/mdsimon2/RPi-CamillaDSP/tree/main/configs) folder of this repository.

The naming convention configuration files in this repository is dac_input_capturerate_playbackrate. For example, a configuration for a MOTU Ultralite Mk5, TOSLINK input with 96 kHz capture and 96 kHz playback rates is ultralitemk5_toslink_96c_96p.

### ASRC Options
CamillaDSP expects a constant capture sample rate and cannot accommodate rate changes without a restart. For variable sample rate physical digital sources like TOSLINK, AES or SPDIF or multiple physical digital sources with different rates, a good option is to add a device that has an ASRC to convert to a consistent rate. miniDSP offer many devices with this capability which are summarized summarized below.

- [nanoDIGI](https://www.minidsp.com/images/documents/nanoDIGI%202x8%20User%20Manual.pdf) - $170, discontinued in 2021 but possible to find used, SPDIF / TOSLINK input, SPDIF output, 96 kHz
- [2x4HD](https://www.minidsp.com/products/minidsp-in-a-box/minidsp-2x4-hd) - $225, TOSLINK / analog input, USB output, 96 kHz
- [miniDSP OpenDRC-DI](https://www.minidsp.com/products/opendrc-series/opendrc-di) - $325, AES / SPDIF / TOSLINK input and output, 48 or 96 kHz
- [Flex Digital](https://www.minidsp.com/products/minidsp-in-a-box/flex) - $495, SPDIF / TOSLINK / USB / analog / bluetooth input, SPDIF / TOSLINK / USB output, 96 kHz
- [Flex Analog](https://www.minidsp.com/products/minidsp-in-a-box/flex) $495-470, SPDIF / TOSLINK / analog / bluetooth input, USB Output, 96 kHz
- [SHD Studio](https://www.minidsp.com/products/streaming-hd-series/shd-studio) - $900, AES / SPDIF / TOSLINK / USB / streamer input, SPDIF / AES / USB output, 96 kHz
- [SHD](https://www.minidsp.com/products/streaming-hd-series/shd) - $1250, AES / SPDIF / TOSLINK / USB / streamer / analog input, SPDIF / AES / USB output, 96 kHz

These devices can do IR volume control, although not all have displays for volume / input identification.

2x4HD and Flex can be upgraded to Dirac versions but sample rate will change from 96 kHz to 48 kHz.

In order to use USB output of devices like 2x4HD, Flex and SHD they need to be set as capture device in CamillaDSP. Unfortunately this ties up the USB input and makes it unusable. Still, this is a good approach to add extra input functionality to basic USB DACs like the MOTU M4 or Topping DM7 which only have USB input.

For constant sample rate digital sources the following devices work well. Compared to other solutions like the HiFiBerry Digi+ I/O they handle signal interruptions gracefully. These devices are used in a similar way to the miniDSPs with USB outputs, the device is set as the CamillaDSP capture device. Note, that although the S2 digi also has a TOSLINK output, it is not recommended due to audible dropouts.

- [hifime S2 digi (SA9227)](https://hifimediy.com/product/s2-digi/) - $40, TOSLINK input, USB output, sample rates up to 192 kHz
- [hifime UR23](https://hifimediy.com/product/hifime-ur23-spdif-optical-to-usb-converter/) - $25, TOSLINK input, USB output, does NOT work with RPi5, sample rates up to 96 kHz

### chunksize / target_level

CamillaDSP V1 used a buffer size of 2 x chunksize, CamillaDSP V2 uses a buffer size of 4 x chunksize. In previous versions of this tutorial a rather long chunksize was specified (44.1/48 = 1024, 88.2/96 = 2048, 176.4/192 = 4096) resulting in long latency. After some experimentation, it was found that much lower chunksizes are stable. The configurations in this repository now use the following chunksize depending on playback sample rate.

- 44.1 / 48 kHz: 64
- 88.2 / 96 kHz: 128
- 176.4 / 192 kHz: 256

For configurations where playback and capture device are synchronous (i.e. no rate adjust is enabled), target_level = chunksize. For asynchronous configurations, target_level = 3 x chunksize.

These chunksize / target_level settings will result in < 10 ms latency. If dropouts are experienced, increase chunksize / target_level, and please let me know.

### Okto dac8 PRO

These configurations assume CamillaDSP volume control is NOT being used as the Okto has a nice display with volume knob and IR control. As volume control is downstream of CamillaDSP, digital clipping in CamillaDSP is more of an issue. As a result, 1 dB attenuation has been added to all output channels of configurations that implement resampling to help avoid clipping. In general, if boost is added to a configuration, offset that boost by attenuating the output further. Use the CamillaDSP clipping indicator to gauge if there is enough attenuation to avoid digital clipping.

#### okto_streamer.yml

- Set Okto to Pure USB mode via front panel.
- All streamer configurations expect 44.1 kHz input. 
- Due to clock difference between loopback and Okto, rate adjust is enabled.
- Configurations provided for 44.1, 96 and 192 kHz playback sample rates.

#### okto_aes.yml

- Set Okto to USB / AES mode via front panel.
- This configuration uses AES inputs 1-2 but other AES inputs can be added as needed.
- No rate adjust is enabled as Okto is clocked by AES input in this mode.
- It is not possible to use different input and output sample rates when using Okto as capture device.
- Configurations provided for 48, 96 and 192 kHz sample rates.

### MOTU Ultralite Mk5

This DAC requires some configuration prior to use, either while connected to a Mac / PC or connected to the RPi and managed remotely via nginx.

#### nginx

Install nginx.

```
sudo apt install nginx-full
```

Open nginx.conf in nano.

```
sudo nano /etc/nginx/nginx.conf
```

Paste the text below to the end of nginx.conf, update the IP address shown on the front panel of the Ultralite Mk5.

```
stream {
    upstream portforward {
    
# replace «xx..xx» to the ip-address of the sound card from the About menu
        server 169.254.117.240:1280;
    }

    server {
        listen 1280;
        proxy_pass portforward;
    }
}
```

Restart nginx service.

```
sudo service nginx restart
```

Ultralite Mk5 should automatically connect to the network if using Raspberry Pi OS, if using Ubuntu Server, use the following instructions.

Find the network device name of the Ultralite Mk5.

```
ip a
```

Output should look something like this, enx0001f2fff075 is the network device name in this example.

```
: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether dc:a6:32:7d:4c:dc brd ff:ff:ff:ff:ff:ff
3: enx0001f2fff075: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 00:01:f2:ff:f0:75 brd ff:ff:ff:ff:ff:ff
4: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether dc:a6:32:7d:4c:dd brd ff:ff:ff:ff:ff:ff
    inet 192.168.86.25/24 metric 600 brd 192.168.86.255 scope global dynamic wlan0
       valid_lft 85792sec preferred_lft 85792sec
    inet6 2601:406:4300:910:dea6:32ff:fe7d:4cdd/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 86294sec preferred_lft 86294sec
    inet6 fe80::dea6:32ff:fe7d:4cdd/64 scope link
       valid_lft forever preferred_lft forever
```

Update network configuration to include the Ultralite Mk5. Use an IP address where the third number is one greater than the actual IP address reported on the front panel, followed by /16. For example, if the front panel reports 169.254.117.240, enter 169.254.118.240/16.

```
sudo cp /etc/netplan/50-cloud-init.yaml /etc/cloud/cloud.cfg.d/50-curtin-networking.cfg
sudo nano /etc/cloud/cloud.cfg.d/50-curtin-networking.cfg
```

Paste the following text to the bottom of 50-curtin-networking.cfg, updating the IP address using the guidance above. ethernets should be at the same indentation level as wifis.

```
    ethernets:
         enx0001f2fff075:
            addresses:
                - 169.254.118.240/16
```

Apply changes and restart.

```
sudo cloud-init clean
sudo cloud-init init
sudo reboot now
```

#### CueMix

Install Cuemix 5 on a Mac / PC. Either connect the Ultralite Mk5 to the Mac / PC or click the gear in Cuemix and enter the hostname of the RPi if managing remotely with nginx.

Set up channel routing such that USB 1-2 are routed to analog output 1-2, USB 3-4 to analog output 3-4, etc. Make sure no other channel routing is in place, as all channel routing will be done in CamillaDSP. Check the levels in the Output tab as the Ultralite Mk5 may come with all channels set to -20 dB by default. To use the Mk5 volume knob, select which analog channels (knob will only work on analog channels) should be controlled by the knob in the Output tab. See screenshots below for what this should look like.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/cuemix_main_1-2.png" alt="cuemix_main_1-2" width="500"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/cuemix_main_3-4.png" alt="cuemix_main_3-4" width="500"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/cuemix_output.png" alt="cuemix_output" width="500"/>

It is a good idea to update the firmware at this time. 

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

Once channel routing is set in Cuemix, this DAC is very similar to the Okto in terms of setup, just with more inputs / output options. Although the Ultralite Mk5 has a volume knob, you may want to use CamillaDSP for volume control with the Mk5 as it does not have an IR receiver. See [FLIRC IR Receiver](https://github.com/mdsimon2/RPi-CamillaDSP#flirc-usb-ir-receiver) and [OLED Display](https://github.com/mdsimon2/RPi-CamillaDSP#oled-display) sections of this tutorial for more information.

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
- This configuration uses analog inputs 3-4 but you can add/change to other inputs as needed.
- It is not possible to use different input and output sample rates when using Ultralite Mk5 as capture device.
- Configurations provided for 48, 96 and 192 kHz sample rates.

### MOTU M4

Given lack of 4 channel on device volume control, it is recommended to use CamillaDSP volume control with this DAC. Due limited input functionality, a variety of configurations with external input devices are provided, similar configurations can be used with any DAC in this tutorial.

#### m4_streamer.yml

- All streamer configurations expect 44.1 kHz input. 
- Due to clock difference between loopback and M4, rate adjust is enabled. 
- Configurations provided for 44.1, 96 and 192 kHz sample rates.

#### m4_analog.yml

- This configuration uses analog inputs 3-4 but you can use others if needed. 
- It is not possible to use different input and output sample rates when using M4 as capture device. 
- Configurations provided for 48, 96 and 192 kHz sample rates.

#### m4_2x4hd.yml

- This configuration uses a miniDSP 2x4HD as capture device. 
- Due to clock difference between loopback and M4, rate adjust and asynchronous resampling are enabled.
- Capture sample rate set to 96 kHz to match miniDSP 2x4HD sample rate. 
- Configuration provided for 96 kHz playback sample rate, but can be changed to any rate supported by M4.

#### m4_sa9227.yml

- This configuration uses a hifime S2 digi (SA9227) as capture device. 
- Due to clock difference between S2 digi and M4, rate adjust and asynchronous resampling are enabled. 
- Configuration provided for 44.1 and 192 kHz capture sample rate, but can be changed to match the source.
- Playback sample rate set to device maximum of 192 kHz.

#### m4_ur23.yml

- This configuration uses a hifime UR23 as capture device.
- Due to clock difference between UR23 and M4, rate adjust and asynchronous resampling are enabled. 
- Capture sample rate set to device maximum of 96 kHz, but can be changed to match the source.
- Configuration provided for 96 and 192 kHz playback sample rate.

### HifiBerry DAC8x

This is the only HAT option in the tutorial. As it uses multichannel I2S output, it must be used with a RPi5. Due to lack of volume control, it is recommended to use CamillaDSP volume control with this DAC.

A small addition is required to config.txt for this DAC to be recognized.

```
sudo nano /boot/firmware/config.txt
```

Add the line below.

```
dtoverlay=dtoverlay=hifiberry-dac8x
```

After a RPi reboot, it should be recognized.


## Advanced Configuration

### GUI

Access the GUI via any computer on the same network as the RPi by navigating a browser to http://hostname:5005.

#### Title

As of CamillaDSP V2, the first tab is Title. There isn't much to do in this tab, but the title and description fields can be populated. The title field is displayed on the first line of the [OLED display](https://github.com/mdsimon2/RPi-CamillaDSP#oled-display) described later in this tutorial.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/title.png" alt="title" width="600"/>

#### Devices

The Devices tab defines general parameters like capture device, playback device, sample rate, rate adjust, resampling and chunk size.

It is very important that sample format and channel count are supported by the device. If using configurations from this repository this will not be an issue, but if creating new configurations it is something to be aware of.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/devices.png" alt="devices" width="600"/>

#### Filters

In the Filters tab a variety of filters can be created. A big advantage of using the GUI over a manual configuration file is that it will prompt for the necessary information for a given filter type. Once a filter is created, magnitude / phase / group delay can be viewed. For questions about specific filter implementation, see the [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp). Creating a filter in the Filters tab does not apply it to the pipeline, it just creates a filter that will be available to apply in the pipeline.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/filters.png" alt="filters" width="600"/>

#### Mixers

The Mixers tab defines channel routing, in addition, gain and polarity can be defined for each channel. Like filters, mixers will not be in effect until applied in the pipeline.

As in the Devices tab, it is very important that mixer channel counts exactly match the channel counts of the device. For configurations from this repository this will not be an issue. It is not required to use all channels in the mixer, but the correct channel counts need to specified in the "in" and "out" section. For example in the screenshot below 8 input and 8 output channels are specified although only 2 input channels (0 and 1) are used in the mixer definition.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/mixers.png" alt="mixers" width="600"/>

#### Processors

A new addition with CamillaDSP V2 is the Processors tab. I haven't used this personally, but you can use it to implement a compressor.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/processors.png" alt="processors" width="600"/>

#### Pipeline

The Pipeline tab is where everything comes together. Filters, mixers and processors created in the previous tabs are applied here. The entire pipeline can be plotted to show how the mixer and filters are applied as well as the combined magnitude / phase / group delay on each channel.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/pipeline.png" alt="pipeline" width="800"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/pipeline_map.png" alt="pipeline_map" width="800"/>

#### Files

The Files tab stores configurations and convolution filters. It will show configuration files located in ~/camilladsp/configs/ and convolution filters located in ~/camilladsp/coeffs/. Configurations and convolution filters can be downloaded / uploaded to/from via this tab. 

To load a configuration in the GUI, press the clockwise arrow button next to the desired configuration. Once this is done, the configuration name appear in the lower left under "Config", in the screenshot below, a configuration called lxminibsc.yml is loaded in the GUI.

Just because a configuration is loaded in the GUI does NOT mean it is actually applied to the DSP. To apply a configuration to the DSP, click the "Apply to DSP" button. This will apply the configuration in the GUI to the DSP but it will NOT save any changes made via the GUI. To save changes, click the "Save to File" button. To implement both of these operations at the same time, click the "Apply and save" button. Alternatively, use the "Apply automatically" and "Save automatically" check boxes to do these operations automatically after a change is made in the GUI.

To see what settings are currently applied to the DSP, click the "Fetch from DSP" button and to load the GUI with the current DSP settings. Note, it only pulls the settings and does NOT change the configuration name in the lower left.

In order to set a configuration as default (i.e. the configuration that will be loaded when CamillaDSP starts), click the star button next to the desired configuration. After this is done, the star button will now be green next to the default configuration.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/files.png" alt="files" width="600"/>

There is a compact view that is great for changing volume or configurations from a smartphone or tablet. It can be accessed by clicking the "Change to compact view" button just to the right of the CamillaDSP logo.

If filters named "Bass" and "Treble" are created and applied, the sliders in this view can be used as bass / treble tone controls. Recommended parameters for bass and treble tone control are lowshelf, f=85 Hz, q=0.9 and highshelf, f=6500 Hz, q=0.7 respectively.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/compact_view.png" alt="files" width="300"/>

### FLIRC USB IR Receiver

A [FLIRC IR receiver](https://flirc.tv/more/flirc-usb) is an easy way to add IR volume control for around $20. A python script has been created so setting this up is very easy. 

Download the FLIRC software on a Mac / PC and connect the FLIRC receiver to that computer. Use the software to pair a remote as shown below.

- KEY_UP = volume up
- KEY_DOWN = volume down
- KEY_LEFT = mute
- KEY_RIGHT = source change

The source change functionality will switch between any configuration that has "_" in front of the name. For example, for the following configurations:

- _ultralitemk5_toslink48.yml
- _ultralitemk5_streamer.yml
- _ultralitemk5_analog.yml
- ultralitemk5_streamer.yml

Pressing KEY_RIGHT will switch between:

- _ultralitemk5_toslink48.yml
- _ultralitemk5_streamer.yml
- _ultralitemk5_analog.yml 

However, will not switch to ultralitemk5_streamer.yml because it does not start with "_".

Pressing KEY_LEFT will mute CamillaDSP, if configurations are switched this mute will stay set. Volume can be changed while muted. The mute will be removed by either pressing KEY_LEFT again or unmuting in the GUI.

Install evdev.

```
sudo apt install python3-evdev
```

Install flirc.py.

```
wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/flirc.py -P ~/
```

Enable USB-C port for use, this is needed to run the IR receiver from the USB-C port as is implemented in the [Modushop Case](https://github.com/mdsimon2/RPi-CamillaDSP#modushop-case) design in this tutorial . If the FLIRC is plugged in to a USB-A port this step is not required.

Open config.txt in nano.

```
sudo nano /boot/firmware/config.txt
```

Below "arm_64bit=1", add line containing "dtoverlay=dwc2,_dr_mode=host". On the Ubuntu Server, "dtoverlay=dwc2" will already be present, on Raspberry Pi OS there is no entry below "arm_64bit=1". The end result should like below. Reboot the RPi for the changes to take effect.

```
# Config settings specific to arm64
arm_64bit=1
dtoverlay=dwc2,dr_mode=host
```

Check that the FLIRC is recognized.

```
lsusb
```

There should be an entry for Clay Logic flirc as shown below.

```
Bus 003 Device 002: ID 20a0:0006 Clay Logic flirc
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 006: ID 07fd:000c Mark of the Unicorn UltraLite-mk5
Bus 001 Device 005: ID 07fd:0008 Mark of the Unicorn M Series
Bus 001 Device 004: ID 262a:10e7 SAVITECH Corp. UR23 USB SPDIF Rx
Bus 001 Device 002: ID 2109:3431 VIA Labs, Inc. Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

Next check the FLIRC device name.

```
ls /dev/input/by-id/
```

Expected output is:

```
username@hostname:~$ ls /dev/input/by-id/
usb-flirc.tv_flirc-if01-event-kbd
```

If this looks different, potentially like usb-flirc.tv_flirc_E7A648F650554C39322E3120FF08122E-if01-event-kbd, modify flirc.py to reflect this.

```
nano ~/flirc.py
```

If needed, change the flirc=evdev.InputDevice line near the top to reflect the FLIRC device name.

```
flirc=evdev.InputDevice('/dev/input/by-id/usb-flirc.tv_flirc-if01-event-kbd')
```

Install FLIRC service.

```
sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/flirc.service -P /lib/systemd/system/
```

Change username to reflect your username.

```
sudo nano /lib/systemd/system/flirc.service
```

Enable FLIRC service.

```
sudo systemctl enable flirc
```

Start FLIRC service.

```
sudo service flirc start
```

### Trigger Output

It is easy to add a trigger output to the Ultralite Mk5 using a [Bobwire DAT1](https://www.bobwireaudio.com/). Simply connect the TOSLINK output of the Ultralite Mk5 to the Bobwire DAT1 and use the Audio Detect output port. All configuration files in this tutorial are set to stop after 5 seconds of output less than -100 dB, as a result CamillaDSP will stop after 5 seconds and after 60 seconds the trigger from the Bobwire DAT1 will turn any connected amplifiers off. Once CamillaDSP starts playing, the Bobwire DAT1 trigger will activate.

### OLED Display

RPis have GPIO pins which can be used to interface with a variety of displays. A python script has been developed for the [buydisplay.com 3.2” diagonal SSD1322 OLED display](https://www.buydisplay.com/white-3-2-inch-arduino-raspberry-pi-oled-display-module-256x64-spi) which is ~$30 + shipping. Be sure to order the display in the 6800 8 bit configuration. It is recommended to have them solder a pin header as it is only an additional cost of $0.59.

The base setup turns the display off after 10 seconds of no volume changes to avoid OLED burn in. It will turn back on if the volume, status or configuration are changed. 

Two versions of the OLED python script are provided. The default uses lgpio and is supported by both the RPi4 and RPi5. An alternative configuration is provided which uses rpi-gpio, this is only supported by the RPi4 and is slightly faster.

If using the default lgpio routine, install lgpio and oled.py.

```
sudo apt install python3-lgpio
wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/oled.py -P ~/
```

If using the alternative rpi-gpio routine, install rpi-gpio and oled-rpi.gpio.py.

```
sudo apt install python3-rpi.gpio
wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/oled-rpi.gpio.py -P ~/
mv ~/oled-rpi.gpio.py ~/oled.py
```

Install OLED service.

```
sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/oled.service -P /lib/systemd/system/
```
If using a RPi5, change the gpiochip specified in oled.py.

```
nano ~/oled.py
```

Uncomment the RPi5 line and comment out the RPi4 line so it looks like below.

```
#chip = sbc.gpiochip_open(0) #use this for RPi4
chip = sbc.gpiochip_open(4) #use this for RPi5
```

Open OLED service in nano and update username to reflect your username

```
sudo nano /lib/systemd/system/oled.service
```

Enable OLED service.

```
sudo systemctl enable oled
```

Start OLED service.

```
sudo service oled start
```
The python script has the ability to show user defined text on the first line of the display based on loaded configuration file. With CamillaDSP V2, this will show the title field under the Title tab of the GUI. If this field is blank, "CamillaDSP" will be displayed.

Wiring configuration from the display to the RPi GPIO header is listed below. Note, these pins can be changed as desired, see here for more information on RPi pinout -> https://www.tomshardware.com/reviews/raspberry-pi-gpio-pinout,6122.html. Please note the wiring configuration has been changed from earlier versions of the tutorial to accommodate the HifiBerry DAC8x, the old pin configurations are shown in parenthesis for the pins that have changed.

1) (ground) -> ground
2) (supply voltage) -> 3.3 V
3) (no connection) -> no connection
4) (data bus 0) -> GPIO 15 (GPIO 26)
5) (data bus 1) -> GPIO 13
6) (data bus 2) -> GPIO 6
7) (data bus 3) -> GPIO 5
8) (data bus 4) -> GPIO 7 (GPIO 22)
9) (data bus 5) -> GPIO 2 (GPIO 27)
10) (data bus 6) -> GPIO 17
11) (data bus 7) -> GPIO 3 (GPIO 18)
12) (enable) -> GPIO 14 (GPIO 23)
13) (read/write) -> ground
14) (data/command) -> GPIO 16
15) (reset) -> GPIO 12
16) (chip select)-> GPIO 8 (GPIO 25)

For wiring, prefabbed 8” long 0.1” header jumpers are recommended. These are a bit long but allow the removal the front panel with the wiring remaining connected.

### Modushop Case

[Modushop](https://modushop.biz/site/) offers CNC machining of aluminum cases for custom projects. Depending on exchange rates and shipping costs, ordering directly from Modushop may be slightly cheaper than ordering from [DIYAudio Store](https://diyaudiostore.com) which is the US distributor. All cases are based on the Galaxy GX247 chassis (230 mm x 170 mm x 40 mm) with 2 mm aluminum covers.

Case designs discussed below are intended for use with an [OLED Display](https://github.com/mdsimon2/RPi-CamillaDSP#oled-display), [FLIRC IR Receiver](https://github.com/mdsimon2/RPi-CamillaDSP#flirc-usb-ir-receiver) and RPi4. A RPi5 can be used but the back panel will not work as the USB/ethernet orientation has been reversed compared to the RPi4. If using a RPi5, either modify the rear panel drawing or leave the back panel off. Drawings in dwg, pdf and vsdx format can be found in the [case_drawings](https://github.com/mdsimon2/RPi-CamillaDSP/tree/main/case_drawings) folder of this repository.

All USB-A ports are located on the rear of the RPi. The only USB port that is accessible from inside the case is the USB-C port which is typically used for power, however this port can be used as a normal USB port and the RPi can be powered via the pin header. For the FLIRC IR receiver, a USB-A socket to USB-C plug adapter is used on the USB-C port coupled with a panel mount USB-A extension cable to connect to the IR receiver at the front of the case. For power, a [5.5 mm x 2.1 mm jack](https://www.digikey.com/en/products/detail/mpd-memory-protection-devices/EJ501A/2439531) is located in the rear of the case, it is recommended to solder at least 20 awg wire with pin connectors at the end to the jack, using preferably two 5 V and two ground wires. This is the only part of the project that requires soldering. If soldering is not possible, a 5.5 mm x 2.1 mm jack with prefabbed wiring and crimp prefabbed 20 awg 0.1” header wiring on the ends can be purchased but this may require changing the diameter of the power jack hole.

For a power supply, a standard [RPi4 (15 W)](https://www.raspberrypi.com/products/type-c-power-supply/) or [RPi5 (27 W)](https://www.raspberrypi.com/products/27w-power-supply/) power supply with a USB-C to 5.5 mm adapter or another 5V power supply with the appropriate 5.5 mm jack can be used. The power supply should be capable of supplying at least 3 A. The standard RPi power supplies are recommended as they output slightly more than 5 V which helps with voltage sag.

#### 10 mm front panel - single sided machining - 50€ add-on

This option machines a 10 mm aluminum panel from the back side only. The screen is set half way through the panel thickness and there is a through hole for the FLIRC IR receiver. Mounting holes for the screen and IR receiver are tapped for M2.5 screws so there are no exposed fasteners. Pictures of this panel are shown below. Overall this option looks very nice, however due to the thickness of the front panel the top of the display text can be obstructed from view if sitting very near to the case and looking down on the screen. 

Recommended hardware:
- display mounting screws: [M2.5 x 3 mm long](https://www.mcmaster.com/91292A035/)
- FLIRC mounting screws: [M2.5 x 16 mm long](https://www.mcmaster.com/91292A018/) w/ [8 mm spacers](https://www.mcmaster.com/94669A102/)
- USB-C male to USB-A female: [Adafruit USB A Socket to USB Type C Plug Adapter](https://www.adafruit.com/product/5030)
- USB panel extension: [Adafruit Panel Mount USB Cable - A Male to A Female](https://www.adafruit.com/product/908)

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/frontpanel_front.jpeg" alt="frontpanel_front" width="600"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/frontpanel_rear.jpeg" alt="frontpanel_rear" width="600"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/case_interior.jpeg" alt="case_interior" width="600"/>

#### 10 mm front panel - double sided machining - 70€ add-on

This is the same as the first option but has a 45 deg chamfer around the screen opening to improve viewing angles. This option requires machining on both sides of the panel and is more expensive.

Recommended hardware: 
- same as single sided 10 mm front panel

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/frontpanel_front_chamfer.jpeg" alt="frontpanel_front_chamfer" width="600"/>

#### 3 mm front panel - 31€ add-on

This option uses all through holes to reduce machining cost. As this panel is not default for the case, a separate 3 mm front panel must be purchased. This design has a lot of exposed fasteners due to the through holes but has good viewing angle due to the thinner panel. The IR receiver holes are slightly larger than the display holes so that they can accept M3 screws which match the threading of the Adafruit USB panel extension cable, alternatively you can use M2.5 screw with nuts to keep the hardware consistent.

Recommended hardware:
- display mounting screws: [M2.5 x 12 mm long](https://www.mcmaster.com/92290A062/)
- FLIRC mounting screws: [M2.5 x 30 mm long](https://www.mcmaster.com/91292A037/) w/ [15 mm spacers](https://www.mcmaster.com/94669A308/)
- nuts: [M2.5](https://www.mcmaster.com/94150a310/)
- USB-C male to USB-A female: [Adafruit USB A Socket to USB Type C Plug Adapter](https://www.adafruit.com/product/5030)
- USB panel extension: [Adafruit Panel Mount USB Cable - A Male to A Female](https://www.adafruit.com/product/908)

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/frontpanel_front_thin.jpeg" alt="frontpanel_front_thin" width="600"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/case_interior_thin.jpeg" alt="case_interior_thin" width="600"/>

#### 2 mm bottom panel - 30€ add-on

This design uses a solid aluminum bottom panel which costs 5€. However, the additional 25€ machining cost for 4 RPi mounting holes is probably not worth it, as drilling 4 holes is reasonably simple.

If using the case with a RPi5 + DAC8x + OLED display, use [5 mm spacers](https://www.mcmaster.com/94669A098/) to accommodate the additional stack height.

Recommended hardware:
- RPi mounting screws: [M2.5 x 16 mm long](https://www.mcmaster.com/91292A018/) w/ [10 mm spacers](https://www.mcmaster.com/94669A104/)
- nuts: [M2.5](https://www.mcmaster.com/94150a310/) (as an alternative you can use the top part of [aluminum heatsink](https://www.amazon.com/gp/product/B07VD568FB/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) case which is tapped for M2.5 screws, this is what I used).

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/case_interior_top.jpeg" alt="case_interior_top" width="600"/>

#### 2 mm back panel - 25€ add-on

This is another area to potentially save on machining costs. For example, the back panel can be completely left off as it is in the rear and not visible. Alternatively, although it requires substantial effort, circular holes can be drilled and filled to manually create square holes. This panel has cutouts for RPi4 USB and ethernet ports. There is also an 8 mm diameter hole for a 5.5 mm barrel connector. Important to again note that the RPi5 USB / ethernet port orientation is reversed compared to the RPi4, therefore this design will NOT work with a RPi5.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/rearpanel.jpeg" alt="rearpanel" width="600"/>

As of 12/2021, prices in USD including priority shipping to Detroit, MI US for the three basic case options including front panel, bottom panel and rear panel machining are shown below.

- 3 mm front panel: $171
- 10 mm front panel, one sided machining: $189
- 10 mm front panel, double sided machining: $212
