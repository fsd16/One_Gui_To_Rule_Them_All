from enphase_equipment.rlc_load.common import calculate_rlc_from_real_and_reactive_power
from one_gui.logic.utils import import_class_from_string
from time import sleep

class RLC:
    """Class wrapper for the RLC load
    """
    def __init__(self, driver_path, address, *args, **kwargs):
        parent_class = import_class_from_string(driver_path)
        self.parent_instance = parent_class(address)
        # self.__class__ = type(self.__class__.__name__,
        #                     (parent_class, object),
        #                     dict(self.__class__.__dict__))
            
        # super(self.__class__, self).__init__(*args, **kwargs)
    class NoInput(Exception):
        pass
    class VoltageInvalid(Exception):
        pass
    class PowerInvalid(Exception):
        pass
    class FrequencyInvalid(Exception):
        pass

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
        
        actual = self.parent_instance.request_power_config(real_power=real_pwr, reactive_power=reactive_pwr, ac_voltage=ac_volts, ac_frequency=ac_freq)

        r, l, c = calculate_rlc_from_real_and_reactive_power(actual["actual_real_power"],
                                                                actual["actual_reactive_power"],
                                                                ac_volts,
                                                                ac_freq)
                                                                
        print(f"RLC parameters applied: Resistance = {r}, Inductance = {l}, Capacitance = {c}")
        print(f'RLC configured Power: Real Power = {actual["actual_real_power"]}, Reactive Power = {actual["actual_reactive_power"]}')

    def turn_on(self, rlc_config):
        self.on_power(rlc_config)
        print("RLC on")

    # callback to turn off rlc output
    def turn_off(self):
        # open interlock and shutdown master relay power supply
        self.parent_instance.enable_master_relay(False)
        print("RLC off")
        
    def close(self):
        self.parent_instance.close()
        
class Mock_RLC:
    def __init__(self, *args, **kwargs):
        pass
    
    class NoInput(Exception):
        pass
    class VoltageInvalid(Exception):
        pass
    class PowerInvalid(Exception):
        pass
    class FrequencyInvalid(Exception):
        pass
    
    # Callback to apply settings and turn on rlc
    def on_power(self, *args, **kwargs):
        pass

    def turn_on(self, *args, **kwargs):
        pass

    # callback to turn off rlc output
    def turn_off(self, *args, **kwargs):
        pass
    
    def close(self):
        pass