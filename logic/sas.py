# -*- coding: utf-8 -*-
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import (
    FigureCanvasWxAgg as FigureCanvas,
    NavigationToolbar2WxAgg as NavigationToolbar
)
from enphase_station.station_obj import STATION
from enphase_equipment.solar_array_simulator.agilent import AgilentE4360A

class SAS(AgilentE4360A):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def get_config(self):
    #     return self.SETTINGS
    
    # def set_config(self, config):
    #     self.SETTINGS = config

    # def set_vmp(self, vmp):
    #     self.SETTINGS["vmp"] = vmp

    # def set_pmp(self, pmp):
    #     self.SETTINGS["pmp"] = pmp

    # def set_ff(self, ff):
    #     self.SETTINGS["ff"] = ff

    # def set_irrad(self, irrad):
    #     self.SETTINGS["irrad"] = irrad

    def apply(self, sas_config):
        sas_curve = self.create_table(Pmp=sas_config["sas_entry_pmp"],
                                        Vmp=sas_config["sas_entry_vmp"],
                                        FillFactor=sas_config["sas_entry_ff"],
                                        irradiance=sas_config["sas_entry_irrad"])
        
        
        vi_array = np.array(sas_curve[1]).astype(np.float)
        p_array = [vi_array[0], vi_array[0] * vi_array[1]]

        self.select_table()
        self.select_table_mode()
        return vi_array, p_array

    def turn_on(self):
        self.on()
        print("SAS on")

    def turn_off(self):
        self.off()
        print("SAS off")
