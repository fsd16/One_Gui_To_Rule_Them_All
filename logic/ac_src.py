from math import sqrt
from os.path import join
from enphase_equipment.ac_source.interface import Waveform 
from logic.equipment_library import import_class_from_string
import pyvisa as visa

class AC_SRC():
        
    def __init__(self, driver_path, *args, **kwargs):
        parent_class = import_class_from_string(driver_path)
        self.__class__ = type(self.__class__.__name__,
                            (parent_class, object),
                            dict(self.__class__.__dict__))
            
        super(self.__class__, self).__init__(*args, **kwargs)

        # pre defined profiles
        self.PROFILES = {
            "240v, 60hz, Split Phase (NA)":   (240, 60, "split"), # North American (NA)
            "220v, 60hz, Split Phase ":       (220, 60, "split"), # Brazil (NA)
            "120v, 60hz, Single Phase":       (120, 60, "single"),  # North American (NA)
            "230v, 50hz, Single Phase (INT)": (230, 50, "single"),  # Rest of world (INT)
            "208V, 60hz, Three Phase ":       (208, 60, "three"), # North American Comercial (NA)
        }
        self.base_path = 'C:/Users/fdrabsch/Envs/enphase_env/workspace/hw_testcases/src/hw_testcases/abnormal_waveform_test/waveforms'

        self.AB_WAVEFORMS = {
            "IEC 77A Class 1":                             ('IEC_77A_Class_1.wfd'),
            "IEC 77A Class 2":                             ('IEC_77A_Class_2.wfd'),
            "_208_120 NastyCurrentSpiker":                 ('_208_120_NastyCurrentSpiker.wfd'),
            "Clip 12% THD":                                ('Clip_12%_THD.wfd'),
            "MINV17":                                      ('MINV17.wfd'),
            "MINV18":                                      ('MINV18.wfd'),
            "Giles 5 19 17":                               ('Giles_5_19_17.wfd'),
            "InductiveCurrent":                            ('InductiveCurrent.wfd'),
            "InductiveCurrent WaHoC":   ('InductiveCurrent_With_A_HintOfCapacitance.wfd'),
            "LangLake Zero Cross Distortion":              ('LangLake_Zero_Cross_Distortion.wfd'),
            "NastyCurrentSpiker":                          ('NastyCurrentSpiker.wfd'),
            "Poleshek":                                    ('Poleshek.wfd'),
            "TWACS VL1Na":                                 ('TWACS_VL1Na.wfd'),
            "Triangle":                                    ('Triangle.wfd'),
            "ross vL1n":                                   ('ross_vL1n.wfd'),
            "Amanda Welz Florida":                         ('Amanda_Welz_Florida.wfd'),
        }

        self.rm = visa.ResourceManager()
        self.vl = self.rm.visalib
    
    # Callback to set ac voltage
    def calc_ac_volts(self, config, ac_rms_voltage):
        
        if config == "split":
            ac_voltage_tuple = (ac_rms_voltage / 2.0, ac_rms_voltage / 2.0)
        elif config == "single":
            ac_voltage_tuple = (ac_rms_voltage, 0)
        elif config == "three":
            ac_voltage_tuple = (round(ac_rms_voltage/sqrt(3)), round(ac_rms_voltage/sqrt(3)), round(ac_rms_voltage/sqrt(3)))
        
        return ac_voltage_tuple

    # Callback to apply settings to AC
    def apply(self, ac_config):
 
        if ac_config["ac_radio_single"]:
            phase_config = "single"
        elif ac_config["ac_radio_split"]:
            phase_config = "split"
        elif ac_config["ac_radio_three"]:
            phase_config = "three"

        ac_voltage_tuple = self.calc_ac_volts(phase_config, float(ac_config["ac_entry_ac_volts"]))

        ac_freq = ac_config["ac_entry_freq"]

        if ac_config["ac_check_abnormal"]:
            choice = ac_config["ac_menu_abnormal"]
            filepath = join(self.base_path, (self.AB_WAVEFORMS[choice]))
            continuous_waveform = Waveform.create_waveform_from_file(filepath)
            self.set_steady_state(voltages=ac_voltage_tuple, frequency=ac_freq, waveform=continuous_waveform)
            print(f"AC parameters applied: Voltages = {ac_voltage_tuple}, Frequency = {ac_freq}, Waveform = {choice}")
        else:
            self.set_steady_state(voltages=ac_voltage_tuple, frequency=ac_freq)
            print(f"AC parameters applied: Voltages = {ac_voltage_tuple}, Frequency = {ac_freq}")
        
    # callback to apply settings and turn on ac output
    def turn_on(self):    
        self.on()
        print("AC on")
    
    # callback to turn off ac output
    def turn_off(self):
        self.off()
        print("AC off")
    
    def return_manual(self):
        # Put Ametek back into manual control after gui_test_runner test case leaves it in remote control
        b = self.rm.open_resource(self.resource_name)
        #vl.gpib_control_ren(b.session, visa.highlevel.constants.VI_GPIB_REN_DEASSERT)
        self.vl.gpib_control_ren(b.session, visa.highlevel.constants.VI_GPIB_REN_DEASSERT)
        print("Manual control of AC source restored")