import math
import os
from enphase_equipment.ac_source.interface import Waveform
from enphase_equipment.ac_source.pacific_power_source import PPS_308


class AC_SRC(PPS_308):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.reset()
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
            "IEC_77A_Class_1":                             ('IEC_77A_Class_1.wfd'),
            "IEC_77A_Class_2":                             ('IEC_77A_Class_2.wfd'),
            "_208_120_NastyCurrentSpiker":                 ('_208_120_NastyCurrentSpiker.wfd'),
            "Clip 12% THD":                                ('Clip 12% THD.wfd'),
            "MINV17":                                      ('MINV17.wfd'),
            "MINV18":                                      ('MINV18.wfd'),
            "Giles_5_19_17":                               ('Giles_5_19_17.wfd'),
            "InductiveCurrent":                            ('InductiveCurrent.wfd'),
            "InductiveCurrent_With_A_HintOfCapacitance":   ('InductiveCurrent_With_A_HintOfCapacitance.wfd'),
            "LangLake_Zero_Cross_Distortion":              ('LangLake_Zero_Cross_Distortion.wfd'),
            "NastyCurrentSpiker":                          ('NastyCurrentSpiker.wfd'),
            "Poleshek":                                    ('Poleshek.wfd'),
            "TWACS_VL1Na":                                 ('TWACS_VL1Na.wfd'),
            "Triangle":                                    ('Triangle.wfd'),
            "ross_vL1n":                                   ('ross_vL1n.wfd'),
            "Amanda_Welz_Florida":                         ('Amanda_Welz_Florida.wfd'),
        }
        
        self.SETTINGS = {
            "ac_rms_voltage": 240,
            "ac_freq": 60,
            "config": "split",
            "abnormal": "IEC_77A_Class_1"
        }
    def get_config(self):
        return self.SETTINGS
    
    def set_config(self, config):
        self.SETTINGS = config

    def set_ac_rms_volts(self, ac_rms_voltage):
        self.SETTINGS["ac_rms_voltage"] = ac_rms_voltage
        
    def set_ac_freq(self, ac_freq):
        self.SETTINGS["ac_freq"] = ac_freq
        
    def set_ac_config(self, ac_config):
        self.SETTINGS["config"] = ac_config
        
    # Callback to select abnormal waveform
    def set_ab_waveform(self, choice):
        self.SETTINGS["abnormal"] = choice
    
    # def set_ac_profile(self, profile_key):
    #     profile = self.PROFILES[profile_key]
    #     self.SETTINGS.update(ac_rms_voltage=profile[0], ac_freq=profile[1], config=profile[2])
    
    # Callback to set ac voltage
    def calc_ac_volts(self):
        config = self.SETTINGS["config"]
        ac_rms_voltage = self.SETTINGS["ac_rms_voltage"]
        
        if config == "split":
            ac_voltage_tuple = (ac_rms_voltage / 2.0, ac_rms_voltage / 2.0)
        elif config == "single":
            ac_voltage_tuple = (ac_rms_voltage, 0)
        elif config == "three":
            ac_voltage_tuple = (round(ac_rms_voltage/math.sqrt(3)), round(ac_rms_voltage/math.sqrt(3)), round(ac_rms_voltage/math.sqrt(3)))
        
        return ac_voltage_tuple

    # Callback to apply settings to AC
    def apply(self):
        
        self.prog_voltage_line_voltages(99, self.calc_ac_volts(), self.SETTINGS["ac_freq"])
        self.exec_program(99)
        print("AC updated ")
        
    def apply_abnormal(self):
        
        choice = self.SETTINGS["abnormal"]
        path = os.path.join(self.base_path, (self.AB_WAVEFORMS[choice]))
        continuous_waveform = Waveform.create_waveform_from_file(path)
        
        self.set_steady_state(voltages=self.calc_ac_volts(), frequency=self.SETTINGS["ac_freq"], waveform=continuous_waveform)
        
    # callback to apply settings and turn on ac output
    def turn_on(self):    
        self.on()
        print("ac on")
    
    # callback to turn off ac output
    def turn_off(self):
        self.off()
        print("ac off")