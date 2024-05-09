# RPi-CamillaDSP

## Introduction
Intent of this project is to provide guidance for setting up [CamillaDSP](https://github.com/HEnquist/camilladsp) on a RPi4/5. There is a lot of good information scattered through [ASR](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/), [DIYAudio](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) and the [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp) but there also appears to be a lot of apprehension. My goal is to give concrete examples of how to use CamillaDSP with a variety of hardware to ease some of that apprehension. This tutorial originally lived at ASR but in May 2024 I decided to migrate it to GitHub to make version management easier and provide a more universal location.

I realize this tutorial is long and looks daunting. I felt the same way when trying to figure this stuff out. My advice is to take it step by step, go slowly and ask questions. Some DIY projects are not worth the effort but this one is. At the end of this project you will have a DSP with almost unparalleled processing power in a very small form factor, easily configured via web interface, all at a very low cost compared to commercial options.

I would like to especially thank @HenrikEnquist for developing CamillaDSP. I’ve long been skeptical of computer-based DSP but CamillaDSP is a game changer. It runs on minimal hardware, is easy to interface with a variety of devices and is exceptionally well designed. I’ve replaced all of my miniDSP systems with RPi4s running CamillaDSP and could not be happier.

I am not a programmer or DSP expert, my primary motivation is finding better ways to implement DIY active speakers. If you see a better way of doing something or want further explanation please speak up! These instructions have been developed as I learned how to implement CamillaDSP and found better ways to set it up but I am always learning.

Prior to GitHub, I archived older versions of the tutorial at the links below.

- [10/20/2022 Archive](https://drive.google.com/file/d/1y-vULEbXNjza7W4X1vQyIIH1r1GOCVpN/view?usp=sharing)
- [12/12/2023 Archive](https://drive.google.com/file/d/1MbB300dAJUEtBld14Qd4loA6hD94v67B/view?usp=share_link)

## Background

Part 1: CamillaDSP Background

### Why would I want to use CamillaDSP on a RPi4?

This tutorial is geared towards 2 channel audio as it is somewhat difficult to get multichannel audio in to a RPi4. Typical applications are DIY active speakers / subwoofers such as Directiva R1 (4+ channels), LXmini + sub(s) or LX 521.4 (8+ channels). Another good application is passive stereo speakers with 3+ subwoofers. CamillaDSP makes the most sense for applications over 4 channels as the miniDSP Flex offers 4 channel DSP with good analog performance at a very reasonable price. You can do a 4 channel RPi4 + CamillaDSP setup for less cost than the Flex and such a setup has a few advantages, such as more processing power and volume control with dynamic loudness. Although it is possible to use other hardware with CamillaDSP, a RPi4 offers GPIO pins which are useful for integrating a display and has the ability to be used as a USB gadget.

### At a high level how does this work?

Starting point is a RPi4 (2 GB, 4 GB or 8 GB are all fine) running Ubuntu Server 64 bit. I prefer Ubuntu Server as it is very stable and works well with all multichannel DACs mentioned in this tutorial (and historically had a newer kernel than Raspberry Pi OS and other audio distros). We will set up CamillaDSP such that it is always running on the RPi4 as a service. A web browser based GUI is available to configure CamillaDSP after initial setup. CamillaDSP requires a capture device and playback device, the capture device is your input and playback device is your output.

The capture device can be a variety of things, it can be the RPi itself with software audio players such as squeezelite or shairport-sync playing to an ALSA loopback, it can be the same device as the playback device in the case of an audio interface with analog/digital inputs or it can be a separate device such as a TOSLINK to USB card. The main point here is that CamillaDSP is NOT limited to applications that use a RPi as a source.

The playback device is either a USB DAC/DDC, HDMI output of the RPi or HAT DAC/DDC. This tutorial will focus on USB DACs. Between the capture device and the playback device is where the magic happens, CamillaDSP can implement channel routing, IIR filters, FIR filters, volume control (w/ dynamic loudness), resampling and delay. The RPi4 is surprising powerful and is able to do much more than any miniDSP product that exists today.

### What DACs do you recommend?

1) Okto dac8 PRO - €1295, 8 channel balanced analog output, 8 channel AES digital input, 2 channel AES digital output, 1RU full-rack, volume knob, IR remote control, 5 V trigger, large display, excellent analog performance and overall design. Probably the highest performance 8 channel DAC but availability is an issue and long term support may be a concern. Okto dac8 PRO ASR Review.

2) MOTU Ultralite Mk5 - $600, 10 channel balanced analog output, 8 channel balanced analog input, TOSLINK input / output (can also do ADAT), SPDIF input / output, volume knob capable of controlling all analog outputs, 1RU half-rack, overall good analog performance. I recommend this DAC for most applications due to good analog performance, superior I/O functionality, reasonable price and smaller form factor. MOTU Ultralite Mk5 ASR Review.

3) MOTU M4 - $250, 4 channel unbalanced/balanced analog output, 4 channel balanced analog input, good analog performance. Good budget option for 2.1/2.2 or 2 way active systems, I/O functionality is rather limited. MOTU M4 ASR Review.

5) HifiBerry DAC8x - 

4) Whatever you have on hand! Part of the beauty of a CamillaDSP / RPi4 setup is that a RPi4 is cheap and available and if you want to try it out with another USB DAC it is rather easy to do so. Obviously I will not be able to provide specific configuration files but this tutorial should help you get started.

Although I am not providing configuration files for the following devices, I have used them successfully with CamillaDSP on a RPi4 and can help you with them if needed. In particular the MCHstreamer / USBstreamer are very useful as they allow you to use old pro audio interfaces with ADAT inputs to achieve 8 channels of output at 44.1/48 kHz.

- miniDSP MCHstreamer
- miniDSP USBstreamer
- Focusrite 18i20 2nd gen
- DIYINHK multichannel XMOS

Besides this tutorial what are other good sources of information?

CamillaDSP GitHub
Henrik has done a great job with the GitHub and it is an excellent reference. Almost everything I present here can also be found there.

CamillaDSP DIYAudio Thread
If you want to ask a question about CamillaDSP this is where I would ask it. A good thread to search if you have questions on a particular topic.

Pi4 + CamillaDSP + MOTU M4 ASR Thread
This was the thread that got me started with CamillaDSP. You can also search ASR for Camilla and find a few other useful threads.

Budget Standalone Toslink > DSP > Toslink with CamillaDSP ASR Thread
Great thread by @MarcosCh showing how to make a low cost (< 50€ !) TOSLINK input / output stereo room correction DSP using CamillaDSP.

Using a Raspberry Pi as equaliser in between an USB Source and USB DAC
Great thread from @DeLub on how to use a RPi as a USB gadget. Note if you are using Ubuntu 22.10 or later steps 1-6 can be skipped (no need to compile kernel).

