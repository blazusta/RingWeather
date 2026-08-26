import os
# This line prevents pygame from displaying its welcome message.
# Assigning the value 1 means this environment variable will take the value of 'True'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import datetime as dt
from time import sleep
from pygame import mixer

class Alarm:
    """
    Class for managing the alarm. 
    Includes a lock (is_active) to prevent running multiple alarms simultaneously,
    and a kill switch (cancel) to stop the waiting thread.
    """  

    def __init__(self, ringtone_path):
        self.ringtone_path = ringtone_path
        self.cancel = False       # Kill switch to stop the alarm before it rings
        self.is_active = False    # Lock to prevent setting another alarm if one is already active
        mixer.init()


    @staticmethod
    def get_date():
        """Returns today's date in day-month-year format."""
        today = dt.datetime.now()
        today = today.strftime("%d-%m-%Y")
        return today


    def set_alarm(self, hrs:int, min:int, sec=0):
        """Enters an infinite loop to wait for the specified time."""
        self.cancel = False
        while True:
            # Did the user trigger the cancel switch? If yes, exit quietly
            if self.cancel:
                return False
            
            now = dt.datetime.now()
            if now.hour == hrs and now.minute == min and now.second == sec:
                return True
            
            # CPU checks time every 200ms (5 times a second) to make the program
            # faster, and less resource-intensive
            sleep(0.2)
            

    def play_alarm(self, rep=1):
        """Plays the ringtone. rep=-1 makes it loop indefinitely until stopped."""
        mixer.music.load(self.ringtone_path)
        mixer.music.play(loops=rep)


    def stop_alarm(self) -> bool:
        """Stops the audio if it's ringing, and releases the lock."""
        if mixer.music.get_busy():
            mixer.music.stop()
            self.is_active = False  
            print("\n[OK]: Alarm stopped successfully.")
            return True
        else:
            print("[WARN]: No alarm is ringing now.")
            return False
        

    def cancel_alarm(self):
        """Triggers the cancel switch to terminate the waiting thread."""
        if self.is_active:
            self.cancel = True
            self.is_active = False   # Release the lock to allow setting a new alarm
            print("[OK]: Alarm cancelled successfully.")
        else:
            print("[WARN]: You have not set an alarm yet.")