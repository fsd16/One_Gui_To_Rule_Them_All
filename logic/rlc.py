import math
from enphase_equipment.rlc_load.enphase_rlc_v2 import EnphaseRLCV2
from enphase_equipment.rlc_load.common import calculate_rlc_from_real_and_reactive_power
from enphase_equipment.rlc_load.common import calculate_real_and_reactive_power_from_rlc

class RLC(EnphaseRLCV2):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class NoInput(Exception):
        pass
    class VoltageInvalid(Exception):
        pass
    class PowerInvalid(Exception):
        pass
    class FrequencyInvalid(Exception):
        pass

    # def get_config(self):
    #     return self.SETTINGS
    
    # def set_config(self, config):
    #     self.SETTINGS = dict((config.get(k, k), v) for (k, v) in self.SETTINGS.items())

    # def set_ac_rms_volts(self, ac_rms_voltage):
    #     self.SETTINGS["ac_rms_voltage"] = ac_rms_voltage
        
    # def set_ac_freq(self, ac_freq):
    #     self.SETTINGS["ac_freq"] = ac_freq
        
    # def set_real_pwr(self, ac_config):
    #     self.SETTINGS["real_pwr"] = ac_config
        
    # def set_reactive_pwr(self, choice):
    #     self.SETTINGS["reactive_pwr"] = choice

    # def set_resistance(self, choice):
    #     raise NotImplementedError

    # def set_inductance(self, choice):
    #     raise NotImplementedError
        

    # Callback to apply settings and turn on rlc
    def on_power(self, rlc_config):
        ac_volts = rlc_config["rlc_entry_ac_volts"]
        ac_freq = rlc_config["rlc_entry_freq"]
        real_pwr = rlc_config["rlc_entry_real_pwr"]
        reactive_pwr = rlc_config["rlc_entry_reactive_pwr"]

        if all(v == 0 for v in rlc_config.values()):
            raise self.NoInput
        
        if ac_volts == 0:
            # voltage invalid
            raise self.VoltageInvalid

        if real_pwr == 0 and reactive_pwr == 0:
            # power invalid
            raise self.PowerInvalid

        if ac_freq == 0 and reactive_pwr >= 0:
            #frequency invalid
            raise self.FrequencyInvalid
        
        actual = self.request_power_config(real_power=real_pwr, reactive_power=reactive_pwr, ac_voltage=ac_volts, ac_frequency=ac_freq)
        # if real_pwr > 0:
        #     res = ac_volts*ac_volts/real_pwr
        # else:
        #     res = "Inf"
        # if reactive_pwr > 0:
        #     ind = 2*math.pi*ac_volts*ac_volts/reactive_pwr
        # else:
        #     ind = "Inf"
        rlc_config["rlc_entry_real_pwr"] = actual["actual_real_power"]
        rlc_config["rlc_entry_reactive_pwr"] = actual["actual_reactive_power"]
        r, l, c = calculate_rlc_from_real_and_reactive_power(actual["actual_real_power"],
                                                                actual["actual_reactive_power"],
                                                                ac_volts,
                                                                ac_freq)
                                                                
        print("real = {}, reactive = {}".format(actual["actual_real_power"],actual["actual_reactive_power"]))
        print("res = {}, ind = {}, cap = {}".format(r,l,c))
        print("rlc configured using power values")

        return rlc_config

    def on_rlc(self):
        raise NotImplementedError
        res = self.SETTINGS["resistance"]
        ind = self.SETTINGS["inductance"]

        actual = self.request_rlc_config(r=res, l=ind)
            
        print("res = {}, ind = {}".format(res,ind))
        print("rlc configured using rlc values")

    def turn_on(self, rlc_config):
        rlc_config = self.on_power(rlc_config)
        return rlc_config

    # callback to turn off rlc output
    def turn_off(self):
        self.close()
        print("rlc off")