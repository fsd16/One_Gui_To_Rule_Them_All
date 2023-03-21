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
    
    def uniquify(self, path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + " (" + str(counter) + ")" + extension
            counter += 1

        return path

    # callback to take the scope capture
    def scope_capture(self, path, date, name, invert):
        capture_folder = Path(path)
        if not Path(capture_folder).exists():
            Path(capture_folder).mkdir(parents=True)
            print("made filepath: {}".format(capture_folder))

        date_prefix = ''
        if date:
            date_prefix = ("%s_" % (strftime("%Y-%m-%d_%H;%M;%S", localtime())))
        capture_name_str = name
        if Path(capture_name_str).suffix != '.png':
            capture_name_str = capture_name_str + '.png'
        

        capture_path = self.uniquify(capture_folder / (date_prefix + capture_name_str))
        self.capture(capture_path, invert_graticule=invert)
        print("Captured to: {}".format(capture_path))
        

        # This works for any number of digits in a single location in the name string
        # pat = re.compile(r'\d+')
        # if pat.search(capture_name_str):
            # new = 1 + int(pat.search(capture_name_str).group())
            # print(new)
            # capture_name_str = pat.sub(str(new), capture_name_str)
            # print(capture_name_str)

        # capture_name.set(capture_name_str)

    # callback to apply the labels
    def scope_label(self, ch1, ch2 , ch3, ch4):
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