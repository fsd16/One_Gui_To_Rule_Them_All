import time
start_time = time.time()

import sys
import json
import smartside.signal as smartsignal


from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QErrorMessage, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QRadioButton, QFileDialog
from PySide6.QtCore import QTimer
from pyqtgraph import ViewBox, PlotCurveItem, ScatterPlotItem
from numpy import array

from ui.ui_One_Gui_To_Rule_Them_All import Ui_MainWindow
from ui.ui_Devices_Dialog import Ui_Dialog
from logic.ac_src import AC_SRC
from logic.scope import Scope
from logic.rlc import RLC
from logic.sas import SAS
from serial.serialutil import SerialException

import_time = time.time()
print(f"Import time: {import_time - start_time}")

# TODO: Tidy up GUI layout
# TODO: Auto import station
# TODO: Add loading screen
# TODO: Improve handling of pps and ametek
# TODO: Improve logging

RUN_EQUIPMENT = True

class Dialog(QDialog, Ui_Dialog, smartsignal.SmartSignal):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ac_device = None
        self.scope_device = None
        self.rlc_device = None
        self.sas_device = None
        self.startup = None

        self.setupUi(self)

        self.ac_entry_device.setText(config["ac"]["ac_entry_device"])
        self.scope_entry_device.setText(config["scope"]["scope_entry_device"])
        self.rlc_entry_device.setText(config["rlc"]["rlc_entry_device"])
        self.sas_entry_device.setText(config["sas"]["sas_entry_device"])
        self.device_entry_startup.setChecked(config["setup_devices"])

        self.auto_connect()

    _dialog_entries = 'ac_entry_device, scope_entry_device, rlc_entry_device, sas_entry_device'
    def _when_dialog_entries__editingFinished(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.text()
        
        if obj_name == "ac_entry_device":
            print(state)
            self.ac_device = state
        elif obj_name == "scope_entry_device":
            print(state)
            self.scope_device = state
        elif obj_name == "rlc_entry_device":
            print(state)
            self.rlc_device = state
        elif obj_name == "sas_entry_device":
            print(state)
            self.sas_device = state

    def _on_device_entry_startup__stateChanged(self):
        state = self.sender().isChecked()
        print (f"Startup behaviour set to: {state}")
        self.startup = state

class MainWindow(QMainWindow, Ui_MainWindow, smartsignal.SmartSignal): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setup_sas_plot()

        self.sas_timer = QTimer()
        self.sas_timer.setInterval(100)
        self.sas_timer.timeout.connect(self.sas_update_plot_pv)

        self.errorMsg = QErrorMessage()
        
        self.load_config()

        if self.c_config["setup_devices"]:
            self._on_main_action_devices__triggered()

        self.setup_equipment()
        
        if RUN_EQUIPMENT:
            self.ac_menu_abnormal.addItems(self.ac_src.AB_WAVEFORMS)
            self.ac_menu_phase.addItems(self.ac_src.PROFILES)
        
        self.auto_connect()
    
    def setup_equipment(self):
        if RUN_EQUIPMENT:
            try:
                self.ac_src = AC_SRC(self.c_config["ac"]["ac_entry_device"], "Ametek")
            except RuntimeError:
                self.ac_src = AC_SRC(self.c_config["ac"]["ac_entry_device"], "PPS")
            
            self.scope = Scope(self.c_config["scope"]["scope_entry_device"])
            rcc, split, pcc = self.c_config["rlc"]["rlc_entry_device"].partition(',')
            try:
                self.rlc = RLC(relay_controller_comport=rcc,
                            phase_controller_comport=pcc)
            except SerialException:
                self.rlc.close()
                self.rlc = RLC(relay_controller_comport=rcc,
                            phase_controller_comport=pcc)
            self.sas = SAS(self.c_config["sas"]["sas_entry_device"])
            print("Equipment is setup")

    def setup_sas_plot(self):
        self.sas_plot.setBackground('w')

        # Set up plot item
        plot = self.sas_plot.plotItem
        plot.showAxis('left')
        plot.showAxis('right')
        plot.setLabel(axis='left', text='Power', units='W')
        plot.setLabel(axis='right', text='Current', units='A')
        plot.invertY()

        # Set up view box
        self.left_vb = ViewBox(lockAspect=False)
        self.right_vb = ViewBox(lockAspect=False)

        plot.addItem(self.left_vb)
        plot.addItem(self.right_vb)

        plot.getAxis('left').linkToView(self.left_vb)
        plot.getAxis('right').linkToView(self.right_vb)

    def sas_plot_pvi(self, data):
        current = data["i"]
        voltage = data["v"]
        power = data["p"]
        left_curve = PlotCurveItem(voltage, power, pen='b')
        self.left_vb.addItem(left_curve)

        right_curve = PlotCurveItem(voltage, current, pen='r')
        self.right_vb.addItem(right_curve)

        self.left_vb.disableAutoRange()
        self.right_vb.disableAutoRange()

        self.pv_point = ScatterPlotItem()
        self.left_vb.addItem(self.pv_point)

    def sas_update_plot_pv(self):
        power, voltage = self.sas.get_sas_pv()
        # print(f"Power: {power}, Voltage: {voltage}")
        self.pv_point.clear()
        self.pv_point.addPoints(array([voltage]), array([power]), pen='g', symbol='o')

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

    def _on_main_action_reconnect__triggered(self):
        self.setup_equipment()

    def _on_main_action_devices__triggered(self):
        dlg = Dialog(self.c_config)
        dlg.exec()

        if QDialog.Accepted:
            if not dlg.ac_device == None:
                self.c_config["ac"]["ac_entry_device"] = dlg.ac_device
            if not dlg.scope_device == None:
                self.c_config["scope"]["scope_entry_device"] = dlg.scope_device
            if not dlg.rlc_device == None:
                self.c_config["rlc"]["rlc_entry_device"] = dlg.rlc_device
            if not dlg.sas_device == None:
                self.c_config["sas"]["sas_entry_device"] = dlg.sas_device
            if not dlg.startup == None:
                self.c_config["setup_devices"] = dlg.startup

    def _on_main_action_restore__triggered(self):
        print("Restore defaults triggered")
        self.force_update_ui(self.d_config)
    
    _closers = 'sas_butt_close, ac_butt_close, scope_butt_close, rlc_butt_close'
    def _when_closers__clicked(self):
        print("Close was clicked")
        self.sas_timer.stop()
        self.ac_butt_off.click()
        self.ac_src.return_manual()
        self.rlc_butt_off.click()
        self.sas_butt_off.click()

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
        if RUN_EQUIPMENT:
            self.ac_src.apply(self.c_config["ac"])
        
    def _on_ac_check_abnormal__stateChanged(self):
        state = self.sender().isChecked()
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

    def _on_scope_butt_browse__clicked(self):
        path = str(QFileDialog.getExistingDirectory())
        self.scope_line_cap_path.setText(path)
        print("Capture path entered:", path)
        self.c_config["scope"]["scope_line_cap_path"] = path

    
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
            self.sas_timer.start()

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
    app = QApplication(sys.argv)
    app_time = time.time()
    print(f"App time: {app_time - import_time}")
    window = MainWindow()
    window_time = time.time()
    print(f"MainWindow time: {window_time - app_time}")
    window.show()

    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()
