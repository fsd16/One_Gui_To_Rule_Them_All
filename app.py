import time
start_time = time.time()

import sys
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QErrorMessage, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QRadioButton, QFileDialog, QProgressDialog 
from PySide6.QtCore import QTimer, Qt
from pyqtgraph import ViewBox, PlotCurveItem, ScatterPlotItem
from numpy import array

from ui.ui_One_Gui_To_Rule_Them_All import Ui_MainWindow
from ui.ui_Devices_Dialog import Ui_DevicesDialog
from ui.ui_Loading_Dialog import Ui_LoadingDialog
from logic.ac_src import AC_SRC
from logic.scope import Scope
from logic.rlc import RLC
from logic.sas import SAS
from logic.signal import SmartSignal
from serial.serialutil import SerialException
from pyvisa.errors import VisaIOError
from typing import Dict, Any, TypeVar
KeyType = TypeVar('KeyType')

import_time = time.time()
print(f"Import time: {import_time - start_time}")

# TODO: Auto import station
# TODO: Improve handling of pps and ametek
# TODO: Save and recall scope setups from gui
# TODO: After autocapture stops, return the scope to the mode it was in before autocapture was started (or just to run mode)
# TODO: Issue where abnormal waveforms location is hardcoded to a bench
# TODO: Allow startup with only selected equipment
# TODO: Add sas cluster support

RUN_EQUIPMENT = True

#--------------------------------------------------------
#                   Loading Dialog                      #
#--------------------------------------------------------
class LoadingDialog(QDialog, Ui_LoadingDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

    def set_progress(self, value):
        self.progressBar.setValue(value)

#--------------------------------------------------------
#                   Devices Dialog                      #
#--------------------------------------------------------
class DevicesDialog(QDialog, Ui_DevicesDialog, SmartSignal):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ac_device = None
        self.scope_device = None
        self.rlc_device = None
        self.sas_device = None
        self.startup = None
        self.sas_config = None

        self.sas_configs = {
            "Series":   "series",
            "Parallel": "parallel"
        }
        
        self.setupUi(self)
        self.sas_menu_config.addItems(self.sas_configs)

        self.ac_entry_device.setText(config["ac"]["ac_entry_device"])
        self.scope_entry_device.setText(config["scope"]["scope_entry_device"])
        self.rlc_entry_device.setText(config["rlc"]["rlc_entry_device"])
        self.sas_entry_device.setText(config["sas"]["sas_entry_device"])
        sas_config_index = list(self.sas_configs.values()).index(config["sas"]["sas_menu_config"])
        self.sas_menu_config.setCurrentIndex(sas_config_index)
        self.device_entry_startup.setChecked(config["setup_devices"])

        self.auto_connect()

    _dialog_entries = 'ac_entry_device, scope_entry_device, rlc_entry_device, sas_entry_device'
    def _when_dialog_entries__editingFinished(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.text()
        
        if obj_name == "ac_entry_device":
            print(f"AC Source: {state}")
            self.ac_device = state
        elif obj_name == "scope_entry_device":
            print(f"Scope: {state}")
            self.scope_device = state
        elif obj_name == "rlc_entry_device":
            print(f"RLCe: {state}")
            self.rlc_device = state
        elif obj_name == "sas_entry_device":
            print(f"SAS: {state}")
            self.sas_device = state
    
    _dialog_menus = 'sas_menu_config'
    def _when_dialog_menus__activated(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.currentText()

        if obj_name == "sas_menu_config":
            print(f"SAS config selected: {state}")
            self.sas_config = self.sas_configs[state]

    def _on_device_entry_startup__stateChanged(self):
        state = self.sender().isChecked()
        print (f"Startup behaviour checked: {state}")
        self.startup = state

#--------------------------------------------------------
#                   Main Window                         #
#--------------------------------------------------------
class MainWindow(QMainWindow, Ui_MainWindow, SmartSignal): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setup_sas_plot()

        self.sas_timer = QTimer()
        self.sas_timer.setInterval(100)
        self.sas_timer.timeout.connect(self.sas_update_plot_pv)

        self.error_msg = QErrorMessage()
        self.error_msg.setWindowModality(Qt.ApplicationModal)

        self.load_config()

        if self.l_config["setup_devices"]:
            self._on_main_action_devices__triggered()

        self._on_main_action_connect__triggered()
            
        self.auto_connect()

    #--------------------------------------------------------
    #                       Helpers                         #
    #--------------------------------------------------------
    def deep_update(self, mapping: Dict[KeyType, Any], *updating_mappings: Dict[KeyType, Any]) -> Dict[KeyType, Any]:
        updated_mapping = mapping.copy()
        for updating_mapping in updating_mappings:
            for k, v in updating_mapping.items():
                if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
                    updated_mapping[k] = self.deep_update(updated_mapping[k], v)
                else:
                    updated_mapping[k] = v

        return updated_mapping

    def setup_equipment(self):
        if RUN_EQUIPMENT:
            loading_dlg = LoadingDialog()
            loading_dlg.set_progress(0)
            loading_dlg.show()
            QApplication.processEvents()

            try:
                self.ac_src = AC_SRC(self.l_config["ac"]["ac_entry_device"], "Ametek")
            except RuntimeError:
                self.ac_src = AC_SRC(self.l_config["ac"]["ac_entry_device"], "PPS")
            self.ac_menu_abnormal.addItems(self.ac_src.AB_WAVEFORMS)
            self.ac_menu_profile.addItems(self.ac_src.PROFILES)
            print("AC Source configured")
            loading_dlg.set_progress(25)
            QApplication.processEvents()
            
            self.scope = Scope(self.l_config["scope"]["scope_entry_device"])
            print("Scope configured")
            loading_dlg.set_progress(50)
            QApplication.processEvents()

            rcc, pcc, *trash = tuple([x.strip() for x in self.l_config["rlc"]["rlc_entry_device"].split(',')])
            try:
                self.rlc = RLC(relay_controller_comport=rcc,
                            phase_controller_comport=pcc)
            except SerialException:
                self.rlc.close()
                self.rlc = RLC(relay_controller_comport=rcc,
                            phase_controller_comport=pcc)
                
            print("RLC configured")
            loading_dlg.set_progress(75)
            QApplication.processEvents()

            sas_addresses = [x.strip() for x in self.l_config["sas"]["sas_entry_device"].split(',')]
            self.sas = SAS(sas_addresses, self.l_config["sas"]["sas_menu_config"])
            print(self.l_config["sas"]["sas_menu_config"])
            print("SAS configured")
            loading_dlg.set_progress(100)
            QApplication.processEvents()
            loading_dlg.close()
            print("Equipment setup complete")

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
        
        self.left_vb.disableAutoRange()
        self.right_vb.disableAutoRange()

        plot.addItem(self.left_vb)
        plot.addItem(self.right_vb)

        plot.getAxis('left').linkToView(self.left_vb)
        plot.getAxis('right').linkToView(self.right_vb)

    def sas_plot_pvi(self, data):
        current = data["i"]
        voltage = data["v"]
        power = data["p"]
        left_curve = PlotCurveItem(voltage, power, pen='b')
        self.left_vb.clear()
        self.left_vb.addItem(left_curve)

        right_curve = PlotCurveItem(voltage, current, pen='r')
        self.right_vb.clear()
        self.right_vb.addItem(right_curve)

        self.left_vb.autoRange()
        self.right_vb.autoRange()

        self.pv_point = ScatterPlotItem()
        self.pv_point.clear()
        self.left_vb.addItem(self.pv_point)

    def sas_update_plot_pv(self):
        power, voltage = self.sas.get_sas_pv()
        # print(f"Power: {power}, Voltage: {voltage}")
        self.pv_point.clear()
        self.pv_point.addPoints(array([voltage]), array([power]), pen='g', symbol='o')

    def rlc_auto_update_params(self):
        if self.rlc_check_auto.isChecked():
            self.rlc_entry_ac_volts.setValue(self.l_config["ac"]["ac_entry_ac_volts"])
            self.rlc_entry_freq.setValue(self.l_config["ac"]["ac_entry_freq"])
            self.rlc_entry_reactive_pwr.setValue(0)
            self.rlc_entry_real_pwr.setValue(self.l_config["sas"]["sas_entry_pmp"])
            if RUN_EQUIPMENT:
                rlc_config = self.rlc.turn_on(self.l_config["rlc"])
                self.l_config["rlc"].update(rlc_config)

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
    
    def load_config(self):

        with open("config/config.json", "r") as jsonfile:
            self.d_config = json.load(jsonfile)

        try:
            with open("config/local_config.json", "r") as jsonfile:
                self.l_config = json.load(jsonfile)
        except IOError:
            self.l_config = self.d_config
        
        self.l_config = self.deep_update(self.d_config, self.l_config)

        self.force_update_ui(self.l_config)
        print("Config loaded")

    #--------------------------------------------------------
    #                       Main Items                      #
    #--------------------------------------------------------
    def _on_main_action_connect__triggered(self):
        print("Equipment connect triggered")
        try:
            if RUN_EQUIPMENT:
                self.setup_equipment()
        except VisaIOError:
            self.error_msg.setWindowTitle("Connection failed")
            self.error_msg.showMessage("Ensure equipment is on and address is correct<br/>Retry connection:<br/>(Options->Reconnect Equipment)")
            self.error_msg.exec()

    def _on_main_action_devices__triggered(self):
        print("Device setup triggered")
        dlg = DevicesDialog(self.l_config)
        dlg.exec()

        if QDialog.Accepted:
            if not dlg.ac_device == None:
                self.l_config["ac"]["ac_entry_device"] = dlg.ac_device
            if not dlg.scope_device == None:
                self.l_config["scope"]["scope_entry_device"] = dlg.scope_device
            if not dlg.rlc_device == None:
                self.l_config["rlc"]["rlc_entry_device"] = dlg.rlc_device
            if not dlg.sas_device == None:
                self.l_config["sas"]["sas_entry_device"] = dlg.sas_device
            if not dlg.sas_config == None:
                self.l_config["sas"]["sas_menu_config"] = dlg.sas_config
            if not dlg.startup == None:
                self.l_config["setup_devices"] = dlg.startup

    def _on_main_action_restore__triggered(self):
        print("Restore defaults triggered")
        self.force_update_ui(self.d_config)
    
    def closeEvent(self, event):
        self._when_closers__clicked()

        if True:
            event.accept() # let the window close
        else:
            event.ignore()

    _closers = 'sas_butt_close, ac_butt_close, scope_butt_close, rlc_butt_close'
    def _when_closers__clicked(self):
        print("Close clicked")
        self.hide()
        try:
            self.ac_src.turn_off()
            self.ac_src.return_manual()
            self.sas.turn_off()
            self.rlc.close()
            # self.rlc.turn_off()
            self.scope.turn_off()

            print("Equipment turned off")

            # save config
            with open("config/local_config.json", "w") as jsonfile:
                json.dump(self.l_config, jsonfile)

            print("Config saved")

        except AttributeError:
            pass

        sys.exit()

    #--------------------------------------------------------
    #                       AC Tab                          #
    #--------------------------------------------------------
    _ac_buttons = 'ac_butt_apply, ac_butt_off, ac_butt_on'
    def _when_ac_buttons__clicked(self):
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "ac_butt_apply":
            print("Apply clicked")
            if RUN_EQUIPMENT:
                self.ac_src.apply(self.l_config["ac"])
            self.rlc_auto_update_params()
        elif obj_name == "ac_butt_on":
            print("AC on clicked")
            if RUN_EQUIPMENT:
                self.ac_src.turn_on()
        elif obj_name == "ac_butt_off":
            print("AC off clicked")
            if RUN_EQUIPMENT:
                self.ac_src.turn_off()
        
    def _on_ac_check_abnormal__stateChanged(self):
        state = self.sender().isChecked()
        print (f"Abnormal checked: {state}")
        self.l_config["ac"]["ac_check_abnormal"] = state

    _ac_entries = 'ac_entry_step_size, ac_entry_freq, ac_entry_ac_volts'
    def _when_ac_entries__valueChanged(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()

        self.l_config["ac"][obj_name] = state

        if obj_name == "ac_entry_step_size":
            print(f"Step size entered: {state}")
        elif obj_name == "ac_entry_freq":
            print(f"Frequency entered: {state}")
        elif obj_name == "ac_entry_ac_volts":
            print(f"Ac Volts entered: {state}")

    _ac_menus = 'ac_menu_abnormal, ac_menu_profile'
    def _when_ac_menus__activated(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.currentText()

        self.l_config["ac"][obj_name] = state

        if obj_name == "ac_menu_abnormal":
            print(f"Abnormal waveform selected: {state}")
        elif obj_name == "ac_menu_profile":
            print(f"Profile selected: {state}")
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

    _ac_radios = 'ac_radio_single, ac_radio_split, ac_radio_three'
    def _when_ac_radios__toggled(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["ac"][obj_name] = state

        if obj_name == "ac_radio_single" and state:
            print("Single selected")
        elif obj_name == "ac_radio_split" and state:
            print("Split selected")
        elif obj_name == "ac_radio_three" and state:
            print("Three selected")

    #--------------------------------------------------------
    #                       RLC Tab                         #
    #--------------------------------------------------------
    _rlc_buttons = 'rlc_butt_off, rlc_butt_on'
    def _when_rlc_buttons__clicked(self):
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "rlc_butt_off":
            print("RLC off clicked")
            if RUN_EQUIPMENT:
                self.rlc.turn_off()
        elif obj_name == "rlc_butt_on":
            print("RLC on clicked")
            rlc_config = self.l_config["rlc"]
            try:
                if RUN_EQUIPMENT:
                    self.rlc.turn_on(rlc_config)
            except self.rlc.NoInput:
                self.error_msg.setWindowTitle("No Inputs")
                self.error_msg.showMessage("Why do I even exist?")
            except self.rlc.VoltageInvalid:
                self.error_msg.setWindowTitle("Voltage Invalid")
                self.error_msg.showMessage("Need to specify voltage")
            except self.rlc.PowerInvalid:
                self.error_msg.setWindowTitle("Power Invalid")
                self.error_msg.showMessage("Need to specify real and/or reactive power")
            except self.rlc.FrequencyInvalid:
                self.error_msg.setWindowTitle("Frequency Invalid")
                self.error_msg.showMessage("Need to specify frequency with reactive power")

    _rlc_entries = 'rlc_entry_ac_volts, rlc_entry_freq, rlc_entry_reactive_pwr, rlc_entry_real_pwr'
    def _when_rlc_entries__valueChanged(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()

        self.l_config["rlc"][obj_name] = state

        if obj_name == "rlc_entry_ac_volts":
            print(f"Ac Volts entered: {state}")
        elif obj_name == "rlc_entry_freq":
            print(f"Frequency entered: {state}")
        elif obj_name == "rlc_entry_reactive_pwr":
            print(f"Reactive power entered: {state}")
        elif obj_name == "rlc_entry_real_pwr":
            print(f"Real power entered: {state}")

    _rlc_checks = 'rlc_check_auto'
    def _when_rlc_checks__stateChanged(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["rlc"][obj_name] = state

        if obj_name == "rlc_check_auto":
            print (f"Auto set RLC parameters checked: {state}")
            if state:
                self.rlc_entry_ac_volts.setValue(self.l_config["ac"]["ac_entry_ac_volts"])
                self.rlc_entry_freq.setValue(self.l_config["ac"]["ac_entry_freq"])
                self.rlc_entry_reactive_pwr.setValue(0)
                self.rlc_entry_real_pwr.setValue(self.l_config["sas"]["sas_entry_pmp"])
                self.rlc_entry_ac_volts.setDisabled(True)
                self.rlc_entry_freq.setDisabled(True)
                self.rlc_entry_reactive_pwr.setDisabled(True)
                self.rlc_entry_real_pwr.setDisabled(True)
                self.rlc_butt_on.setDisabled(True)
                self.rlc_butt_off.setDisabled(True)
            else:
                self.rlc_entry_ac_volts.setDisabled(False)
                self.rlc_entry_freq.setDisabled(False)
                self.rlc_entry_reactive_pwr.setDisabled(False)
                self.rlc_entry_real_pwr.setDisabled(False)
                self.rlc_butt_on.setDisabled(False)
                self.rlc_butt_off.setDisabled(False)
    
    _rlc_auto_check_entries = 'ac_entry_ac_volts, ac_entry_freq, sas_entry_pmp'
    def _when_rlc_auto_check_entries__valueChanged(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()

        if self.rlc_check_auto.isChecked():
            if obj_name == "ac_entry_ac_volts":
                self.rlc_entry_ac_volts.setValue(state)
            elif obj_name == "ac_entry_freq":
                self.rlc_entry_freq.setValue(state)
            elif obj_name == "sas_entry_pmp":
                self.rlc_entry_real_pwr.setValue(state)

    _rlc_auto_check_applies = 'ac_butt_apply'
    def _when_rlc_auto_checks__clicked(self):
        obj = self.sender()
        obj_name = obj.objectName()

        if self.rlc_check_auto.isChecked():
            if obj_name == "ac_butt_apply":
                if RUN_EQUIPMENT:
                        rlc_config = self.rlc.turn_on(rlc_config)
                        self.l_config["rlc"].update(rlc_config)

    #--------------------------------------------------------
    #                       SAS Tab                         #
    #--------------------------------------------------------
    _sas_buttons = 'sas_butt_off, sas_butt_on, sas_butt_apply'
    def _when_sas_buttons__clicked(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.text()

        if obj_name == "sas_butt_off":
            print("SAS off clicked")
            if RUN_EQUIPMENT:
                self.sas.turn_off()
        elif obj_name == "sas_butt_on":
            print("SAS on clicked")
            if RUN_EQUIPMENT:
                self.sas.turn_on()
        elif obj_name == "sas_butt_apply":
            print("Apply clicked")
            if RUN_EQUIPMENT:
                sas_data =  self.sas.apply(self.l_config["sas"])
                self.sas_plot_pvi(sas_data)
                self.sas_timer.start()
            self.rlc_auto_update_params()

    _sas_entries = 'sas_entry_vmp, sas_entry_pmp, sas_entry_ff, sas_entry_irrad'
    def _when_sas_entries__editingFinished(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()

        self.l_config["sas"][obj_name] = state
        
        if obj_name == "sas_entry_vmp":
            print(f"Vmp entered: {state}")
        elif obj_name == "sas_entry_pmp":
            print(f"Pmp entered: {state}")
        elif obj_name == "sas_entry_ff":
            print(f"Fill Factor entered: {state}")
        elif obj_name == "sas_entry_irrad":
            print(f"Irradiance entered: {state}")

    #--------------------------------------------------------
    #                       Scope Tab                       #
    #--------------------------------------------------------
    _scope_buttons = 'scope_butt_cap, scope_butt_apply, scope_butt_browse'
    def _when_scope_buttons__clicked(self):
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "scope_butt_cap":
            print("Capture clicked")
            if RUN_EQUIPMENT:
                self.scope.capture_display(self.l_config["scope"])
        elif obj_name == "scope_butt_apply":
            print("Apply labels clicked")
            if RUN_EQUIPMENT:
                self.scope.label(self.l_config["scope"])
        elif obj_name == "scope_butt_browse":
            path = str(QFileDialog.getExistingDirectory())
            self.scope_line_cap_path.setText(path)
            print(f"Capture path entered: {path}")
            self.l_config["scope"][obj_name] = path
        
    _scope_checks = 'scope_check_auto, scope_check_date, scope_check_invert'
    def _when_scope_checks__stateChanged(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["scope"][obj_name] = state

        if obj_name == "scope_check_auto":
            print (f"Auto capture checked: {state}")
            if state:
                if RUN_EQUIPMENT:    
                    self.scope.auto_capture_on(self.l_config["scope"])
            else:
                if RUN_EQUIPMENT:
                    self.scope.auto_capture_off()
        elif obj_name == "scope_check_date":
            print (f"Date checked: {state}")
        elif obj_name == "scope_check_invert":
            print (f"Invert checked: {state}")
    
    _scope_entries = 'scope_line_cap_name, scope_line_cap_path, scope_line_ch1_lab, scope_line_ch2_lab, scope_line_ch3_lab, scope_line_ch4_lab'
    def _when_scope_entries__editingFinished(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.text()
        
        self.l_config["scope"][obj_name] = state

        if obj_name == "scope_line_cap_name":
            print(f"Capture name entered: {state}")
        elif obj_name == "scope_line_cap_path":
            print(f"Capture path entered: {state}")
        elif obj_name == "scope_line_ch1_lab":
            print(f"CH1 label entered: {state}")
        elif obj_name == "scope_line_ch2_lab":
            print(f"CH2 label entered: {state}")
        elif obj_name == "scope_line_ch3_lab":
            print(f"CH3 label entered: {state}")
        elif obj_name == "scope_line_ch4_lab":
            print(f"CH4 label entered: {state}")

def main():
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
