# This module will determinate operative system caracteristics
import platform
import sys
from datetime import datetime

OS_USERNAME = platform.uname()
OS_SYSTEM = platform.system()
PROCESOR = platform.processor()
PLATFORM = platform.platform()
__time_now = datetime.now() # It contains the time now
time_now = __time_now.strftime("%A %d/%m/%Y  %H:%M %p")

class Information:

    information = f"""
    
    Operative system : {OS_SYSTEM}
    -----------------------------------
    Platform         : {PLATFORM}
    -----------------------------------
    Username         : {OS_USERNAME[1]}
    -----------------------------------
    Processor        : {PROCESOR}
    -----------------------------------
    Arquitechture    : {OS_USERNAME[4]}
    -----------------------------------
    
    """

    def __repr__(self):
        return self.information


def get_system_info():
    info = Information()
    print(info)

