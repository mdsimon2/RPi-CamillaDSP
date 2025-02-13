# RPi-CamillaDSP

## Introduction
Intent of this project is to provide guidance on implementing [CamillaDSP](https://github.com/HEnquist/camilladsp) on a RPi4/5. There is a lot of good information on [ASR](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/), [DIYAudio](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) and the [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp), but there also appears to be a lot of apprehension. My goal is to give concrete examples of how to use CamillaDSP with a variety of hardware to ease some of that apprehension. This tutorial originally lived at ASR, but in May 2024 I decided to migrate it to GitHub to make version management easier and provide a more universal location.

I would like to especially thank [@HEnquist](https://github.com/HEnquist) for developing CamillaDSP. I’ve long been skeptical of computer-based DSP but CamillaDSP is a game changer. It runs on minimal hardware, is easy to interface with a variety of devices and is exceptionally well designed. I’ve replaced all of my miniDSP systems with RPi4s running CamillaDSP and could not be happier.

I am not a programmer or DSP expert, my primary motivation is finding better ways to implement DIY active speakers. If you see a better way of doing something or want further explanation please speak up! These instructions have been developed as I learned how to implement CamillaDSP and found better ways to set it up, but I am always learning.

For archived versions of this tutorial that pre-date the migration to Github, see links below.

- [20-Oct-2022 Archive](https://drive.google.com/file/d/1y-vULEbXNjza7W4X1vQyIIH1r1GOCVpN/view?usp=sharing)
- [12-Dec-2023 Archive](https://drive.google.com/file/d/1MbB300dAJUEtBld14Qd4loA6hD94v67B/view?usp=share_link)
- [13-May-2024 Archive](https://drive.google.com/file/d/1SS70Ra2lkjtfXbIT7be4-WIjYCXNgC9c/view?usp=share_link)

## Background

### Why use CamillaDSP on a RPi?

This tutorial is geared towards 2 channel audio as it is somewhat difficult to get multichannel audio in to a RPi. Typical applications are DIY active speakers / subwoofers such as Directiva R1 (4+ channels), LXmini + sub(s) or LX 521.4 (8+ channels). Another good application is passive stereo speakers with 3+ subwoofers. Although it is possible to use other hardware with CamillaDSP, a RPi offers GPIO pins which are useful for [display](#oled-display) integration and has the ability to be used as a USB gadget.

### How does it work?

Starting point is a RPi4 or RPi5 running either Raspberry Pi OS Lite 64 bit. RPi4 is recommended over RPi5 due to lower cost and better thermal performance. However, RPi5 is required for multichannel I2S applications such as the HifiBerry DAC8x.

CamillaDSP will be installed such that it is always running on the RPi as a service. A web browser based GUI is available to configure CamillaDSP after initial setup.

CamillaDSP requires a capture device and playback device, the capture device is the input and playback device is the output. 

The capture device can be a variety of things, it can be the RPi itself with software audio players such as squeezelite or shairport-sync playing to an ALSA loopback, the same device as the playback device in the case of an audio interface with analog/digital inputs, or a separate device such as a TOSLINK to USB card. The main point is that CamillaDSP is NOT limited to applications that use a RPi as a source.

The playback device is either a USB DAC/DDC, HDMI output of the RPi or HAT DAC/DDC. Between the capture device and the playback device is where the magic happens, CamillaDSP can implement channel routing, IIR filters, FIR filters, volume control (with dynamic loudness), resampling and delay. The RPi is surprising powerful and is able to do much more than any miniDSP product that exists today.

### What DACs are recommended?

1) [Okto dac8 PRO](https://www.oktoresearch.com/dac8pro.htm) - €1289, 8 channel balanced analog output, 8 channel AES digital input, 2 channel AES digital output, 1RU full-rack, volume knob, IR remote control, 5 V trigger, large display, excellent analog performance and overall design. [Okto dac8 PRO ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/review-and-measurements-of-okto-dac8-8ch-dac-amp.7064/).

2) [MOTU Ultralite Mk5](https://motu.com/en-us/products/gen5/ultralite-mk5/) - $650, 10 channel balanced analog output, 8 channel balanced analog input, TOSLINK input / output (also supports ADAT), SPDIF input / output, volume knob capable of controlling all analog outputs, 1RU half-rack, overall good analog performance.  [MOTU Ultralite Mk5 ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/motu-ultralite-mk5-review-audio-interface.24777/).

3) [MOTU M4](https://motu.com/en-us/products/m-series/m4/) - $250, 4 channel unbalanced/balanced analog output, 4 channel balanced analog input, good analog performance, USB powered. Good budget option for 2.1/2.2 or 2 way active systems, I/O functionality is rather limited. [MOTU M4 ASR Review](https://www.audiosciencereview.com/forum/index.php?threads/motu-m4-audio-interface-review.15757/).

5) [HifiBerry DAC8x](https://www.hifiberry.com/shop/boards/hifiberry-dac8x/) - $65, requires a RPi5, HAT, 8 channel unbalanced analog output, good analog noise performance, acceptable distortion performance, 1/8" headphone outputs are rather flimsy. [HifiBerry DAC8x Measurements](https://www.audiosciencereview.com/forum/index.php?threads/8ch-hifiberry-hat-dac-for-rpi5.53672/post-1966410).

6) Whatever is on have on hand! Part of the beauty of a CamillaDSP / RPi setup is that it is cheap and easy try with almost any USB device. 

Although configurations are not provided for the following devices, they have been used successfully with CamillaDSP on a RPi4. In particular the MCHstreamer / USBstreamer are useful with ADAT input pro audio interfaces to achieve 8 channels of output at 44.1/48 kHz.

- [miniDSP MCHstreamer](https://www.minidsp.com/products/usb-audio-interface/mchstreamer)
- [miniDSP USBstreamer](https://www.minidsp.com/products/usb-audio-interface/usbstreamer)
- [Focusrite 18i20 2nd gen](https://www.crutchfield.com/S-8cLHKJ3PIHh/p_880SC182G2/Focusrite-Scarlett-18i20-Second-Generation.html)
- [DIYINHK multichannel XMOS](https://www.diyinhk.com/shop/audio-kits/142-xmos-multichannel-high-quality-usb-tofrom-i2sdsd-spdif-pcb.html)

Below are other good sources of information related to CamillaDSP.

- [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp) - Henrik has done a great job with the GitHub and it is an excellent reference. Almost everything presented in this tutorial can also be found there.

- [CamillaDSP DIYAudio Thread](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) - The best place to ask general CamillaDSP questions. Also a great thread to search for further information on any CamillaDSP topic.

- [RPi4 + CamillaDSP Tutorial ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/) - This tutorial originally lived in this thread. It is a good place to discuss using CamillaDSP on a RPi as well as display / remote control integrations.

- [Pi4 + CamillaDSP + MOTU M4 ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/pi4-camilladsp-audio-interface-motu-m4-phenomal-dsp-streamer.24493/) - Excellent thread by [@armigo](https://www.audiosciencereview.com/forum/index.php?members/armigo.20011/) that helped inspire this tutorial. 

- [Budget Standalone Toslink > DSP > Toslink with CamillaDSP ASR Thread](https://www.audiosciencereview.com/forum/index.php?threads/budget-standalone-toslink-dsp-toslink-with-camilladsp-set-up-instructions-for-newbies.30830/) - Great thread by [@MCH](https://www.audiosciencereview.com/forum/index.php?members/mch.30254/) showing how to make a low cost (< 50€) TOSLINK input / output stereo room correction DSP using CamillaDSP.

- [Using a Raspberry Pi as equaliser in between an USB Source and USB DAC](https://www.audiosciencereview.com/forum/index.php?threads/using-a-raspberry-pi-as-equaliser-in-between-an-usb-source-ipad-and-usb-dac.25414/page-3#post-1180356) - Great thread from [@DeLub](https://www.audiosciencereview.com/forum/index.php?members/delub.16965/) on how to use a RPi as a USB gadget.

## CamillaDSP Setup

This part describes how to get a working CamillaDSP setup. For reference, a complete install should take less than 30 minutes (including [OLED display](#oled-display) and [FLIRC IR receiver](#flirc-usb-ir-receiver) setup), most of that time is waiting for things to download / install.

### 1) Write OS to micro SD card

Download and install Raspberry Pi Imager from the links below for Raspberry Pi OS Lite 64 bit Bookworm.

- [Raspberry Pi Imager for Ubuntu](https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb)
- [Raspberry Pi Imager for Windows](https://downloads.raspberrypi.org/imager/imager_latest.exe)
- [Raspberry Pi Imager for macOS](https://downloads.raspberrypi.org/imager/imager_latest.dmg)

Open Raspberry Pi Imager, select the desired RPi, OS and micro SD card. When done, click Next.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/rpi_imager.png" alt="rpi_imager" width="300"/>

When prompted, click Edit Settings.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/rpi_imager_2.png" alt="rpi_imager_2" width="300"/>

Under General tab, set hostname, username, password and wifi settings. When done, click Services tab.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/rpi_imager_3.png" alt="rpi_imager_3" width="300"/>

Under Services tab, enable SSH and password authentication. When done, click Save.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/rpi_imager_4.png" alt="rpi_imager_4" width="300"/>

Click Yes to write OS to micro SD card.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/rpi_imager_5.png" alt="rpi_imager_5" width="300"/>

When done writing, insert micro SD card into RPi and connect power supply.

This install assumes the RPi will be managed remotely via SSH from a separate computer. With Mac or Linux, terminal will installed by default and commands in subsequent steps of this tutorial can be run in terminal without issue.

With Windows 10 or 11 it is recommended to install Windows Subsystem for Linux (WSL). Instruction below are condensed version of this -> https://docs.microsoft.com/en-us/windows/wsl/install.

Open PowerShell as administrator as shown below.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/powershell.png" alt="powershell" width="300"/>

Run wsl --install in PowerShell and restart.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/wsl_install.png" alt="wsl_install" width="500"/>

Following the restart Ubuntu can be used for terminal access.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/Ubuntu.png" alt="Ubuntu" width="500"/>

### 2) Log in to RPi and update / upgrade

Wait a minute or two for RPi to start for the first time, then open terminal and log in to RPi using your username and hostname. 

```
ssh username@hostname
```

Update / upgrade RPi.

```
sudo apt update
sudo apt full-upgrade
```

Say yes to any upgrade prompts. If prompted about restarting services, hit enter.

### 3) Install CamillaDSP

Make a camilladsp folder, as well as folders for CamillaDSP to reference stored FIR filters and configurations. Download and unpack CamillaDSP binary. The commands below will install V3.0.0 in /usr/local/bin/.

```
mkdir ~/camilladsp ~/camilladsp/coeffs ~/camilladsp/configs
wget https://github.com/HEnquist/camilladsp/releases/download/v3.0.0/camilladsp-linux-aarch64.tar.gz -O ~/camilladsp/camilladsp-linux-aarch64.tar.gz
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/
```

### 4) Install CamillaDSP service

```
sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/camilladsp.service -O /lib/systemd/system/camilladsp.service
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

### 5) Install GUI

Download and extract GUI bundle.

```
wget https://github.com/HEnquist/camillagui-backend/releases/download/v3.0.1/bundle_linux_aarch64.tar.gz -O ~/camilladsp/bundle_linux_aarch64.tar.gz
tar -xvf ~/camilladsp/bundle_linux_aarch64.tar.gz
```

### 6) Install GUI service

```
sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/camillagui.service -O /lib/systemd/system/camillagui.service
```

Open GUI service in nano and update username and ExecStart to reflect your username.

```
sudo nano /lib/systemd/system/camillagui.service
```

Enable and start camillagui service.

```
sudo systemctl enable camillagui
sudo service camillagui start
```

### 7) Enable ALSA loopback (optional)

This step is only required for [streamer applications](#streamer-applications) using an ALSA loopback.

Create snd-aloop.conf.

```
echo 'snd-aloop' | sudo tee -a /etc/modules-load.d/snd-aloop.conf > /dev/null
```

Restart RPi for the change to take effect.

```
sudo reboot now
```

### 8) Enable USB gadget (optional)

The RPi4/5 can be used as USB input / output device, this is known as a USB gadget. This step is only required for configurations using the USB gadget as capture device.

Update config.txt to include dtoverlay=dwc2, add dwc2 and g_audio to /etc/modules and create usb_g_audio.conf with desired parameters.

```
echo 'dtoverlay=dwc2' | sudo tee -a /boot/firmware/config.txt > /dev/null
echo -e 'dwc2\ng_audio' | sudo tee -a /etc/modules > /dev/null
echo 'options g_audio c_srate=44100 c_ssize=4 c_chmask=3 p_chmask=0' | sudo tee -a /etc/modprobe.d/usb_g_audio.conf > /dev/null 
```
"c_srate" sets the capture rates that will be offered to the USB host. To add rates use commas, for example, c_srate=44100,48000,88200,96000. It is important to note the USB host must be set to the same rate as the CamillaDSP capture rate, this is why the above command only gives the 44100 Hz option. There are tools that can automatically switch the CamillaDSP capture rate such as [gaudio_ctl](https://github.com/pavhofman/gaudio_ctl) and [camilladsp-setrate](https://github.com/marcoevang/camilladsp-setrate) but they are outside the scope of this tutorial.

"c_ssize" sets the capture rate format offered to the USB host. 4 = S32_LE.

"c_chmask" sets the number of capture channels. Format is 2^(number of channels) - 1. Therefore, 3 = 2 channels, 63 = 6 channels and 255 = 8 channels.

"p_chmask" sets the number of playback channels offered to the RPi. This is set to 0 as as the gadget is typically only used as a capture device.

Restart RPi for the change to take effect.

```
sudo reboot now
```

If using the RPi as a USB gadget, connect the RPi to the USB host via the USB-C port. By default, this will power the RPi from the USB host. Purchase a [USB-C power/data splitter](https://www.tindie.com/products/8086net/usb-cpwr-splitter/) to power the RPi from a separate power supply.

### 9) Assign active configuration in GUI

Configurations are explained in more detail in the [CamillaDSP Configurations](#camilladsp-configurations) section of this tutorial. Pre-made configurations for the DACs in this tutorial can be downloaded by navigating to the [configs](https://github.com/mdsimon2/RPi-CamillaDSP/tree/main/configs) folder. Alternatively, download the entire repository by clicking [here](https://github.com/mdsimon2/RPi-CamillaDSP/archive/refs/heads/main.zip) or using git clone.

On a computer that is on the same network as the RPi, navigate browser to http://hostname:5005.

Navigate to Files tab of GUI and upload desired configuration using the up arrow in the Configs section. Set this configuration as active by pressing the "star" next to the configuration. From now on CamillaDSP and the GUI will start with this configuration loaded. Click the "Apply and Save" button in the lower left to load the configuration to DSP.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/files.png" alt="files" width="600"/>

Congratulations, CamillaDSP is now up and running!

### 10) Upgrading to future versions

To upgrade to a new version of CamillaDSP, simply download and extract the new binary.
```
wget https://github.com/HEnquist/camilladsp/releases/download/v3.0.0/camilladsp-linux-aarch64.tar.gz -O ~/camilladsp-linux-aarch.tar.gz
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/
sudo service camilladsp restart
```

Upgrading the GUI is a similar process. If you are upgrading from a GUI prior to V3.0.1, please install a new [GUI service](#6-install-gui-service).

```
wget https://github.com/HEnquist/camillagui-backend/releases/download/v3.0.1/bundle_linux_aarch64.tar.gz -O ~/camilladsp/bundle_linux_aarch64.tar.gz
tar -xvf ~/camilladsp/bundle_linux_aarch64.tar.gz
sudo service camilladsp restart
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

Like shairport-sync, a few changes are required to the squeezelite configuration. 

```
echo -e 'SL_SOUNDCARD="hw:Loopback,1"\nSB_EXTRA_ARGS="-W -C 5 -r 44100-44100 -R hLE:::28"' | sudo tee -a /etc/default/squeezelite > /dev/null
```

Restart squeezelite service to reflect changes.

```
sudo service squeezelite restart
```

These changes set ALSA loopback device 1 as squeezelite playback device, resample all files to 44.1 kHz using a high quality resampling algorithm and stop squeezelite after 5 seconds of inactivity.

## CamillaDSP Configurations

All configurations use maximum amount of output channels for a given playback device. Bass and Treble filters are provided on input channels, see [Compact View](#compact-view) for more information. If an output channel is not needed remove it from the mixer as each extra channel requires additional processing resources. Configuration files can be found in the [configs](https://github.com/mdsimon2/RPi-CamillaDSP/tree/main/configs) folder.

The naming convention configuration files in this tutorial is dac_input_capturerate_playbackrate. For example, a configuration for a MOTU Ultralite Mk5, TOSLINK input with 96 kHz capture and 96 kHz playback rates is [ultralitemk5_toslink_96c_96p.yml](https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/configs/ultralitemk5/ultralitemk5_toslink_96c_96p.yml). All configurations are intended for use with CamillaDSP V3.

### Converting Configurations from V2 to V3

CamillaDSP V3 uses different nomenclature than V2, therefore if you have an existing V2 configuration file that you would like to use in V3 it needs to be converted. 

Go to the Files tab of the GUI and click New blank configuration to apply a blank configuration in the GUI. Next click Import config and select CamillaDSP Config. Select your V2 configuration and click the box next to the configuration name and scroll to the bottom and select import, this loads the configuration to the GUI. You should see message saying the import was successful. 

Review the configuration and make any changes needed, I've noticed that resampling appears to be applied to configurations where it was not previously. To save the configuration, enter a configuration name where it says New config.yml and click the adjacent disk. After this the configuration should show as valid and list version as 3.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/v3_import_7.png" alt="v3_import_7" width="500"/>

### ASRC Options
CamillaDSP expects a constant capture sample rate and cannot accommodate rate changes without a restart. For variable sample rate physical digital sources like TOSLINK, AES or SPDIF or multiple physical digital sources with different rates, a good option is to add a device that has an ASRC to convert to a consistent rate. miniDSP offer many devices with this capability which are summarized below.

- [nanoDIGI](https://www.minidsp.com/images/documents/nanoDIGI%202x8%20User%20Manual.pdf) - $170, discontinued in 2021 but possible to find used, SPDIF / TOSLINK input, SPDIF output, 96 kHz
- [2x4HD](https://www.minidsp.com/products/minidsp-in-a-box/minidsp-2x4-hd) - $225, TOSLINK / analog input, USB output, 96 kHz
- [miniDSP OpenDRC-DI](https://www.minidsp.com/products/opendrc-series/opendrc-di) - $325, AES / SPDIF / TOSLINK input and output, 48 or 96 kHz
- [Flex Digital](https://www.minidsp.com/products/minidsp-in-a-box/flex) - $495, SPDIF / TOSLINK / USB / analog / bluetooth input, SPDIF / TOSLINK / USB output, 96 kHz
- [Flex Analog](https://www.minidsp.com/products/minidsp-in-a-box/flex) $495-470, SPDIF / TOSLINK / analog / bluetooth input, USB Output, 96 kHz
- [SHD Studio](https://www.minidsp.com/products/streaming-hd-series/shd-studio) - $900, AES / SPDIF / TOSLINK / USB / streamer input, SPDIF / AES / USB output, 96 kHz
- [SHD](https://www.minidsp.com/products/streaming-hd-series/shd) - $1250, AES / SPDIF / TOSLINK / USB / streamer / analog input, SPDIF / AES / USB output, 96 kHz

These devices can do IR volume control, although not all have displays for volume / input identification.

2x4HD and Flex can be upgraded to Dirac versions but sample rate will change from 96 kHz to 48 kHz.

In order to use USB output of devices like 2x4HD, Flex and SHD they need to be set as capture device in CamillaDSP. Unfortunately this ties up the USB input and makes it unusable. Still, this is a good approach to add extra input functionality to basic USB DACs like the MOTU M4 or Topping DM7 which only have USB input. [minidsp-rs](https://github.com/mrene/minidsp-rs) can be used to manage miniDSPs connected to a RPi but is beyond the scope of this tutorial.

For constant sample rate digital sources the following devices work well. Compared to other solutions like the HiFiBerry Digi+ I/O they handle signal interruptions gracefully. These devices are used in a similar way to the miniDSPs with USB outputs, the device is set as the CamillaDSP capture device. Note, that although the S2 digi also has a TOSLINK output, it is not recommended due to audible dropouts.

- [hifime S2 digi (SA9227)](https://hifimediy.com/product/s2-digi/) - $40, TOSLINK input, USB output, sample rates up to 192 kHz
- [hifime UR23](https://hifimediy.com/product/hifime-ur23-spdif-optical-to-usb-converter/) - $25, TOSLINK input, USB output, does NOT work with RPi5, sample rates up to 96 kHz

### chunksize / target_level

CamillaDSP V1 used a buffer size of 2 x chunksize, CamillaDSP V2 and V3 use a buffer size of 4 x chunksize. In previous versions of this tutorial a rather long chunksize was specified (44.1/48 = 1024, 88.2/96 = 2048, 176.4/192 = 4096) resulting in long latency. After some experimentation, it was found that much lower chunksizes are stable when using physical input (SPDIF, TOSLINK, analog, etc) capture devices.

All physical input capture device configurations now use the following chunksize depending on playback sample rate.

- 44.1 / 48 kHz: 64
- 88.2 / 96 kHz: 128
- 176.4 / 192 kHz: 256

All ALSA Loopback / USB gadget capture device configurations now use the following chunksize depending on playback sample rate.

- 44.1 / 48 kHz: 256
- 88.2 / 96 kHz: 512
- 176.4 / 192 kHz: 1024

All configurations use target level of 3X chunk size.

For physical input capture device configurations latency is ~10 ms, for ALSA Loopback / USB gadget capture device configurations latency is ~20 ms.

If dropouts are experienced, try doubling chunksize / target_level, and please let me know.

### Okto dac8 PRO

These configurations assume CamillaDSP volume control is NOT being used as the Okto has a nice display with volume knob and IR control. As volume control is downstream of CamillaDSP, digital clipping in CamillaDSP is more of an issue. As a result, 1 dB attenuation has been added to all output channels of configurations that implement resampling to help avoid clipping. In general, if boost is added to a configuration, offset that boost by attenuating the output further. Use the CamillaDSP clipping indicator to gauge if there is enough attenuation to avoid digital clipping.

#### okto_streamer.yml

- Set Okto to Pure USB mode via front panel.
- All streamer configurations expect 44.1 kHz input. 
- Due to clock difference between loopback and Okto, rate adjust is enabled.
- Configurations provided for 44.1, 96 and 192 kHz playback sample rates.

#### okto_gadget.yml

- Set Okto to Pure USB mode via front panel.
- All gadget configurations expect 44.1 kHz input to match usb_g_audio.conf.
- Due to clock difference between RPi and Okto, rate adjust is enabled.
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

Paste the text below to the end of nginx.conf, update the IP address shown on the front panel of the Ultralite Mk5 followed by :1280.

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

Ultralite Mk5 should automatically connect to the network if using Raspberry Pi OS.

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

Once channel routing is set in Cuemix, this DAC is very similar to the Okto in terms of setup, just with more inputs / output options. Although the Ultralite Mk5 has a volume knob, it does not have an IR receiver, therefore it is advantageous to use CamillaDSP for volume control. See [FLIRC IR Receiver](#flirc-usb-ir-receiver) and [OLED Display](https://github.com/mdsimon2/RPi-CamillaDSP#oled-display) sections of this tutorial for more information.

#### ultralitemk5_streamer.yml

- Set clock source to internal via Ultralite Mk5 front panel. 
- All streamer configurations expect 44.1 kHz input. 
- Due to clock difference between loopback and Ultralite Mk5, rate adjust is enabled.
- Configurations provided for 44.1, 96 and 192 kHz playback sample rates.

#### ultralitemk5_gadget.yml

- Set clock source to internal via Ultralite Mk5 front panel. 
- All gadget configurations expect 44.1 kHz input to match usb_g_audio.conf.
- Due to clock difference between RPi and Ultralite Mk5, rate adjust is enabled.
- Configurations provided for 44.1, 96 and 192 kHz playback sample rates.

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
- This configuration uses analog inputs 3-4 but others can be used as needed.
- It is not possible to use different input and output sample rates when using Ultralite Mk5 as capture device.
- Configurations provided for 48, 96 and 192 kHz sample rates.

### MOTU M4

Given lack of 4 channel on device volume control, it is recommended to use CamillaDSP volume control with this DAC. Due to limited input functionality, a variety of configurations with external input devices are provided, similar configurations can be used with any DAC in this tutorial.

#### m4_streamer.yml

- All streamer configurations expect 44.1 kHz input. 
- Due to clock difference between loopback and M4, rate adjust is enabled. 
- Configurations provided for 44.1, 96 and 192 kHz playback sample rates.

#### m4_gadget.yml

- All gadget configurations expect 44.1 kHz input to match usb_g_audio.conf.
- Due to clock difference between RPi and M4, rate adjust is enabled. 
- Configurations provided for 44.1, 96 and 192 kHz playback sample rates.

#### m4_analog.yml

- This configuration uses analog inputs 3-4 but others can be used as needed.
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

This is the only HAT option in this tutorial. As it uses multichannel I2S output, it must be used with a RPi5. Due to lack of volume control, it is recommended to use CamillaDSP volume control with this DAC.

Add dtoverlay=hifiberry-dac8x to config.txt.

```
echo 'dtoverlay=hifiberry-dac8x' | sudo tee -a /boot/firmware/config.txt > /dev/null
```

After a RPi reboot, it should be recognized.

#### dac8x_streamer.yml

- All streamer configurations expect 44.1 kHz input. 
- Due to clock difference between loopback and DAC8x, rate adjust is enabled. 
- Configurations provided for 44.1, 96 and 192 kHz playback sample rates.

#### dac8x_gadget.yml

- All gadget configurations expect 44.1 kHz input to match usb_g_audio.conf.
- Due to clock difference between RPi and DAC8x, rate adjust is enabled. 
- Configurations provided for 44.1, 96 and 192 kHz playback sample rates.

#### dac8x_2x4hd.yml

- This configuration uses a miniDSP 2x4HD as capture device. 
- Due to clock difference between loopback and DAC8x, rate adjust and asynchronous resampling are enabled.
- Capture sample rate set to 96 kHz to match miniDSP 2x4HD sample rate. 
- Configuration provided for 96 kHz playback sample rate, but can be changed to any rate supported by DAC8x.

#### dac8x_sa9227.yml

- This configuration uses a hifime S2 digi (SA9227) as capture device. 
- Due to clock difference between S2 digi and DAC8x, rate adjust and asynchronous resampling are enabled. 
- Configuration provided for 44.1 and 192 kHz capture sample rate, but can be changed to match the source.
- Playback sample rate set to device maximum of 192 kHz.

## Advanced Configuration

### GUI

Access the GUI via any computer on the same network as the RPi by navigating a browser to http://hostname:5005.

#### Title

There isn't much to do in this tab, but the title and description fields can be populated. The title field is displayed on the first line of the [OLED display](#oled-display) described later in this tutorial.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/title.png" alt="title" width="600"/>

#### Devices

The Devices tab defines general parameters like capture device, playback device, sample rate, rate adjust, resampling and chunk size.

It is very important that sample format and channel count are supported by the device. If using configurations from this tutorial this will not be an issue, but if creating new configurations it is something to be aware of. 

With V3 there are now labels that can be applied to capture device channels, if a list of labels is provided they will appear in the Mixers and Pipeline tabs, as well as level meters.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/devices.png" alt="devices" width="600"/>

#### Filters

In the Filters tab a variety of filters can be created. A big advantage of using the GUI over a manual configuration file is that it will prompt for the necessary information for a given filter type. Once a filter is created, magnitude / phase / group delay can be viewed. For questions about specific filter implementation, see the [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp). Creating a filter in the Filters tab does not apply it to the pipeline, it just creates a filter that will be available to apply in the pipeline.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/filters.png" alt="filters" width="600"/>

#### Mixers

The Mixers tab defines channel routing, in addition, gain and polarity can be defined for each channel. Like filters, mixers will not be in effect until applied in the pipeline.

As in the Devices tab, it is very important that mixer channel counts exactly match the channel counts of the device. For configurations from this tutorial this will not be an issue. It is not required to use all channels in the mixer, but the correct channel counts need to specified in the "in" and "out" section. For example in the screenshot below 8 input and 8 output channels are specified although only 2 input channels (0 and 1) are used in the mixer definition.

With V3 there are now labels that can be applied to playback device channels, if a list of labels is provided they will appear in the Mixers and Pipeline tabs, as well as level meters.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/mixers.png" alt="mixers" width="600"/>

#### Processors

I haven't used this personally, but it can be used to implement a compressor.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/processors.png" alt="processors" width="600"/>

#### Pipeline

The Pipeline tab is where everything comes together. Filters, mixers and processors created in the previous tabs are applied here. The entire pipeline can be plotted to show how the mixer and filters are applied as well as the combined magnitude / phase / group delay on each channel.

With V3 filter steps can now be applied to multiple channels, eliminating the need to repeat filter steps for left / right channels as an example.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/pipeline1.png" alt="pipeline1" width="800"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/pipeline2.png" alt="pipeline2" width="800"/>

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/pipelinemap.png" alt="pipeline_map" width="800"/>

#### Files

The Files tab stores configurations and convolution filters. It will show configuration files located in ~/camilladsp/configs/ and convolution filters located in ~/camilladsp/coeffs/. Configurations and convolution filters can be downloaded / uploaded to/from via this tab. 

To load a configuration in the GUI, press the clockwise arrow button next to the desired configuration. Once this is done, the configuration name appear in the lower left under "Config", in the screenshot below, a configuration called lxminibsc.yml is loaded in the GUI.

Just because a configuration is loaded in the GUI does NOT mean it is actually applied to the DSP. To apply a configuration to the DSP, click the "Apply to DSP" button. This will apply the configuration in the GUI to the DSP but it will NOT save any changes made via the GUI. To save changes, click the "Save to File" button. To implement both of these operations at the same time, click the "Apply and save" button. Alternatively, use the "Apply automatically" and "Save automatically" check boxes to do these operations automatically after a change is made in the GUI.

To see what settings are currently applied to the DSP, click the "Fetch from DSP" button and to load the GUI with the current DSP settings. Note, it only pulls the settings and does NOT change the configuration name in the lower left.

In order to set a configuration as default (i.e. the configuration that will be loaded when CamillaDSP starts), click the star button next to the desired configuration. After this is done, the star button will now be green next to the default configuration.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/files.png" alt="files" width="600"/>

#### Compact View

The Compact View is great for changing volume or configurations from a smartphone or tablet. It can be accessed by clicking the "Change to compact view" button just to the right of the CamillaDSP logo.

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

Install python virtual environment and pycamilladsp. Installing pycamilladsp in a virtual environment is a change with V3 and requires an update to flirc.service if upgrading from an older version.

```
sudo apt install git python3-dev python3-aiohttp
python -m venv --system-site-packages ~/camilladsp/.venv
source ~/camilladsp/.venv/bin/activate
pip3 install git+https://github.com/HEnquist/pycamilladsp.git
deactivate
```

Install evdev and flirc.py. If upgrading from V2 to V3, re-run the step below as pycamilladsp is now installed in a virtual environment and nomenclature has changed.

```
sudo apt install python3-evdev
wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/flirc.py -O ~/flirc.py
```

Enable USB-C port for use, this is needed to run the IR receiver from the USB-C port as is implemented in the [Modushop Case](#modushop-case) design in this tutorial . If the FLIRC is plugged in to a USB-A port this step is not required.

```
echo 'dtoverlay=dwc2,dr_mode=host' | sudo tee -a /boot/firmware/config.txt > /dev/null
```

After rebooting, check that the FLIRC is recognized.

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

Install FLIRC service. If upgrading from V2 to V3, download a new version of flirc.service as pycamilladsp is now installed in a virtual environment.

```
sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/flirc.service -O /lib/systemd/system/flirc.service
```

Open FLIRC service in nano and update username and ExecStart to reflect your username.

```
sudo nano /lib/systemd/system/flirc.service
```

Enable and start FLIRC service.

```
sudo systemctl enable flirc
sudo service flirc start
```

### Trigger Output

It is easy to add a trigger output to the Ultralite Mk5 using a [Bobwire DAT1](https://www.bobwireaudio.com/). Simply connect the TOSLINK output of the Ultralite Mk5 to the Bobwire DAT1 and use the Audio Detect output port. All configuration files in this tutorial are set to stop after 5 seconds of output less than -100 dB, as a result CamillaDSP will stop after 5 seconds and after 60 seconds the trigger from the Bobwire DAT1 will turn any connected amplifiers off. Once CamillaDSP starts playing, the Bobwire DAT1 trigger will activate.

### OLED Display

RPis have GPIO pins which can be used to interface with a variety of displays. A python script has been developed for the [buydisplay.com 3.2” diagonal SSD1322 OLED display](https://www.buydisplay.com/white-3-2-inch-arduino-raspberry-pi-oled-display-module-256x64-spi) which is ~$30 + shipping. Be sure to order the display in the 6800 8 bit configuration. It is recommended to have them solder a pin header as it is only an additional cost of $0.59.

The base setup turns the display off after 10 seconds of no volume changes to avoid OLED burn in. It will turn back on if the volume, status or configuration are changed. 

Previous versions of this tutorial offered python routines based on lgpio and rpi-gpio. However, going forward only the lgpio routine will be provided. Updates to the lgpio routine implementing group pin writing have significantly improved performance and using Raspberry Pi OS instead of Ubuntu Server improves performance even further. In addition, the RPi5 does not support rpi-gpio.

Install python virtual environment and pycamilladsp. Note, you may have already completed this step in the (FLIRC USB IR Receiver)[#flirc-usb-ir-receiver) section. Installing pycamilladsp in a virtual environment is a change with V3 and requires an update to oled.service if upgrading from an older version.

```
sudo apt install git python3-dev python3-aiohttp
python -m venv --system-site-packages ~/camilladsp/.venv
source ~/camilladsp/.venv/bin/activate
pip3 install git+https://github.com/HEnquist/pycamilladsp.git
deactivate
```

Install oled.py. If upgrading from V2 to V3, re-run the step below as pycamilladsp is now installed in a virtual environment and nomenclature has changed.

```
wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/oled.py -O ~/oled.py
```

Install OLED service. If upgrading from V2 to V3, download a new version of oled.service as pycamilladsp is now installed in a virtual environment.

```
sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/oled.service -O /lib/systemd/system/oled.service
```

Open OLED service in nano and update username and ExecStart to reflect your username.

```
sudo nano /lib/systemd/system/oled.service
```

Enable and start OLED service.

```
sudo systemctl enable oled
sudo service oled start
```

The python script has the ability to show user defined text on the first line of the display based on loaded configuration file. With CamillaDSP V2, this will show the title field under the Title tab of the GUI. If this field is blank, "CamillaDSP" will be displayed.

Wiring configuration from the display to the RPi GPIO header is listed below. Note, these pins can be changed as desired, see here for more information on RPi pinout -> https://www.tomshardware.com/reviews/raspberry-pi-gpio-pinout,6122.html. Please note the wiring configuration has been changed from earlier versions of this tutorial to accommodate the HifiBerry DAC8x, the old pin configurations are shown in parenthesis for the pins that have changed.

1) (ground) -> ground
2) (supply voltage) -> 3.3 V
3) (no connection) -> no connection
4) (data bus 0) -> GPIO 15 (GPIO 26)
5) (data bus 1) -> GPIO 13
6) (data bus 2) -> GPIO 6
7) (data bus 3) -> GPIO 5
8) (data bus 4) -> GPIO 9 (GPIO 22)
9) (data bus 5) -> GPIO 2 (GPIO 27)
10) (data bus 6) -> GPIO 17
11) (data bus 7) -> GPIO 3 (GPIO 18)
12) (enable) -> GPIO 14 (GPIO 23)
13) (read/write) -> ground
14) (data/command) -> GPIO 16
15) (reset) -> GPIO 12
16) (chip select)-> GPIO 10 (GPIO 25)

For wiring, prefabbed 8” long 0.1” header jumpers are recommended. These are a bit long but allow the removal the front panel with the wiring remaining connected.

### Modushop Case

[Modushop](https://modushop.biz/site/) offers CNC machining of aluminum cases for custom projects. Depending on exchange rates and shipping costs, ordering directly from Modushop may be slightly cheaper than ordering from [DIYAudio Store](https://diyaudiostore.com) which is the US distributor. All cases are based on the Galaxy GX247 chassis (230 mm x 170 mm x 40 mm) with 2 mm aluminum covers.

Case designs discussed below are intended for use with an [OLED Display](#oled-display), [FLIRC IR Receiver](#flirc-usb-ir-receiver) and RPi4. A RPi5 can be used but the back panel will not work as the USB/ethernet orientation has been reversed compared to the RPi4. If using a RPi5, either modify the rear panel drawing or leave the back panel off. Drawings in dwg, pdf and vsdx format can be found in the [case_drawings](https://github.com/mdsimon2/RPi-CamillaDSP/tree/main/case_drawings) folder.

All USB-A ports are located on the rear of the RPi. The only USB port that is accessible from inside the case is the USB-C port which is typically used for power, however this port can be used as a normal USB port and the RPi can be powered via the pin header. For the FLIRC IR receiver, a USB-A socket to USB-C plug adapter is used on the USB-C port coupled with a panel mount USB-A extension cable to connect to the IR receiver at the front of the case. For power, a [5.5 mm x 2.1 mm jack](https://www.digikey.com/en/products/detail/mpd-memory-protection-devices/EJ501A/2439531) is located in the rear of the case, it is recommended to solder at least 20 awg wire with pin connectors at the end to the jack, using preferably two 5 V and two ground wires. This is the only part of the project that requires soldering. If soldering is not possible, a 5.5 mm x 2.1 mm jack with prefabbed wiring and crimp prefabbed 20 awg 0.1” header wiring on the ends can be purchased but this may require changing the diameter of the power jack hole.

For a power supply, a standard [RPi4 (15 W)](https://www.raspberrypi.com/products/type-c-power-supply/) with a USB-C to 5.5 mm adapter or another 5V power supply with the appropriate 5.5 mm jack can be used. The power supply should be capable of supplying at least 3 A. The standard RPi power supply is recommended as they output slightly more than 5 V which helps with voltage sag. DO NOT USE a standard [RPi5 (27 W)](https://www.raspberrypi.com/products/27w-power-supply/) power supply with a USB-C to 5.5 mm adapter as it will output 15 V and destroy the RPi. In all cases, verify 5 V from the power supply with a multimeter prior to applying to the pin header.

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

This option uses all through holes to reduce machining cost. As this panel is not default for the case, a separate 3 mm front panel must be purchased. This design has a lot of exposed fasteners due to the through holes but has good viewing angle due to the thinner panel. The IR receiver holes are slightly larger than the display holes so that they can accept M3 screws which match the threading of the Adafruit USB panel extension cable, alternatively M2.5 screw with nuts can be used to keep the hardware consistent.

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
- nuts: [M2.5](https://www.mcmaster.com/94150a310/) (as an alternative use the top part of an [aluminum heatsink](https://www.amazon.com/gp/product/B07VD568FB/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) case tapped for M2.5 screws).

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/case_interior_top.jpeg" alt="case_interior_top" width="600"/>

#### 2 mm back panel - 25€ add-on

This is another area to potentially save on machining costs. For example, the back panel can be completely left off as it is in the rear and not visible. Alternatively, although it requires substantial effort, circular holes can be drilled and filled to manually create square holes. This panel has cutouts for RPi4 USB and ethernet ports. There is also an 8 mm diameter hole for a 5.5 mm barrel connector. Important to again note that the RPi5 USB / ethernet port orientation is reversed compared to the RPi4, therefore this design will NOT work with a RPi5.

<img src="https://github.com/mdsimon2/RPi-CamillaDSP/blob/main/screenshots/rearpanel.jpeg" alt="rearpanel" width="600"/>

As of 12/2021, prices in USD including priority shipping to Detroit, MI US for the three basic case options including front panel, bottom panel and rear panel machining are shown below.

- 3 mm front panel: $171
- 10 mm front panel, one sided machining: $189
- 10 mm front panel, double sided machining: $212
