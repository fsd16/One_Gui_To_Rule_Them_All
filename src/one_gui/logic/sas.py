# Finn Drabsch
# Enphase Energy
# 2023

import numpy as np
from enphase_equipment.solar_array_simulator.agilent import DcSupplyCluster
from one_gui.logic.utils import import_class_from_string

class SAS:
    """Class wrapper for the SAS
    """
    def __init__(self, driver_path, addresses, config, *args, **kwargs):
        if type(driver_path) == type(dict()):
            clusters = []
            for address in addresses:
                sas_class = import_class_from_string(driver_path['SAS Drivers'])
                clusters.append(sas_class(address))
            parent_class = import_class_from_string(driver_path['Cluster Driver'])
            self.parent_instance = parent_class(clusters, config)
        else:
            parent_class = import_class_from_string(driver_path)
            self.parent_instance = parent_class(addresses[0])

    def get_sas_pv(self):

        sas_measurement = self.parent_instance.measurement()

        measured_v = sas_measurement['dc_volts']
        measured_i = sas_measurement['dc_amps']
        calculated_p = measured_v * measured_i

        sas_data  = {
            "v": measured_v,
            "i": measured_i,
            "p": calculated_p
        }

        return sas_data

    def apply(self, sas_config):
        Pmp = sas_config["sas_entry_pmp"]
        Vmp = sas_config["sas_entry_vmp"]
        ff = sas_config["sas_entry_ff"]
        irrad = sas_config["sas_entry_irrad"]
        sas_curve = self.parent_instance.create_table(Pmp=float(Pmp),
                                        Vmp=float(Vmp),
                                        FillFactor=float(ff),
                                        irradiance=float(irrad))
        
        vi_array = np.array(sas_curve[1]).astype(np.float)
        p_array =  vi_array[0]* vi_array[1]
        
        sas_data  = {
            "v": vi_array[0],
            "i": vi_array[1],
            "p": p_array
        }

        self.parent_instance.select_table()
        self.parent_instance.select_table_mode()
        print(f"SAS parameters applied: Pmp = {Pmp}, Vmp = {Vmp}, FF = {ff}, Irradiance = {irrad}")
        return sas_data

    def turn_on(self):
        self.parent_instance.on()
        print("SAS on")

    def turn_off(self):
        self.parent_instance.off()
        print("SAS off")
        
class Mock_SAS:
    """Class wrapper for the SAS
    """
    def __init__(self, *args, **kwargs):
        pass

    def get_sas_pv(self, *args, **kwargs):

        sas_data  = {
            "v": 0,
            "i": 0,
            "p": 0
        }

        return sas_data

    def apply(self, *args, **kwargs):
        
        sas_data  = {
            "v": [0],
            "i": [0],
            "p": [0]
        }
        
        return sas_data

    def turn_on(self, *args, **kwargs):
        pass

    def turn_off(self, *args, **kwargs):
        pass