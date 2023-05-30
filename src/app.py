import time
start_time = time.time()

import sys
import json
import logging


from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QErrorMessage, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QRadioButton, QFileDialog, QProgressDialog 
from PySide6.QtCore import QTimer, Qt
from pyqtgraph import ViewBox, PlotCurveItem, ScatterPlotItem
from numpy import array

from ui.One_GUI_To_Rule_Them_All_ui import Ui_MainWindow
from ui.Devices_Dialog_ui import Ui_DevicesDialog
from ui.Loading_Dialog_ui import Ui_LoadingDialog
from logic.ac_src import AC_SRC
from logic.scope import Scope
from logic.rlc import RLC
from logic.sas import SAS
from logic.signal import SmartSignal
from logic.equipment_library import EquipmentDrivers
from logic.utils import dict_value_to_index, deep_update
from serial.serialutil import SerialException
from pyvisa.errors import VisaIOError
from pathlib import Path

import_time = time.time()
print(f"Import time: {import_time - start_time}")

# TODO: Auto import station
# TODO: Save and recall scope setups from gui
# TODO: After autocapture stops, return the scope to the mode it was in before autocapture was started (or just to run mode)
# TODO: Some serious commenting is needed

RUN_EQUIPMENT = True

# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Dummy:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, *args, **kwargs):
        return self

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
        super().__init__()
        self.drivers = EquipmentDrivers()

        self.config = config

        self.sas_configs = {
            "Series":   "series",
            "Parallel": "parallel"
        }

        self.setupUi(self)
        
        self.ac_menu_driver.addItems(self.drivers.AC_SOURCE_DRIVERS)
        self.scope_menu_driver.addItems(self.drivers.SCOPE_DRIVERS)
        self.rlc_menu_driver.addItems(self.drivers.RLC_DRIVERS)
        self.sas_menu_driver.addItems(self.drivers.SAS_DRIVERS)
        
        self.sas_menu_config.addItems(self.sas_configs)

        self.ac_entry_address.setText(config["ac"]["ac_entry_address"])
        self.scope_entry_address.setText(config["scope"]["scope_entry_address"])
        self.rlc_entry_address.setText(config["rlc"]["rlc_entry_address"])
        self.sas_entry_address.setText(config["sas"]["sas_entry_address"])

        self.sas_menu_config.setCurrentIndex(config["sas"]["sas_menu_config"]["index"])
        self.ac_menu_driver.setCurrentIndex(config["ac"]["ac_menu_driver"]["index"])
        self.scope_menu_driver.setCurrentIndex(config["scope"]["scope_menu_driver"]["index"])
        self.rlc_menu_driver.setCurrentIndex(config["rlc"]["rlc_menu_driver"]["index"])
        self.sas_menu_driver.setCurrentIndex(config["sas"]["sas_menu_driver"]["index"])

        self.device_entry_startup.setChecked(config["setup_devices"])

        self.auto_connect()

    _dialog_entries = 'ac_entry_address, scope_entry_address, rlc_entry_address, sas_entry_address'
    def _when_dialog_entries__editingFinished(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.text()

        prefix = obj_name.split('_')[0]
        self.config[prefix][obj_name] = state

        if obj_name == "ac_entry_address":
            print(f"AC Source: {state}")
        elif obj_name == "scope_entry_address":
            print(f"Scope: {state}")
        elif obj_name == "rlc_entry_address":
            print(f"RLC: {state}")
        elif obj_name == "sas_entry_address":
            print(f"SAS: {state}")
    
    _dialog_menus = 'sas_menu_config, ac_menu_driver, scope_menu_driver, rlc_menu_driver, sas_menu_driver'
    def _when_dialog_menus__activated(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.currentText()
        
        prefix = obj_name.split('_')[0]
        self.config[prefix][obj_name]["index"] = obj.currentIndex()

        if obj_name == "sas_menu_config":
            print(f"SAS config selected: {state}")
            self.config["sas"][obj_name]["item"] = self.sas_configs[state]
        if obj_name == "ac_menu_driver":
            print(f"AC source driver selected: {state}")
            self.config["ac"][obj_name]["item"] = self.drivers.AC_SOURCE_DRIVERS[state]
        if obj_name == "scope_menu_driver":
            print(f"Scope driver selected: {state}")
            self.config["scope"][obj_name]["item"] = self.drivers.SCOPE_DRIVERS[state]
        if obj_name == "rlc_menu_driver":
            print(f"RLC source driver selected: {state}")
            self.config["rlc"][obj_name]["item"] = self.drivers.RLC_DRIVERS[state]
        if obj_name == "sas_menu_driver":
            print(f"SAS source driver selected: {state}")
            self.config["sas"][obj_name]["item"] = self.drivers.SAS_DRIVERS[state]

    def _on_device_entry_startup__stateChanged(self):
        state = self.sender().isChecked()
        print (f"Startup behaviour checked: {state}")
        self.config["setup_devices"] = state

#--------------------------------------------------------
#                   Main Window                         #
#--------------------------------------------------------
class MainWindow(QMainWindow, Ui_MainWindow, SmartSignal): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setup_logging()
        self.setup_config()
        self.setup_sas_plot()
        self.setup_view()

        self.error_msg = QErrorMessage()
        self.error_msg.setWindowModality(Qt.ApplicationModal)

        if self.l_config["setup_devices"]:
            self._on_options_action_devices__triggered()

        self.setup_equipment_connection()
            
        self.auto_connect()
        
    #--------------------------------------------------------
    #                       Helpers                         #
    #--------------------------------------------------------
    def setup_logging(self):
        # You can format what is printed to text box
        self.central_textEdit_log.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        # self.central_textEdit_log.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.LOG = logging.getLogger(__name__)
        self.LOG.addHandler(self.central_textEdit_log)
        # You can control the logging level
        self.LOG.setLevel(logging.INFO)

    def setup_config(self):
        dir_path = Path(__file__).resolve().parent
        with open(f"{dir_path}/config/config.json", "r") as jsonfile:
            self.d_config = json.load(jsonfile)

        try:
            with open(f"{dir_path}/config/local_config.json", "r") as jsonfile:
                self.l_config = json.load(jsonfile)
        except IOError:
            self.l_config = self.d_config
        
        self.l_config = deep_update(self.d_config, self.l_config)

        self.force_update_ui(self.l_config)
        self.LOG.info("Config loaded")

    def setup_view(self):
        self.view_action_log.setChecked(self.l_config["view"]["view_action_log"])
        
        if not self.l_config["view"]["view_action_log"]:
            self.central_textEdit_log.hide()
            self.resize(self.minimumSizeHint())
            

    def setup_equipment(self):
        loading_dlg = LoadingDialog()
        loading_dlg.set_progress(0)
        loading_dlg.show()
        QApplication.processEvents()

        if self.l_config["ac"]["ac_menu_driver"]["item"] != None:
            self.ac_src = AC_SRC(self.l_config["ac"]["ac_menu_driver"]["item"], self.l_config["ac"]["ac_entry_address"])
            self.ac_menu_abnormal.addItems(self.ac_src.AB_WAVEFORMS)
            self.ac_menu_profile.addItems(self.ac_src.PROFILES)
            self.LOG.info("AC Source configured")
        else:
            self.ac_tab.setDisabled(True)
            self.LOG.info("AC Source not configured")
        loading_dlg.set_progress(25)
        QApplication.processEvents()
        
        if self.l_config["scope"]["scope_menu_driver"]["item"] != None:
            self.scope = Scope(self.l_config["scope"]["scope_menu_driver"]["item"], self.l_config["scope"]["scope_entry_address"])
            self.LOG.info("Scope configured")
        else:
            self.scope_tab.setDisabled(True)
            self.LOG.info("Scope not configured")
        loading_dlg.set_progress(50)
        QApplication.processEvents()

        if self.l_config["rlc"]["rlc_menu_driver"]["item"] != None:
            rcc, pcc, *trash = tuple([x.strip() for x in self.l_config["rlc"]["rlc_entry_address"].split(',')])
            try:
                self.rlc = RLC(self.l_config["rlc"]["rlc_menu_driver"]["item"], relay_controller_comport=rcc, phase_controller_comport=pcc)
            except SerialException:
                self.rlc.close()
                self.rlc = RLC(self.l_config["rlc"]["rlc_menu_driver"]["item"], relay_controller_comport=rcc, phase_controller_comport=pcc)
            self.LOG.info("RLC configured")
        else:
            self.rlc_tab.setDisabled(True)
            self.LOG.info("RLC not configured") 
        
        loading_dlg.set_progress(75)
        QApplication.processEvents()

        if self.l_config["sas"]["sas_menu_driver"]["item"] != None:
            sas_addresses = [x.strip() for x in self.l_config["sas"]["sas_entry_address"].split(',')]
            self.sas = SAS(self.l_config["sas"]["sas_menu_driver"]["item"], sas_addresses, self.l_config["sas"]["sas_menu_config"]["item"])
            self.LOG.info(self.l_config["sas"]["sas_menu_config"])
            self.LOG.info("SAS configured")
        else:
            self.sas_tab.setDisabled(True)
            self.LOG.info("SAS not configured")

        loading_dlg.set_progress(100)
        QApplication.processEvents()
        loading_dlg.close()
        self.LOG.info("Equipment setup complete")

    def setup_equipment_connection(self):
        self.LOG.info("Equipment connect triggered")
        try:
            if RUN_EQUIPMENT:
                self.setup_equipment()
        except VisaIOError:
            self.error_msg.setWindowTitle("Connection failed")
            self.error_msg.showMessage("Ensure equipment is on and address is correct<br/>Retry connection:<br/>(Options->Reconnect Equipment)")
            self.error_msg.exec()

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

        self.sas_timer = QTimer()
        self.sas_timer.setInterval(100)
        self.sas_timer.timeout.connect(self.sas_update_plot_pv)

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
        # self.LOG.info(f"Power: {power}, Voltage: {voltage}")
        self.pv_point.clear()
        self.pv_point.addPoints(array([voltage]), array([power]), pen='g', symbol='o')

    def rlc_auto_update_params(self):
        if self.rlc_check_auto.isChecked():
            self.rlc_entry_ac_volts.setValue(self.l_config["ac"]["ac_entry_ac_volts"])
            self.rlc_entry_freq.setValue(self.l_config["ac"]["ac_entry_freq"])
            self.rlc_entry_reactive_pwr.setValue(0)
            self.rlc_entry_real_pwr.setValue(self.l_config["sas"]["sas_entry_pmp"])
            if RUN_EQUIPMENT:
                self.rlc.turn_on(self.l_config["rlc"])

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

    #--------------------------------------------------------
    #                       Main Items                      #
    #--------------------------------------------------------
    def _on_options_action_connect__triggered(self):
        self.setup_equipment_connection()

    def _on_options_action_devices__triggered(self):
        self.LOG.info("Device setup triggered")
        dlg = DevicesDialog(self.l_config)
        result = dlg.exec()

        if result:
            self.l_config = dlg.config
        else:
            sys.exit()

    def _on_options_action_restore__triggered(self):
        self.LOG.info("Restore defaults triggered")
        self.force_update_ui(self.d_config)

    def _on_view_action_log__triggered(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["view"][obj_name] = state

        if state:
            self.central_textEdit_log.show()
        else:
            self.central_textEdit_log.hide()
            self.resize(self.minimumSizeHint())
    
    def closeEvent(self, event):
        self._when_closers__clicked()

        if True:
            event.accept() # let the window close
        else:
            event.ignore()

    _closers = 'sas_butt_close, ac_butt_close, scope_butt_close, rlc_butt_close'
    def _when_closers__clicked(self):
        self.LOG.info("Close clicked")
        self.hide()
        try:
            self.ac_src.turn_off()
            self.ac_src.return_manual()
        except AttributeError:
            pass
        try:  
            self.sas.turn_off()
        except AttributeError:
            pass
        try:
            self.rlc.close()
            # self.rlc.turn_off()
        except AttributeError:
            pass
        try:
            self.scope.turn_off()
        except AttributeError:
            pass

            self.LOG.info("Equipment turned off")

        # save config
        dir_path = Path(__file__).resolve().parent
        with open(f"{dir_path}/config/local_config.json", "w") as jsonfile:
            json.dump(self.l_config, jsonfile)

        self.LOG.info("Config saved")

        sys.exit()

    #--------------------------------------------------------
    #                       AC Tab                          #
    #--------------------------------------------------------
    _ac_buttons = 'ac_butt_apply, ac_butt_off, ac_butt_on'
    def _when_ac_buttons__clicked(self):
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "ac_butt_apply":
            self.LOG.info("Apply clicked")
            if RUN_EQUIPMENT:
                self.ac_src.apply(self.l_config["ac"])
            self.rlc_auto_update_params()
        elif obj_name == "ac_butt_on":
            self.LOG.info("AC on clicked")
            if RUN_EQUIPMENT:
                self.ac_src.turn_on()
        elif obj_name == "ac_butt_off":
            self.LOG.info("AC off clicked")
            if RUN_EQUIPMENT:
                self.ac_src.turn_off()
        
    def _on_ac_check_abnormal__stateChanged(self):
        state = self.sender().isChecked()
        self.LOG.info (f"Abnormal checked: {state}")
        self.l_config["ac"]["ac_check_abnormal"] = state

    _ac_entries = 'ac_entry_step_size, ac_entry_freq, ac_entry_ac_volts'
    def _when_ac_entries__valueChanged(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()

        self.l_config["ac"][obj_name] = state

        if obj_name == "ac_entry_step_size":
            self.LOG.info(f"Step size entered: {state}")
        elif obj_name == "ac_entry_freq":
            self.LOG.info(f"Frequency entered: {state}")
        elif obj_name == "ac_entry_ac_volts":
            self.LOG.info(f"Ac Volts entered: {state}")

    _ac_menus = 'ac_menu_abnormal, ac_menu_profile'
    def _when_ac_menus__activated(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.currentText()

        self.l_config["ac"][obj_name] = state

        if obj_name == "ac_menu_abnormal":
            self.LOG.info(f"Abnormal waveform selected: {state}")
        elif obj_name == "ac_menu_profile":
            self.LOG.info(f"Profile selected: {state}")
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
            self.LOG.info("Single selected")
        elif obj_name == "ac_radio_split" and state:
            self.LOG.info("Split selected")
        elif obj_name == "ac_radio_three" and state:
            self.LOG.info("Three selected")

    #--------------------------------------------------------
    #                       RLC Tab                         #
    #--------------------------------------------------------
    _rlc_buttons = 'rlc_butt_off, rlc_butt_on'
    def _when_rlc_buttons__clicked(self):
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "rlc_butt_off":
            self.LOG.info("RLC off clicked")
            if RUN_EQUIPMENT:
                self.rlc.turn_off()
        elif obj_name == "rlc_butt_on":
            self.LOG.info("RLC on clicked")
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
            self.LOG.info(f"Ac Volts entered: {state}")
        elif obj_name == "rlc_entry_freq":
            self.LOG.info(f"Frequency entered: {state}")
        elif obj_name == "rlc_entry_reactive_pwr":
            self.LOG.info(f"Reactive power entered: {state}")
        elif obj_name == "rlc_entry_real_pwr":
            self.LOG.info(f"Real power entered: {state}")

    _rlc_checks = 'rlc_check_auto'
    def _when_rlc_checks__stateChanged(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["rlc"][obj_name] = state

        if obj_name == "rlc_check_auto":
            self.LOG.info (f"Auto set RLC parameters checked: {state}")
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
            self.LOG.info("SAS off clicked")
            if RUN_EQUIPMENT:
                self.sas.turn_off()
        elif obj_name == "sas_butt_on":
            self.LOG.info("SAS on clicked")
            if RUN_EQUIPMENT:
                self.sas.turn_on()
        elif obj_name == "sas_butt_apply":
            self.LOG.info("Apply clicked")
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
            self.LOG.info(f"Vmp entered: {state}")
        elif obj_name == "sas_entry_pmp":
            self.LOG.info(f"Pmp entered: {state}")
        elif obj_name == "sas_entry_ff":
            self.LOG.info(f"Fill Factor entered: {state}")
        elif obj_name == "sas_entry_irrad":
            self.LOG.info(f"Irradiance entered: {state}")

    #--------------------------------------------------------
    #                       Scope Tab                       #
    #--------------------------------------------------------
    _scope_buttons = 'scope_butt_cap, scope_butt_apply, scope_butt_browse'
    def _when_scope_buttons__clicked(self):
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "scope_butt_cap":
            self.LOG.info("Capture clicked")
            if RUN_EQUIPMENT:
                self.scope.capture_display(self.l_config["scope"])
        elif obj_name == "scope_butt_apply":
            self.LOG.info("Apply labels clicked")
            if RUN_EQUIPMENT:
                self.scope.label(self.l_config["scope"])
        elif obj_name == "scope_butt_browse":
            path = str(QFileDialog.getExistingDirectory())
            self.scope_line_cap_path.setText(path)
            self.LOG.info(f"Capture path entered: {path}")
            self.l_config["scope"][obj_name] = path
        
    _scope_checks = 'scope_check_auto, scope_check_date, scope_check_invert'
    def _when_scope_checks__stateChanged(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["scope"][obj_name] = state

        if obj_name == "scope_check_auto":
            self.LOG.info (f"Auto capture checked: {state}")
            if state:
                if RUN_EQUIPMENT:    
                    self.scope.auto_capture_on(self.l_config["scope"])
            else:
                if RUN_EQUIPMENT:
                    self.scope.auto_capture_off()
        elif obj_name == "scope_check_date":
            self.LOG.info (f"Date checked: {state}")
        elif obj_name == "scope_check_invert":
            self.LOG.info (f"Invert checked: {state}")
    
    _scope_entries = 'scope_line_cap_name, scope_line_cap_path, scope_line_ch1_lab, scope_line_ch2_lab, scope_line_ch3_lab, scope_line_ch4_lab'
    def _when_scope_entries__editingFinished(self):
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.text()
        
        self.l_config["scope"][obj_name] = state

        if obj_name == "scope_line_cap_name":
            self.LOG.info(f"Capture name entered: {state}")
        elif obj_name == "scope_line_cap_path":
            self.LOG.info(f"Capture path entered: {state}")
        elif obj_name == "scope_line_ch1_lab":
            self.LOG.info(f"CH1 label entered: {state}")
        elif obj_name == "scope_line_ch2_lab":
            self.LOG.info(f"CH2 label entered: {state}")
        elif obj_name == "scope_line_ch3_lab":
            self.LOG.info(f"CH3 label entered: {state}")
        elif obj_name == "scope_line_ch4_lab":
            self.LOG.info(f"CH4 label entered: {state}")

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
