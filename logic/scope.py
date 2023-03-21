from pathlib import Path
from time import strftime, localtime
import os
import time
from configparser import ConfigParser
from concurrent import futures
from enphase_equipment.oscilloscope.agilent import AgilentDSO


thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

class Scope(AgilentDSO):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.SCOPE = {
            "path": os.getcwd(),
            "name": "foo",
            "date": False,
            "invert": False,
            "ch1": "1",
            "ch2": "2",
            "ch3": "3",
            "ch4": "4",
        }
    
    # Ensure file name is unique
    def uniquify(self, path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + " (" + str(counter) + ")" + extension
            counter += 1

        return path

    def set_path(self, path):
        self.SCOPE["path"] = path
    
    def set_name(self, name):
        self.SCOPE["name"] = name
        
    def set_date(self, date):
        self.SCOPE["date"] = date
    
    def set_invert(self, invert):
        self.SCOPE["invert"] = invert

    def set_ch1(self, label):
        self.SCOPE["ch1"] = label
    
    def set_ch2(self, label):
        self.SCOPE["ch2"] = label
    
    def set_ch3(self, label):
        self.SCOPE["ch3"] = label
    
    def set_ch4(self, label):
        self.SCOPE["ch4"] = label
        
    # callback to take the scope capture
    def scope_capture(self):
        capture_folder = Path(self.SCOPE["path"])
        
        if not Path(capture_folder).exists():
            Path(capture_folder).mkdir(parents=True)
            print("made filepath: {}".format(capture_folder))

        date_prefix = ''
        if self.SCOPE["date"]:
            date_prefix = ("%s_" % (strftime("%Y-%m-%d_%H;%M;%S", localtime())))

        capture_name_str = self.SCOPE["name"]
        if Path(capture_name_str).suffix != '.png':
            capture_name_str = capture_name_str + '.png'

        capture_path = self.uniquify(capture_folder / (date_prefix + capture_name_str))
        self.capture(capture_path, invert_graticule=self.SCOPE["invert"])
        
        print("Captured to: {}".format(capture_path))

    # callback to apply the labels
    def scope_label(self):
        ch1, ch2 , ch3, ch4 = [self.SCOPE.get(k) for k in ["ch1", "ch2" , "ch3", "ch4"]]
        self.write(':DISPLAY:LABEL ON;:CHAN1:LABel "{}";:CHAN2:LABel "{}";:CHAN3:LABel "{}";:CHAN4:LABel "{}"'.format(ch1, ch2 ,ch3 ,ch4))
        print("labelled {}, {}, {}, {}".format(ch1, ch2 ,ch3 ,ch4))

    # Automatically scope capture if trigger occurs
    def auto_capture(self, auto_cap):
        if auto_cap:
            self.write("*CLS;:SINGle")
            
        while auto_cap:
            if bool(int(self.ask(":TER?"))): # True when a trigger has occured
                print("Capture Scope Data")
                time.sleep(0.5)
                self.scope_capture()
                self.write(":Single")

    # Create thread for auto capture to run in
    def auto_capture_on(self):
        thread_pool_executor.submit(self.auto_capture)    
        
    # callback to clean up and exit, used by the Close button
    def exit_clean(self):
        print("Bye ...")
        self.close()