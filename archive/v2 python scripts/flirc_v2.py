import evdev
import sys
import os
import time
import yaml
import glob
from camilladsp import CamillaClient

cdsp = CamillaClient("127.0.0.1",1234)
cdsp.connect()

flirc=evdev.InputDevice('/dev/input/by-id/usb-flirc.tv_flirc-if01-event-kbd')
flirc.grab()

active = cdsp.config.file_path()
configdir = active.split('camilladsp/configs/')[0] + 'camilladsp/configs/'

def main():

  for event in flirc.read_loop():
       config = glob.glob(configdir + '_*')
       cdspvolume = cdsp.volume.main()
       cdspmute = cdsp.mute.main()
       cdspvolumeold = cdspvolume
       if event.type == evdev.ecodes.EV_KEY:
            attrib = evdev.categorize(event)
            if attrib.keystate == 1:
                if attrib.keycode == 'KEY_DOWN':
                    if cdspvolume - 1 >= -99: #change to cdspvolume - 0.5 if you want 0.5 dB increments
                        cdsp.volume.set_main(cdspvolume - 1) # change to cdspvolume - 0.5 if you want 0.5 dB increments
                        cdspvolume = cdsp.volume.main()
                    else:
                        cdsp.volume.set_main(-99)
                        cdspvolume = cdsp.volume.main()

                elif attrib.keycode == 'KEY_UP':
                    if cdspvolume + 1 < 0: #change to cdspvolume + 0.5 if you want 0.5 dB increments
                         cdsp.volume.set_main(cdspvolume + 1) #change to cdspvolume + 0.5 if you want 0.5 dB increments
                         cdspvolume = cdsp.volume.main()
                    else:
                         cdsp.volume.set_main(0)
                         cdspvolume = cdsp.volume.main()

                elif attrib.keycode == 'KEY_LEFT':
                    if cdspmute == False:
                        cdsp.mute.set_main(True)
                        cdspmute = cdsp.mute.main()

                    else:
                        cdsp.mute.set_main(False)
                        cdspmute = cdsp.mute.main()


                elif attrib.keycode == 'KEY_RIGHT':
                    if len(config) != 1:
                       current = cdsp.config.file_path()
                       for i in range(len(config)):
                           if i == len(config)-1:
                              if current == config[i]:
                                 newconfig = config[0]
                           else:
                              if current == config[i]:
                                 newconfig = config[i+1]

                       cdsp.config.set_file_path(newconfig)
                       cdsp.general.reload()

            elif attrib.keystate == 2:
                if attrib.keycode == 'KEY_DOWN':
                    if cdspvolume - 1 >= -99: #change to cdspvolume - 0.5 if you want 0.5 dB increments
                        cdsp.volume.set_main(cdspvolume - 1) #change to cdspvolume - 0.5 volume if you want 0.5 increments
                        cdspvolume = cdsp.volume.main()
                    else:
                        cdsp.volume.set_main(-99)
                        cdspvolume = cdsp.volume.main()

                elif attrib.keycode == 'KEY_UP':
                    if cdspvolume + 1 < 0: #change to cdspvolume + 0.5 if you want 0.5 dB increments
                        cdsp.volume.set_main(cdspvolume + 1) #change to cdspvolume + 0.5 if you want 0.5 dB increments
                        cdspvolume = cdsp.volume.main()
                    else:
                        cdsp.volume.set_main(0)
                        cdspvolume = cdsp.volume.main()

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
