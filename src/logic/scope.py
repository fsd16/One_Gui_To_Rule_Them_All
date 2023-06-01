from pathlib import Path
from time import strftime, localtime, sleep
from concurrent import futures
from logic.equipment_library import import_class_from_string
from threading import Thread
from logic.utils import uniquify

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)

class Scope():

    def __init__(self, driver_path, *args, **kwargs):
        parent_class = import_class_from_string(driver_path)
        self.__class__ = type(self.__class__.__name__,
                            (parent_class, object),
                            dict(self.__class__.__dict__))
            
        super(self.__class__, self).__init__(*args, **kwargs)

        self.auto_cap_run = False
        # self.scope_run_state = "Run"

    def interface_type(self):
        return self.resource_name.partition(':')[0][:-1]
        
    # callback to take the scope capture
    def capture_display(self, sas_config):
        capture_folder = Path(sas_config["scope_line_cap_path"])

        if capture_folder == Path(""):
            capture_folder = Path.cwd().joinpath('captures')
        
        if not Path(capture_folder).exists():
            Path(capture_folder).mkdir(parents=True)
            print(f"Made filepath: {capture_folder}")

        date_prefix = ''
        if sas_config["scope_check_date"]:
            date_prefix = ("%s_" % (strftime("%Y-%m-%d_%H;%M;%S", localtime())))

        capture_name_str = sas_config["scope_line_cap_name"]
        if Path(capture_name_str).suffix != '.png':
            capture_name_str = capture_name_str + '.png'

        filename = uniquify(capture_folder / (date_prefix + capture_name_str))

        if self.interface_type() == 'USB':
            fileformat = 'BMP8bit'
        else:
            fileformat = 'PNG'
        self.capture(filename, invert_graticule=sas_config["scope_check_invert"], fileformat=fileformat)
        
        print(f"Scope display captured to: {filename}")

    # callback to apply the labels
    def label(self, sas_config):
        ch1, ch2 , ch3, ch4 = [sas_config.get(k) for k in ["scope_line_ch1_lab", "scope_line_ch2_lab" , "scope_line_ch3_lab", "scope_line_ch4_lab"]]
        self.write(f':DISPLAY:LABEL ON;:CHAN1:LABel "{ch1}";:CHAN2:LABel "{ch2}";:CHAN3:LABel "{ch3}";:CHAN4:LABel "{ch4}"')
        print(f"Scope channel labels applied: CH1 = {ch1}, CH2 = {ch2}, CH3 = {ch3}, CH4 = {ch4}")

    # Automatically scope capture if trigger occurs
    def auto_capture(self, sas_config):
        self.write(":TIMebase:MODE MAIN;*CLS;:SINGle")
        
        while self.auto_cap_run:
            if bool(int(self.ask(":TER?"))): # True when a trigger has occured
                print("Capture Scope Data")
                sleep(0.5)
                self.capture_display(sas_config)
                self.write(":Single")

    # Create thread for auto capture to run in
    def auto_capture_on(self, sas_config):
        
        auto_capture_thread = Thread(target=self.auto_capture, args=[sas_config])
        auto_capture_thread.start()
        self.auto_cap_run = True
        # self.scope_run_state = self.ask(":RSTate?")
        # print(self.scope_run_state)
        print("Auto capture started")

    def auto_capture_off(self):
        self.auto_cap_run = False
        # print(f":{self.scope_run_state}")
        # self.write(f":{self.scope_run_state}")
        print("Auto capture stopped")
        
    # callback to clean up and exit, used by the Close button
    def turn_off(self):
        self.close()
        print("Scope conection closed")