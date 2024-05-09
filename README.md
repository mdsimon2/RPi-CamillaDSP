# RPi-CamillaDSP

Intent of this project is to provide guidance for setting up [CamillaDSP](https://github.com/HEnquist/camilladsp) on a RPi4/5. There is a lot of good information scattered through [ASR](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/), [DIYAudio](https://www.diyaudio.com/community/threads/camilladsp-cross-platform-iir-and-fir-engine-for-crossovers-room-correction-etc.349818/) and the [CamillaDSP GitHub](https://github.com/HEnquist/camilladsp) but there also appears to be a lot of apprehension. My goal is to give concrete examples of how to use CamillaDSP with a variety of hardware to ease some of that apprehension. This tutorial originally lived at ASR but in May 2024 I decided to migrate it to GitHub to make version management easier and provide a more universal location.

I realize this tutorial is long and looks daunting. I felt the same way when trying to figure this stuff out. My advice is to take it step by step, go slowly and ask questions. Some DIY projects are not worth the effort but this one is. At the end of this project you will have a DSP with almost unparalleled processing power in a very small form factor, easily configured via web interface, all at a very low cost compared to commercial options.

I would like to especially thank @HenrikEnquist for developing CamillaDSP. I’ve long been skeptical of computer-based DSP but CamillaDSP is a game changer. It runs on minimal hardware, is easy to interface with a variety of devices and is exceptionally well designed. I’ve replaced all of my miniDSP systems with RPi4s running CamillaDSP and could not be happier.

The tutorial is divided in to 4 parts, Part 1 talks through CamillaDSP background, Part 2 covers initial CamillaDSP setup, Part 3 documents specific CamillaDSP configuration files for various multichannel DACs and Part 4 talks covers advanced topics such as the GUI, displays, IR receivers, trigger output options and cases.

I am not a programmer or DSP expert, my primary motivation is finding better ways to implement DIY active speakers. If you see a better way of doing something or want further explanation please speak up! These instructions have been developed as I learned how to implement CamillaDSP and found better ways to set it up but I am always learning.

Prior to GitHub, I archived older versions of the tutorial at the links below.

Old Versions
10/20/2022 Archive
12/12/2023 Archive

Similarly, revision log prior to GitHub is shown below.

Revision Log
-01/18/2022: Fixed error with quotation mark in squeezelite configuration instructions.
-01/19/2022: Added 1 dB attenuation to all output channels of Okto configuration to avoid digital clipping. Added further discussion about digital clipping when using downstream volume control. Added dates to configuration files.
-01/20/2022: Revised instructions for ALSA loopback to run sudo apt install linux-modules-extra-raspi instead of sudo apt install linux-modules-extra-$(uname -r). This should allow the loopback to persist through kernel updates without running any additional commands.
-01/26/2022: Added brief notes on specific micro SD card models.
-01/27/2022: Small editorial changes, thanks @Wirrunna for the feedback.
-02/01/2022: Updated case pictures to match attached drawings.
-03/29/2022: Updated following:
*Added more detail on how to install and use WSL
*Added guidance on how to copy / paste in to terminal
*Added guidance on how to use scp to copy files to RPi
*Added steps for starting camilladsp and camillagui from terminal before implementing service
*Added logging to camilladsp service
*Updated flirc.py and oled.py with source switching functionality
*Added video of display
03/31/2022: Moved ALSA Loopback installation step sooner.
04/10/2022: Added instructions to implement bluetooth using bluez-alsa.
04/26/2022: Minor updates for use with Ubuntu Server 22.04 64 bit.
05/04/2022: Updated to reflect CamillaDSP V1.0.0 release. Changed to using symlink configuration file.
05/22/2022: Slight update to reflect that SPDIF input works on Focusrite 18i20 2nd gen as Ubuntu 22.04.
07/17/2022: Updated flirc.py and oled.py to implement mute functionality bound to KEY_LEFT.
07/21/2022: Added upgrade instructions and revised to use CamillaDSP V1.0.1 and rc5 GUI.
08/11/2022: Minor update to flirc.py to better integrate with GUI.
08/16/2022: Removed all directory changes to make installation easier.
10/20/2022: Major update for Ubuntu 22.10 and V1.0.2 CamillaDSP and V1.0.0 CamillaGUI
11/29/2022: Minor update to reflect V1.0.3 CamillaDSP and V1.0.1 CamillaGUI
11/30/2022: Updated following:
+Changed to single flirc.py routine as a result of CamillaDSP mute behavior changes
+Implemented improved configuration switching in flirc.py and oled.py
+Updated oled.py to eliminate display anomalies when switching from longer to short text strings
02/21/2022: Added performance improvements to oled.py based on feedback from @LandscapeJohn.
03/25/2023: Changed recommended display mounting hardware for 10 mm faceplate from 5 mm to 3 mm long screws.
04/18/2023: Updated oled.py with option for smaller volume font with tenths place. Also updated flirc.py to with option for 0.5 dB volume increments.
04/20/2023: Updated oled.py with option to display clipped samples instead of CDSP status.
04/25/2023: Minor update to give option for Ubuntu Server 23.04 64 bit.
07/17/2023: Minor update to use WantedBy=multi-user.target instead of WantedBy=graphical.target for all services.
12/15/2023: Major update to reflect V2.0.0 CamillaDSP and CamillaGUI.
03/02/2024: Minor update to reflect V2.0.3 CamillaDSP and V2.1.0 CamillaGUI.
03/14/2024: Updated oled-rpi.gpio.py and oled-lgpio.py to use optimized code, oled-lgpio.py is now significantly faster.
03/15/2024: Updated oled-rpi.gpio.py and oled-lgpio.py to use set_sleep_mode to avoid wiping effect.
