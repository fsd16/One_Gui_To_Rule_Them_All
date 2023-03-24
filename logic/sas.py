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

        self.SAS_VALUES = {
            "vmp": 30.0,
            "pmp": 100.0,
            "ff": 0.78,
            "irrad": 1.0,
        }

    def set_vmp(self, vmp):
        self.SAS_VALUES["vmp"] = vmp

    def set_pmp(self, pmp):
        self.SAS_VALUES["pmp"] = pmp

    def set_ff(self, ff):
        self.SAS_VALUES["ff"] = ff

    def set_irrad(self, irrad):
        self.SAS_VALUES["irrad"] = irrad

    def sas_apply(self):
        sas_curve = self.create_table(Pmp=self.SAS_VALUES["pmp"],
                                        Vmp=self.SAS_VALUES["vmp"],
                                        FillFactor=self.SAS_VALUES["ff"],
                                        irradiance=self.SAS_VALUES["irrad"])

        # # Update the plotting on the measurement panel
        # measurement_panel = self.Parent.Parent.measurement_panel

        # vi_array = np.array(sas_curve[1]).astype(np.float)
        # p_array = vi_array[0] * vi_array[1]

        # # Update plots
        # for panel in [self, measurement_panel]:
        #     panel.vi_curve.set_data(vi_array[0], vi_array[1])
        #     panel.vi_axis.relim()
        #     panel.vi_axis.autoscale_view(True, True, True)

        #     panel.vp_curve.set_data(vi_array[0], p_array)
        #     panel.vp_axis.relim()
        #     panel.vp_axis.autoscale_view(True, True, True)

        #     panel.canvas.draw()

        self.select_table()
        self.select_table_mode()

    def sas_on(self):
        self.on()

    def sas_off(self):
        self.off()
