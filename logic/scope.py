from pathlib import Path
from time import strftime, localtime
import os
import time
from configparser import ConfigParser
from concurrent import futures
from enphase_equipment.oscilloscope.agilent import AgilentDSO
from threading import Thread


thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

class Scope(AgilentDSO):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SETTINGS = {
            # update to mkdir if doesnt exist
            "path": str(os.getcwd()/Path('captures')),
            "name": "foo",
            "date": False,
            "invert": False,
            "ch1": "1",
            "ch2": "2",
            "ch3": "3",
            "ch4": "4",
        }

        self.auto_cap_run = False
    
    # Ensure file name is unique
    def uniquify(self, path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + " (" + str(counter) + ")" + extension
            counter += 1

        return path

    def get_config(self):
        return self.SETTINGS
    
    def set_config(self, config):
        self.SETTINGS = config

    def set_path(self, path):
        self.SETTINGS["path"] = path
    
    def set_name(self, name):
        self.SETTINGS["name"] = name
        
    def set_date(self, date):
        self.SETTINGS["date"] = date
    
    def set_invert(self, invert):
        self.SETTINGS["invert"] = invert

    def set_ch1(self, label):
        self.SETTINGS["ch1"] = label
    
    def set_ch2(self, label):
        self.SETTINGS["ch2"] = label
    
    def set_ch3(self, label):
        self.SETTINGS["ch3"] = label
    
    def set_ch4(self, label):
        self.SETTINGS["ch4"] = label
        
    # callback to take the scope capture
    def capture_display(self):
        capture_folder = Path(self.SETTINGS["path"])
        
        if not Path(capture_folder).exists():
            Path(capture_folder).mkdir(parents=True)
            print("made filepath: {}".format(capture_folder))

        date_prefix = ''
        if self.SETTINGS["date"]:
            date_prefix = ("%s_" % (strftime("%Y-%m-%d_%H;%M;%S", localtime())))

        capture_name_str = self.SETTINGS["name"]
        if Path(capture_name_str).suffix != '.png':
            capture_name_str = capture_name_str + '.png'

        capture_path = self.uniquify(capture_folder / (date_prefix + capture_name_str))
        self.capture(capture_path, invert_graticule=self.SETTINGS["invert"])
        
        print("Captured to: {}".format(capture_path))

    # callback to apply the labels
    def label(self):
        ch1, ch2 , ch3, ch4 = [self.SETTINGS.get(k) for k in ["ch1", "ch2" , "ch3", "ch4"]]
        self.write(':DISPLAY:LABEL ON;:CHAN1:LABel "{}";:CHAN2:LABel "{}";:CHAN3:LABel "{}";:CHAN4:LABel "{}"'.format(ch1, ch2 ,ch3 ,ch4))
        print("labelled {}, {}, {}, {}".format(ch1, ch2 ,ch3 ,ch4))

    # Automatically scope capture if trigger occurs
    def auto_capture(self):
        self.write("*CLS;:SINGle")
            
        while self.auto_cap_run:
            if bool(int(self.ask(":TER?"))): # True when a trigger has occured
                print("Capture Scope Data")
                time.sleep(0.5)
                self.capture_display()
                self.write(":Single")

    # Create thread for auto capture to run in
    def auto_capture_on(self):
        auto_capture_thread = Thread(target=self.auto_capture)
        auto_capture_thread.start()
        self.auto_cap_run = True

    def auto_capture_off(self):
        self.auto_cap_run = False
        
    # callback to clean up and exit, used by the Close button
    def exit_clean(self):
        print("Bye ...")
        self.close()