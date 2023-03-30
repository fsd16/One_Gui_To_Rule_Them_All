import sys
import json
import smartside.signal as smartsignal
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QErrorMessage, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QRadioButton, QComboBox
from PySide6 import QtCore
from pydantic.utils import deep_update
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt

from ui.ui_One_Gui_To_Rule_Them_All import Ui_MainWindow
from logic.ac_src import AC_SRC
from logic.scope import Scope
from logic.rlc import RLC
from logic.sas import SAS

from threading import Thread


RUN_EQUIPMENT = True


class GlobalObject(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self._events = {}

    def addEventListener(self, name, func):
        if name not in self._events:
            self._events[name] = [func]
        else:
            self._events[name].append(func)

    def dispatchEvent(self, name):
        functions = self._events.get(name, [])
        for func in functions:
            QtCore.QTimer.singleShot(0, func)

class MainWindow(QMainWindow, Ui_MainWindow, smartsignal.SmartSignal): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setup_sas_plot()

        # GlobalObject().addEventListener("sas_update_pi", self.sas_update_plot_pi)

        # figure out how to dispatch when a measurment is gathered
        # GlobalObject().dispatchEvent("sas_update_pi")

        self.errorMsg = QErrorMessage()
        if RUN_EQUIPMENT:
            self.ac_src = AC_SRC("GPIB0::1::INSTR")
            self.scope = Scope("GPIB0::28::INSTR")
            self.rlc = RLC(relay_controller_comport='COM3',
                        phase_controller_comport='COM4')
            self.sas = SAS("GPIB0::15::INSTR")

        self.load_config()
        
        if RUN_EQUIPMENT:
            self.ac_menu_abnormal.addItems(self.ac_src.AB_WAVEFORMS)
            self.ac_menu_phase.addItems(self.ac_src.PROFILES)
        
        self.auto_connect()
    
    def setup_sas_plot(self):
        self.sas_plot.setBackground('w')

        # Set up plot item
        plot = self.sas_plot.plotItem
        plot.showAxis('left')
        plot.showAxis('right')
        plot.setLabel(axis='left', text='Power', units='W')
        plot.setLabel(axis='right', text='Voltage', units='V')
        plot.invertY()

        # Set up view box
        self.left_vb = pg.ViewBox(lockAspect=False)
        self.right_vb = pg.ViewBox(lockAspect=False)

        plot.addItem(self.left_vb)
        plot.addItem(self.right_vb)

        plot.getAxis('left').linkToView(self.left_vb)
        plot.getAxis('right').linkToView(self.right_vb)

    def sas_plot_pvi(self, data):
        current = data["i"]
        voltage = data["v"]*10 # *10 is a fudge factor, really don't understand I have to use it...
        power = data["p"]
        left_curve = pg.PlotCurveItem(current, power, pen='r')
        self.left_vb.addItem(left_curve)

        right_curve = pg.PlotCurveItem(current, voltage, pen='b')
        self.right_vb.addItem(right_curve)

    def sas_update_plot_pi(self):
        current = np.array([self.sas.measured_pi["i"]])
        power = np.array([self.sas.measured_pi["p"]])
        print(current)
        print(power)
        left_curve = pg.ScatterPlotItem(current, power, symbol='o')
        self.left_vb.addItem(left_curve)

    def force_update_ui(self, config):
        children = []
        children += self.findChildren(QSpinBox)
        children += self.findChildren(QDoubleSpinBox)
        
        for child in children:
            name = child.objectName()
            if not name.startswith('qt_'):
                prefix, sep, rest = name.partition('_')
                # object_names.append((name, prefix))

                wgtobj = getattr(self, name)
                if hasattr(wgtobj, "setValue"):
                    wgtobj.setValue(config[prefix][name])
                
        children = []
        children += self.findChildren(QLineEdit)
        
        for child in children:
            name = child.objectName()
            if not name.startswith('qt_'):
                prefix, sep, rest = name.partition('_')
                # object_names.append((name, prefix))

                wgtobj = getattr(self, name)
                if hasattr(wgtobj, "setText"):
                    wgtobj.setText(config[prefix][name])
        
        children = []
        children += self.findChildren(QCheckBox)
        children += self.findChildren(QRadioButton)
        
        for child in children:
            name = child.objectName()
            if not name.startswith('qt_'):
                prefix, sep, rest = name.partition('_')
                # object_names.append((name, prefix))

                wgtobj = getattr(self, name)
                if hasattr(wgtobj, "setChecked"):
                    wgtobj.setChecked(config[prefix][name])
                    
        # Setting Menu may overide current values if they are different from the presets
        # children = []
        # children += self.findChildren(QComboBox)
    
    def load_config(self):

        with open("config.json", "r") as jsonfile:
            self.config = json.load(jsonfile)
        self.c_config = self.config["current"]
        self.d_config = self.config["default"]
        self.force_update_ui(self.c_config)
        
        print("Config loaded")

    def _on_main_action_restore__triggered(self):
        print("Restore defaults triggered")
        self.force_update_ui(self.d_config)
    
    _closers = 'sas_butt_close, ac_butt_close, scope_butt_close, rlc_butt_close'
    def _when_closers__clicked(self):
        print("Close was clicked")

        # save config
        with open("config.json", "w") as jsonfile:
            json.dump(self.config, jsonfile)
        print("Config saved")

        sys.exit()
    
    # AC Tab
    def _on_ac_butt_off__clicked(self):
        print("AC off was clicked")
        if RUN_EQUIPMENT:
            self.ac_src.turn_off()
    
    def _on_ac_butt_on__clicked(self):
        print("AC on was clicked")
        if RUN_EQUIPMENT:
            self.ac_src.turn_on()
        
    def _on_ac_butt_apply__clicked(self):
        print("Apply was clicked")
        
        if self.c_config["ac"]["ac_check_abnormal"]:
            if RUN_EQUIPMENT:
                self.ac_src.apply_abnormal(self.c_config["ac"])
        else:
            if RUN_EQUIPMENT:
                self.ac_src.apply(self.c_config["ac"])
        
    def _on_ac_check_abnormal__stateChanged(self):
        state = self.sender().value()
        print ('Abnormal was checked', state)
        self.c_config["ac"]["ac_check_abnormal"] = state

    def _on_ac_entry_ac_volts__valueChanged(self):
        state = self.sender().value()
        print("Ac Volts entered:", state)
        self.c_config["ac"]["ac_entry_ac_volts"] = state

    def _on_ac_entry_freq__valueChanged(self):
        state = self.sender().value()
        print("Frequency entered:", state)
        self.c_config["ac"]["ac_entry_freq"] = state
        
    def _on_ac_entry_step_size__valueChanged(self):
        state = self.sender().value()
        print("Step size entered:", state)
        self.c_config["ac"]["ac_entry_step_size"] = state
    
    def _on_ac_menu_abnormal__activated(self):
        state = self.sender().currentText()
        print("Abnormal waveform selected:", state)
        self.c_config["ac"]["ac_manu_abnormal"] = state
        
    def _on_ac_menu_phase__activated(self):
        state = self.sender().currentText()
        print("Profile selected:", state)
        # self.ac_src.set_ac_profile(self.sender().currentText())
        if RUN_EQUIPMENT:
            profile = self.ac_src.PROFILES[state]
        self.ac_entry_ac_volts.setValue(profile[0])
        self.ac_entry_freq.setValue(profile[1])
        
        if profile[2] == "split":
            self.ac_radio_split.setChecked(True)
        elif profile[2] == "single":
            self.ac_radio_single.setChecked(True)
        elif profile[2] == "three":
            self.ac_radio_three.setChecked(True)

    def _on_ac_radio_single__toggled(self):
        self.c_config["ac"]["ac_radio_single"] = self.ac_radio_single.isChecked()
        if self.c_config["ac"]["ac_radio_single"]:
            print("Single is selected")
            
            
    def _on_ac_radio_split__toggled(self):
        self.c_config["ac"]["ac_radio_split"] = self.ac_radio_split.isChecked()
        if self.c_config["ac"]["ac_radio_split"]:
            print("Split is selected")
            
    def _on_ac_radio_three__toggled(self):
        self.c_config["ac"]["ac_radio_three"] = self.ac_radio_three.isChecked()
        if self.c_config["ac"]["ac_radio_three"]:
            print("Three is selected")
        
    # Scope tab
    def _on_scope_butt_apply__clicked(self):
        print("Apply labels was clicked")
        if RUN_EQUIPMENT:
            self.scope.label(self.c_config["scope"])
    
    def _on_scope_butt_cap__clicked(self):
        print("Capture was clicked")
        if RUN_EQUIPMENT:
            self.scope.capture_display(self.c_config["scope"])
        
    def _on_scope_check_auto__stateChanged(self):
        state = self.sender().isChecked()
        print ('Check is', state)
        self.c_config["scope"]["scope_check_auto"] = state
        if state:
            if RUN_EQUIPMENT:    
                self.scope.auto_capture_on(self.c_config["scope"])
        else:
            if RUN_EQUIPMENT:
                self.scope.auto_capture_off()
        
    def _on_scope_check_date__stateChanged(self):
        state = self.sender().isChecked()
        print ('Check is', state)
        self.c_config["scope"]["scope_check_date"] = state
        
    def _on_scope_check_invert__stateChanged(self):
        state = self.sender().isChecked()
        print ('Check is', state)
        self.c_config["scope"]["scope_check_invert"] = state
        
    def _on_scope_line_cap_name__editingFinished(self):
        state = self.sender().text()
        print("Capture name entered:", state)
        self.c_config["scope"]["scope_line_cap_name"] = state
        
    def _on_scope_line_cap_path__editingFinished(self):
        state = self.sender().text()
        print("Capture path entered:", state)
        self.c_config["scope"]["scope_line_cap_path"] = state
    
    def _on_scope_line_ch1_lab__editingFinished(self):
        state = self.sender().text()
        print("CH1 label entered:", state)
        self.c_config["scope"]["scope_line_ch1_lab"] = state
        
    def _on_scope_line_ch2_lab__editingFinished(self):
        state = self.sender().text()
        print("CH2 label entered:", state)
        self.c_config["scope"]["scope_line_ch2_lab"] = state
        
    def _on_scope_line_ch3_lab__editingFinished(self):
        state = self.sender().text()
        print("CH3 label entered:", state)
        self.c_config["scope"]["scope_line_ch3_lab"] = state
        
    def _on_scope_line_ch4_lab__editingFinished(self):
        state = self.sender().text()
        print("CH4 label entered:", state)
        self.c_config["scope"]["scope_line_ch4_lab"] = state
        
    # RLC tab
    def _on_rlc_butt_off__clicked(self):
        print("RLC off was clicked")
        if RUN_EQUIPMENT:
            self.rlc.turn_off()
    
    def _on_rlc_butt_on__clicked(self):
        print("RLC on was clicked")

        rlc_config = self.c_config["rlc"]

        try:
            if RUN_EQUIPMENT:
                rlc_config = self.rlc.turn_on(rlc_config)
            self.c_config["rlc"].update(rlc_config)
            # self.rlc_entry_real_pwr.setValue(round(self.rlc.SETTINGS["real_pwr"]))
            # self.rlc_entry_reactive_pwr.setValue(round(self.rlc.SETTINGS["reactive_pwr"]))
        except self.rlc.NoInput:
            self.errorMsg.showMessage("Why do I even exist?")
        except self.rlc.VoltageInvalid:
            self.errorMsg.showMessage("Need to specify voltage")
        except self.rlc.PowerInvalid:
            self.errorMsg.showMessage("Need to specify real and/or reactive power")
        except self.rlc.FrequencyInvalid:
            self.errorMsg.showMessage("Need to specify frequency with reactive power")

    def _on_rlc_entry_ac_volts__valueChanged(self):
        state = self.sender().value()
        print("Ac Volts entered:", state)
        self.c_config["rlc"]["rlc_entry_ac_volts"] = state

    def _on_rlc_entry_freq__valueChanged(self):
        state = self.sender().value()
        print("Frequency entered:", state)
        self.c_config["rlc"]["rlc_entry_freq"] = state

    def _on_rlc_entry_reactive_pwr__valueChanged(self):
        state = self.sender().value()
        print("Reactive power entered:", state)
        self.c_config["rlc"]["rlc_entry_reactive_pwr"] = state

    def _on_rlc_entry_real_pwr__valueChanged(self):
        state = self.sender().value()
        print("Real power entered:", state)
        self.c_config["rlc"]["rlc_entry_real_pwr"] = state

    # SAS tab
    def _on_sas_butt_off__clicked(self):
        print("SAS off was clicked")
        if RUN_EQUIPMENT:
            self.sas.turn_off()
    
    def _on_sas_butt_on__clicked(self):
        print("SAS on was clicked")
        if RUN_EQUIPMENT:
            self.sas.turn_on()

        
    def _on_sas_butt_apply__clicked(self):
        print("Apply was clicked")
        if RUN_EQUIPMENT:
            sas_data =  self.sas.apply(self.c_config["sas"])
            self.sas_plot_pvi(sas_data)
            self.sas_update_plot_pi()

    def _on_sas_entry_irrad__valueChanged(self):
        state = self.sender().value()
        print("Irradiance entered:", state)
        self.c_config["sas"]["sas_entry_irrad"] = state

    def _on_sas_entry_ff__valueChanged(self):
        state = self.sender().value()
        print("Fill Factor entered:", state)
        self.c_config["sas"]["sas_entry_ff"] = state

    def _on_sas_entry_pmp__valueChanged(self):
        state = self.sender().value()
        print("Pmp entered:", state)
        self.c_config["sas"]["sas_entry_pmp"] = state

    def _on_sas_entry_vmp__valueChanged(self):
        state = self.sender().value()
        print("Vmp entered:", state)
        self.c_config["sas"]["sas_entry_vmp"] = state


def main():
    # This call takes foooooreeeeeever.....
    start_time = time.time()
    app = QApplication(sys.argv)
    app_time = time.time()
    print(f"App time: {app_time - start_time}")
    window = MainWindow()
    window_time = time.time()
    print(f"App time: {window_time - app_time}")
    window.show()

    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()
