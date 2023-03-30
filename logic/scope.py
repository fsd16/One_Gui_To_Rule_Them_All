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

        self.auto_cap_run = False
    
    # Ensure file name is unique
    def uniquify(self, path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + " (" + str(counter) + ")" + extension
            counter += 1

        return path
        
    # callback to take the scope capture
    def capture_display(self, sas_config):
        capture_folder = Path(sas_config["scope_line_cap_path"])
        
        if not Path(capture_folder).exists():
            Path(capture_folder).mkdir(parents=True)
            print("made filepath: {}".format(capture_folder))

        date_prefix = ''
        if sas_config["scope_check_date"]:
            date_prefix = ("%s_" % (strftime("%Y-%m-%d_%H;%M;%S", localtime())))

        capture_name_str = sas_config["scope_line_cap_name"]
        if Path(capture_name_str).suffix != '.png':
            capture_name_str = capture_name_str + '.png'

        capture_path = self.uniquify(capture_folder / (date_prefix + capture_name_str))
        self.capture(capture_path, invert_graticule=sas_config["scope_check_invert"])
        
        print("Captured to: {}".format(capture_path))

    # callback to apply the labels
    def label(self, sas_config):
        ch1, ch2 , ch3, ch4 = [sas_config.get(k) for k in ["scope_line_ch1_lab", "scope_line_ch2_lab" , "scope_line_ch3_lab", "scope_line_ch4_lab"]]
        self.write(':DISPLAY:LABEL ON;:CHAN1:LABel "{}";:CHAN2:LABel "{}";:CHAN3:LABel "{}";:CHAN4:LABel "{}"'.format(ch1, ch2 ,ch3 ,ch4))
        print("labelled {}, {}, {}, {}".format(ch1, ch2 ,ch3 ,ch4))

    # Automatically scope capture if trigger occurs
    def auto_capture(self, sas_config):
        self.write("*CLS;:SINGle")
            
        while self.auto_cap_run:
            if bool(int(self.ask(":TER?"))): # True when a trigger has occured
                print("Capture Scope Data")
                time.sleep(0.5)
                self.capture_display(sas_config)
                self.write(":Single")

    # Create thread for auto capture to run in
    def auto_capture_on(self, sas_config):
        auto_capture_thread = Thread(target=self.auto_capture, args=[sas_config])
        auto_capture_thread.start()
        self.auto_cap_run = True

    def auto_capture_off(self):
        self.auto_cap_run = False
        
    # callback to clean up and exit, used by the Close button
    def exit_clean(self):
        print("Bye ...")
        self.close()