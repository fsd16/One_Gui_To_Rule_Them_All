import numpy as np
from enphase_equipment.solar_array_simulator.agilent import AgilentE4360A, AgilentE43XXCluster

class SAS(AgilentE43XXCluster):

    def __init__(self, addresses, *args, **kwargs):
        sass = []
        for address in addresses:
            sass.append(AgilentE4360A(address))
        super().__init__(sass, *args, **kwargs)
        
    def get_sas_pv(self):

        sas_measurement = self.measurement()

        measured_v = sas_measurement['dc_volts']
        measured_i = sas_measurement['dc_amps']
        calculated_p = measured_v * measured_i

        return calculated_p, measured_v

    def apply(self, sas_config):
        Pmp = sas_config["sas_entry_pmp"]
        Vmp = sas_config["sas_entry_vmp"]
        ff = sas_config["sas_entry_ff"]
        irrad = sas_config["sas_entry_irrad"]
        sas_curve = self.create_table(Pmp=float(Pmp),
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

        self.select_table()
        self.select_table_mode()
        print(f"SAS parameters applied: Pmp = {Pmp}, Vmp = {Vmp}, FF = {ff}, Irradiance = {irrad}")
        return sas_data

    def turn_on(self):
        self.on()
        print("SAS on")

    def turn_off(self):
        self.off()
        print("SAS off")
        
