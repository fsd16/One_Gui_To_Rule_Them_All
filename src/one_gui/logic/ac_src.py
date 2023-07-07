# Finn Drabsch
# Enphase Energy
# 2023

from math import sqrt
from pathlib import Path
from enphase_equipment.ac_source.interface import Waveform 
from one_gui.logic.utils import import_class_from_string
import pyvisa as visa

class AC_SRC:
    """Class wrapper for the ac source
    """    
    def __init__(self, driver_path, address, *args, **kwargs):
        parent_class = import_class_from_string(driver_path)
        self.parent_instance = parent_class(address)
        # self.__class__ = type(self.__class__.__name__,
        #                     (parent_class, object),
        #                     dict(self.__class__.__dict__))
            
        # super(self.__class__, self).__init__(*args, **kwargs)

        # pre defined profiles
        self.PROFILES = {
            "240v, 60hz, Split Phase (NA)":   (240, 60, "split"), # North American (NA)
            "220v, 60hz, Split Phase ":       (220, 60, "split"), # Brazil (NA)
            "120v, 60hz, Single Phase":       (120, 60, "single"),  # North American (NA)
            "230v, 50hz, Single Phase (INT)": (230, 50, "single"),  # Rest of world (INT)
            "208V, 60hz, Three Phase ":       (208, 60, "three"), # North American Comercial (NA)
        }
        self.base_path = Path('C:/Python37/workspace/hw_testcases/src/hw_testcases/abnormal_waveform_test/waveforms')

        files = sorted(list(self.base_path.glob('*.wfd')) + list(self.base_path.glob('*.csv')))
        
        self.AB_WAVEFORMS = {wf.stem: Waveform.create_waveform_from_file(wf) for wf in files}

        self.rm = visa.ResourceManager()
        self.vl = self.rm.visalib

    # Callback to apply settings to AC
    def apply(self, ac_config):

        ac_rms_voltage = float(ac_config["ac_entry_ac_volts"])
 
        if ac_config["ac_radio_single"]:
            ac_voltage_tuple = (ac_rms_voltage / 2.0, ac_rms_voltage / 2.0)
        elif ac_config["ac_radio_split"]:
            ac_voltage_tuple = (ac_rms_voltage, 0)
        elif ac_config["ac_radio_three"]:
            ac_voltage_tuple = (round(ac_rms_voltage/sqrt(3)), round(ac_rms_voltage/sqrt(3)), round(ac_rms_voltage/sqrt(3)))

        ac_freq = ac_config["ac_entry_freq"]

        if ac_config["ac_check_abnormal"]:
            choice = ac_config["ac_menu_abnormal"]
            self.parent_instance.set_steady_state(voltages=ac_voltage_tuple, frequency=ac_freq, waveform=self.AB_WAVEFORMS[choice])
            # print(f"AC parameters applied: Voltages = {ac_voltage_tuple}, Frequency = {ac_freq}, Waveform = {choice}")
        else:
            self.parent_instance.set_steady_state(voltages=ac_voltage_tuple, frequency=ac_freq)
            # print(f"AC parameters applied: Voltages = {ac_voltage_tuple}, Frequency = {ac_freq}")
        
    # callback to apply settings and turn on ac output
    def turn_on(self):    
        self.parent_instance.on()
    
    # callback to turn off ac output
    def turn_off(self):
        self.parent_instance.off()
    
    def return_manual(self):
        # Put Ametek back into manual control after gui_test_runner test case leaves it in remote control
        b = self.rm.open_resource(self.parent_instance.resource_name)
        #vl.gpib_control_ren(b.session, visa.highlevel.constants.VI_GPIB_REN_DEASSERT)
        self.vl.gpib_control_ren(b.session, visa.highlevel.constants.VI_GPIB_REN_DEASSERT)
        # print("Manual control of AC source restored")
        
class Mock_AC_SRC:
    """Mock Class wrapper for the ac source
    """
    def __init__(self, *args, **kwargs):

        # pre defined profiles
        self.PROFILES = {
            "240v, 60hz, Split Phase (NA)":   (240, 60, "split"), # North American (NA)
            "220v, 60hz, Split Phase ":       (220, 60, "split"), # Brazil (NA)
            "120v, 60hz, Single Phase":       (120, 60, "single"),  # North American (NA)
            "230v, 50hz, Single Phase (INT)": (230, 50, "single"),  # Rest of world (INT)
            "208V, 60hz, Three Phase ":       (208, 60, "three"), # North American Comercial (NA)
        }
        self.base_path = Path('C:/Python37/workspace/hw_testcases/src/hw_testcases/abnormal_waveform_test/waveforms')

        files = sorted(list(self.base_path.glob('*.wfd')) + list(self.base_path.glob('*.csv')))
        
        self.AB_WAVEFORMS = {wf.stem: Waveform.create_waveform_from_file(wf) for wf in files}

    # Callback to apply settings to AC
    def apply(self, ac_config):
        pass
        
    # callback to apply settings and turn on ac output
    def turn_on(self):    
        pass
    
    # callback to turn off ac output
    def turn_off(self):
        pass
    
    def return_manual(self):
        pass