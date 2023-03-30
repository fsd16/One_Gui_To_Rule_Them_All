# -*- coding: utf-8 -*-
import numpy as np
import time

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import (
    FigureCanvasWxAgg as FigureCanvas,
    NavigationToolbar2WxAgg as NavigationToolbar
)
from enphase_station.station_obj import STATION
from enphase_equipment.solar_array_simulator.agilent import AgilentE4360A

from threading import Thread

class SAS(AgilentE4360A):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_vi_run = False
        self.measured_pi = {
            "p": 0,
            "i": 0
        }

    # Create thread for auto measure to run in
    def update_vi(self):

        while self.update_vi_run:
            sas_measurement = self.measurement()

            measured_v = sas_measurement['dc_volts']
            measured_i = sas_measurement['dc_amps']
            calculated_p = measured_v * measured_i

            self.measured_pi["i"] = measured_i
            self.measured_pi["v"] = measured_i
            print("updated")
            time.sleep(0.5)


    def apply(self, sas_config):
        sas_curve = self.create_table(Pmp=sas_config["sas_entry_pmp"],
                                        Vmp=sas_config["sas_entry_vmp"],
                                        FillFactor=sas_config["sas_entry_ff"],
                                        irradiance=sas_config["sas_entry_irrad"])
        
        vi_array = np.array(sas_curve[1]).astype(np.float)
        p_array =  vi_array[0]* vi_array[1]
        
        sas_data  = {
            "i": vi_array[0],
            "v": vi_array[1],
            "p": p_array
        }

        

        self.select_table()
        self.select_table_mode()
        return sas_data

    def turn_on(self):
        self.on()
        print("SAS on")
        self.update_vi_run = True
        update_vi_thread = Thread(target=self.update_vi)
        update_vi_thread.start()
        

    def turn_off(self):
        self.update_vi_run = False
        self.off()
        print("SAS off")
        
