import time
start_time = time.time()

import sys
import json
import traceback
import logging
import re


from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QErrorMessage, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QRadioButton, QFileDialog, QProgressDialog
from PySide6.QtCore import QTimer, Qt, QSize
from pyqtgraph import ViewBox, PlotCurveItem, ScatterPlotItem
from numpy import array

from one_gui.ui.One_GUI_To_Rule_Them_All_ui import Ui_MainWindow
from one_gui.ui.Devices_Dialog_ui import Ui_DevicesDialog
from one_gui.ui.Loading_Dialog_ui import Ui_LoadingDialog
from one_gui.logic.ac_src import AC_SRC, Mock_AC_SRC
from one_gui.logic.scope import Scope, Mock_Scope
from one_gui.logic.rlc import RLC, Mock_RLC
from one_gui.logic.sas import SAS, Mock_SAS
from one_gui.logic.chamber import Chamber, Mock_Chamber
from one_gui.logic.signal import SmartSignal
from one_gui.logic.equipment_library import EquipmentDrivers
from one_gui.logic.utils import dict_value_to_index, deep_update, discover_addresses
from serial.serialutil import SerialException
from pyvisa.errors import VisaIOError
from pathlib import Path


import_time = time.time()
print(f"Import time: {import_time - start_time}")

# TODO: Some serious commenting is needed
# TODO: Fix double entry ranges (AC src ff, irrad)
# TODO: Setup mock equipment. Use dummay class as path for equipment driver

RUN_EQUIPMENT = False

#--------------------------------------------------------
#                   Loading Dialog                      #
#--------------------------------------------------------
class LoadingDialog(QDialog, Ui_LoadingDialog):
    """Class to show a loading dialog with a programmable progress bar
    """
    def __init__(self, steps, *args, **kwargs):
        """Method to initialise the class

        Args:
            steps (int): The number of steps the progress bar will make
        """
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.progress = 0
        self.step = 100/steps

        self.set_progress(self.progress)
        self.show()
        
    def set_progress(self, value):
        """Method to set the progress of the progress bar

        Args:
            value (int): Progress value as a percentage. i.e value=50 for 50%
        """
        self.progressBar.setValue(value)
        QApplication.processEvents()
    
    def step_progress(self):
        """Method to step the progress bar by the initilised amount
        """
        self.progress += self.step
        self.set_progress(int(self.progress))
    
    def progress_complete(self):
        """Method to comlete the progress bar and close the window
        """
        self.close()

#--------------------------------------------------------
#                   Devices Dialog                      #
#--------------------------------------------------------
class DevicesDialog(QDialog, Ui_DevicesDialog, SmartSignal):
    """Class to allow the user to setup the equipment to be controlled
    """
    def __init__(self, config, *args, **kwargs):
        """Initialise the class

        Args:
            config (dict): Dictionary containing the persistant configuration settings. This is overwritten with the updated configuration.
        """
        super().__init__()
        self.drivers = EquipmentDrivers()

        self.config = config

        self.sas_configs = {
            "Series":   "series",
            "Parallel": "parallel"
        }
        
        auto_discovered_connection_addresses = discover_addresses()
        
        self.setupUi(self)
        
        self.ac_menu_driver.addItems(self.drivers.AC_SOURCE_DRIVERS)
        self.scope_menu_driver.addItems(self.drivers.SCOPE_DRIVERS)
        self.rlc_menu_driver.addItems(self.drivers.RLC_DRIVERS)
        self.sas_menu_driver.addItems(self.drivers.SAS_DRIVERS)
        self.sas_menu_config.addItems(self.sas_configs)
        self.chamber_menu_driver.addItems(self.drivers.CHAMBER_DRIVERS)
        
        self.sas_menu_config.setCurrentIndex(config["sas"]["sas_menu_config"]["index"])
        self.ac_menu_driver.setCurrentIndex(config["ac"]["ac_menu_driver"]["index"])
        self.scope_menu_driver.setCurrentIndex(config["scope"]["scope_menu_driver"]["index"])
        self.rlc_menu_driver.setCurrentIndex(config["rlc"]["rlc_menu_driver"]["index"])
        self.sas_menu_driver.setCurrentIndex(config["sas"]["sas_menu_driver"]["index"])
        self.sas_menu_config.setCurrentIndex(config["sas"]["sas_menu_config"]["index"])
        self.chamber_menu_driver.setCurrentIndex(config["chamber"]["chamber_menu_driver"]["index"])

        self.ac_entry_address.addItems(auto_discovered_connection_addresses)
        self.scope_entry_address.addItems(auto_discovered_connection_addresses)
        self.rlc_entry_address_r.addItems(auto_discovered_connection_addresses)
        self.rlc_entry_address_p.addItems(auto_discovered_connection_addresses)
        self.sas_entry_address.addItems(auto_discovered_connection_addresses)
        self.chamber_entry_address.addItems(auto_discovered_connection_addresses)

        self.ac_entry_address.setCurrentText(config["ac"]["ac_entry_address"])
        self.scope_entry_address.setCurrentText(config["scope"]["scope_entry_address"])
        self.rlc_entry_address_r.setCurrentText(config["rlc"]["rlc_entry_address_r"])
        self.rlc_entry_address_p.setCurrentText(config["rlc"]["rlc_entry_address_p"])
        self.sas_entry_address.setCurrentText(config["sas"]["sas_entry_address"])
        self.chamber_entry_address.setCurrentText(config["chamber"]["chamber_entry_address"])

        self.device_entry_startup.setChecked(config["setup_devices"])

        self.auto_connect()

    _dialog_entries = 'ac_entry_address, scope_entry_address, rlc_entry_address_r, rlc_entry_address_p, sas_entry_address, chamber_entry_address'
    def _when_dialog_entries__activated(self):
        """Method to handle dialog entries. Will be called when the user completes an entry by pressing enter or losing focus.
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.currentText()

        prefix = obj_name.split('_')[0]
        self.config[prefix][obj_name] = state

        if obj_name == "ac_entry_address":
            print(f"AC Source: {state}")
        elif obj_name == "scope_entry_address":
            print(f"Scope: {state}")
        elif obj_name == "rlc_entry_address_r":
            print(f"RLC rcc: {state}")
        elif obj_name == "rlc_entry_address_p":
            print(f"RLC pcc: {state}")
        elif obj_name == "sas_entry_address":
            print(f"SAS: {state}")
        elif obj_name == "chamber_entry_address":
            print(f"Chamber: {state}")
    
    _dialog_menus = 'sas_menu_config, ac_menu_driver, scope_menu_driver, rlc_menu_driver, sas_menu_driver, chamber_menu_driver'
    def _when_dialog_menus__activated(self):
        """Method to handle dialog menus. Will be called when the user selects an item from a menu.
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.currentText()
        
        prefix = obj_name.split('_')[0]
        self.config[prefix][obj_name]["index"] = obj.currentIndex()

        if obj_name == "sas_menu_config":
            print(f"SAS config selected: {state}")
            self.config["sas"][obj_name]["item"] = self.sas_configs[state]
        elif obj_name == "ac_menu_driver":
            print(f"AC source driver selected: {state}")
            self.config["ac"][obj_name]["item"] = self.drivers.AC_SOURCE_DRIVERS[state]
        elif obj_name == "scope_menu_driver":
            print(f"Scope driver selected: {state}")
            self.config["scope"][obj_name]["item"] = self.drivers.SCOPE_DRIVERS[state]
        elif obj_name == "rlc_menu_driver":
            print(f"RLC source driver selected: {state}")
            self.config["rlc"][obj_name]["item"] = self.drivers.RLC_DRIVERS[state]
        elif obj_name == "sas_menu_driver":
            print(f"SAS source driver selected: {state}")
            self.config["sas"][obj_name]["item"] = self.drivers.SAS_DRIVERS[state]
        elif obj_name == "chamber_menu_driver":
            print(f"Chamber source driver selected: {state}")
            self.config["chamber"][obj_name]["item"] = self.drivers.CHAMBER_DRIVERS[state]

    _dialog_checks = 'device_entry_startup'
    def _when_dialog_checks__stateChanged(self):
        """Method to handle dialog check boxes. Will be called when the user toggles a checkbox.
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.config["setup_devices"] = state
        print (f"Startup behaviour checked: {state}")

#--------------------------------------------------------
#                   Main Window                         #
#--------------------------------------------------------
class MainWindow(QMainWindow, Ui_MainWindow, SmartSignal):
    """Class for the main GUI window. This class allows the user to control the configured equipment on a bench.
    """
    def __init__(self, *args, **kwargs):
        """Initilise the class
        """
        super().__init__(*args, **kwargs)
        
        self.setupUi(self)
        self.setup_logging()
        self.setup_config()
        self.setup_sas_plot()
        self.setup_view()

        self.error_msg = QErrorMessage()
        self.error_msg.setWindowModality(Qt.ApplicationModal)
        self.error_msg.resize(QSize(350, 200))

        if self.l_config["setup_devices"]:
            self.setup_devices_dialog()

        self.setup_equipment_connection()
            
        self.auto_connect()
        
    #--------------------------------------------------------
    #                       Helpers                         #
    #--------------------------------------------------------
    def setup_logging(self):
        """Method to setup logging for the gui application
        """

        self.log = logging.getLogger(__name__)
        
        # You can control the logging level
        self.log.setLevel(logging.INFO)

        # You can format what is printed to text box
        formatter = logging.Formatter('%(levelname)s - %(message)s')

        self.central_textEdit_log.setFormatter(formatter)
        self.log.addHandler(self.central_textEdit_log)
        
        self.std_out_handler = logging.StreamHandler(sys.stdout)
        self.std_out_handler.setFormatter(formatter)
        self.log.addHandler(self.std_out_handler)

        

    def setup_config(self):
        """Method to load the persistant configuration settings
        """
        dir_path = Path(__file__).resolve().parent
        with open(dir_path.joinpath("config", "config.json"), "r") as jsonfile:
            self.d_config = json.load(jsonfile)

        try:
            with open(dir_path.joinpath("config", "local_config.json"), "r") as jsonfile:
                self.l_config = json.load(jsonfile)
        except IOError:
            self.l_config = self.d_config
        
        self.l_config = deep_update(self.d_config, self.l_config)

        self.force_update_ui(self.l_config)
        self.log.info("Config loaded")

    def setup_view(self):
        """Method to setup embedded logging box using persistent settings
        """
        self.view_action_log.setChecked(self.l_config["view"]["view_action_log"])
        
        if not self.l_config["view"]["view_action_log"]:
            self.central_textEdit_log.hide()
            self.resize(self.minimumSizeHint())
            
    def setup_devices_dialog(self):
        self.log.info("Device setup triggered")
        
        dlg = DevicesDialog(self.l_config)
        result = dlg.exec()

        if result:
            self.l_config = dlg.config
        else:
            sys.exit()

    def setup_equipment(self):
        """Method to initialise and setup bench equipment.

        Returns:
            list: A list of equipment that errored and was not setup during during initialization.
        """
        errors = list()
        loading_dlg = LoadingDialog(steps=5)

        self.ac_src = None
        try:
            if self.l_config["ac"]["ac_menu_driver"]["item"] != None:
                if RUN_EQUIPMENT:
                    self.ac_src = AC_SRC(self.l_config["ac"]["ac_menu_driver"]["item"], self.l_config["ac"]["ac_entry_address"])
                else:
                    self.ac_src = Mock_AC_SRC()
                self.ac_menu_abnormal.addItems(self.ac_src.AB_WAVEFORMS)
                self.ac_menu_profile.addItems(self.ac_src.PROFILES)
                self.log.info("AC Source configured")
            else:
                self.ac_tab.setDisabled(True)
                self.log.info("AC Source not configured")    
        except VisaIOError:
            self.ac_tab.setDisabled(True)
            self.log.error("AC Source connection failed")
            errors.append('AC Source')
            
        loading_dlg.step_progress()
        
        self.scope = None
        try:
            if self.l_config["scope"]["scope_menu_driver"]["item"] != None:
                if RUN_EQUIPMENT:
                    self.scope = Scope(self.l_config["scope"]["scope_menu_driver"]["item"], self.l_config["scope"]["scope_entry_address"])
                else:
                    self.scope = Mock_Scope()
                self.log.info("Scope configured")
            else:
                self.scope_tab.setDisabled(True)
                self.log.info("Scope not configured") 
        except VisaIOError:
            self.scope_tab.setDisabled(True)
            self.log.error("Scope connection failed")
            errors.append('Scope')
            
        loading_dlg.step_progress()

        self.rlc = None
        try:
            if self.l_config["rlc"]["rlc_menu_driver"]["item"] != None:
                if RUN_EQUIPMENT:
                    try:
                        self.rlc = RLC(self.l_config["rlc"]["rlc_menu_driver"]["item"], self.l_config["rlc"]["rlc_entry_address_r"], self.l_config["rlc"]["rlc_entry_address_p"])
                    except SerialException:
                        self.rlc.close()
                        self.rlc = RLC(self.l_config["rlc"]["rlc_menu_driver"]["item"], self.l_config["rlc"]["rlc_entry_address_r"], self.l_config["rlc"]["rlc_entry_address_p"])
                    self.log.info("RLC configured")
                else:
                    self.rlc = Mock_RLC()
            else:
                self.rlc_tab.setDisabled(True)
                self.log.info("RLC not configured")
        except VisaIOError:
            self.rlc_tab.setDisabled(True)
            self.log.error("RLC connection failed")
            errors.append('RLC')
        
        loading_dlg.step_progress()

        self.sas = None
        try:
            if self.l_config["sas"]["sas_menu_driver"]["item"] != None:
                sas_addresses = [x.strip() for x in self.l_config["sas"]["sas_entry_address"].split(',')]
                if RUN_EQUIPMENT:
                    self.sas = SAS(self.l_config["sas"]["sas_menu_driver"]["item"], sas_addresses, self.l_config["sas"]["sas_menu_config"]["item"])
                else:
                    self.sas = Mock_SAS()
                self.log.info(self.l_config["sas"]["sas_menu_config"])
                self.log.info("SAS configured")
            else:
                self.sas_tab.setDisabled(True)
                self.log.info("SAS not configured")
        except VisaIOError:
            self.sas_tab.setDisabled(True)
            self.log.error("SAS connection failed")
            errors.append('SAS')

        loading_dlg.step_progress()

        self.chamber = None
        try:
            if self.l_config["chamber"]["chamber_menu_driver"]["item"] != None:
                if self.l_config["chamber"]["chamber_entry_address"] == 'enphase_equipment.thermal_chamber.watlow.WatlowF4':
                    address = int(re.sub('\\D', '', self.l_config["chamber"]["chamber_entry_address"]))
                else:
                    address = self.l_config["chamber"]["chamber_entry_address"]
                if RUN_EQUIPMENT:
                    try:
                        self.chamber = Chamber(self.l_config["chamber"]["chamber_menu_driver"]["item"], address)
                    except SerialException:
                        self.chamber.close()
                        self.chamber = Chamber(self.l_config["chamber"]["chamber_menu_driver"]["item"], address)
                    self.log.info("Chamber configured")
                else:
                    self.chamber = Mock_Chamber()
                self.log.info("Chamber configured")
            else:
                self.chamber_tab.setDisabled(True)
                self.log.info("Chamber not configured")
        except VisaIOError:
            self.chamber_tab.setDisabled(True)
            self.log.error("Chamber connection failed")
            errors.append('Chamber')

        loading_dlg.step_progress()
        loading_dlg.progress_complete()
        self.log.info("Equipment setup complete")
        
        return errors

    def setup_equipment_connection(self):
        """Method to handle equipment setup
        """
        self.log.info("Equipment connect triggered")
        try:
            errors = self.setup_equipment()
            
            if len(errors) != 0:
                self.error_msg.setWindowTitle("Connection failed")
                error_msg = ''.join(f'&nbsp;&nbsp;&nbsp;&nbsp;{errored}<br/>' for errored in errors)
                self.error_msg.showMessage("The following equipment failed to connect:<br/>"\
                                        f"{error_msg}"\
                                            "Ensure equipment is turned on and address is correct.<br/>"\
                                            "&nbsp;&nbsp;&nbsp;&nbsp;(Options->Configure Equipment)<br/>"
                                            "Then retry connection.<br/>"\
                                            "&nbsp;&nbsp;&nbsp;&nbsp;(Options->Reconnect Equipment)")
                self.error_msg.exec()
        except Exception as e:
            self.log.error(traceback.format_exc())
        
    def setup_sas_plot(self):
        """Funtion to setup the plot embedded in the GUI for the SAS.
        """
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
        """Method to update the embedded sas plot with the curve set by the sas variables.

        Args:
            data (dict): Dictionary containing the power, voltage, and current data for the plot.
        """
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
        """Method to update the embedded sas plot with the current power voltage point.
        """
        data = self.sas.get_sas_pv()
        current = data["i"]
        voltage = data["v"]
        power = data["p"]
        # self.log.info(f"Power: {power}, Voltage: {voltage}")
        self.pv_point.clear()
        self.pv_point.addPoints(array([voltage]), array([power]), pen='g', symbol='o')

    def rlc_auto_update_params(self):
        """Method to set the rlc parameters based on the present sas and ac source paramters
        """
        if self.rlc_check_auto.isChecked():
            self.rlc_entry_ac_volts.setValue(self.l_config["ac"]["ac_entry_ac_volts"])
            self.rlc_entry_freq.setValue(self.l_config["ac"]["ac_entry_freq"])
            self.rlc_entry_reactive_pwr.setValue(0)
            self.rlc_entry_real_pwr.setValue(self.l_config["sas"]["sas_entry_pmp"])
            self.rlc.turn_on(self.l_config["rlc"])

    def force_update_ui(self, config):
        """Method to force update the gui elements with the persistant settings

        Args:
            config (dict): Dictionary containing the persistant settings
        """
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
    _actions = 'options_action_connect, options_action_devices, options_action_restore, view_action_log'
    def _when_actions__triggered(self):
        """Method to handle menubar actions. Will be called when the user selects an item from a menu in the menubar.
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        if obj_name == "options_action_connect":
            self.log.info("Reconnect Equipement clicked")
            self.setup_equipment_connection()
        elif obj_name == "options_action_devices":
            self.log.info("Configure Equipment clicked")
            self.setup_devices_dialog()
        elif obj_name == "options_action_restore":
            self.log.info("Restore Defaults clicked")
            self.force_update_ui(self.d_config)
        elif obj_name == "view_action_log":
            self.log.info("View Log clicked")
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

    _closers = 'sas_butt_close, ac_butt_close, scope_butt_close, rlc_butt_close, chamber_butt_close'
    def _when_closers__clicked(self):
        """Fucntion to handle close events. Will be called when any of the close buttons are clicked
        """
        self.log.info("Close clicked")
        self.hide()
        
        if self.ac_src != None:
            self.ac_src.turn_off()
            self.ac_src.return_manual()
        if self.sas != None:
            self.sas.turn_off()
        if self.rlc != None:
            self.rlc.turn_off()
        if self.scope != None:
            self.scope.turn_off()
        if self.chamber != None:
            self.chamber.close()

        self.log.info("Equipment turned off")

        # save config
        dir_path = Path(__file__).resolve().parent
        with open(dir_path.joinpath("config", "local_config.json"), "w") as jsonfile:
            json.dump(self.l_config, jsonfile)

        self.log.info("Config saved")

        sys.exit()

    #--------------------------------------------------------
    #                       AC Tab                          #
    #--------------------------------------------------------
    _ac_buttons = 'ac_butt_apply, ac_butt_off, ac_butt_on'
    def _when_ac_buttons__clicked(self):
        """Method to handle the ac tab buttons. Will be called whenever a button on the ac tab is clicked
        """
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "ac_butt_apply":
            self.log.info("Apply clicked")
            self.ac_src.apply(self.l_config["ac"])
            self.rlc_auto_update_params()
        elif obj_name == "ac_butt_on":
            self.log.info("AC on clicked")
            self.ac_src.turn_on()
        elif obj_name == "ac_butt_off":
            self.log.info("AC off clicked")
            self.ac_src.turn_off()
        
    def _on_ac_check_abnormal__stateChanged(self):
        """Method to handle the ac tab check buttons. Will be called whenever a check on the ac tab is toggled
        """
        state = self.sender().isChecked()
        self.log.info (f"Abnormal checked: {state}")
        self.l_config["ac"]["ac_check_abnormal"] = state

    _ac_entries = 'ac_entry_step_size, ac_entry_freq, ac_entry_ac_volts'
    def _when_ac_entries__valueChanged(self):
        """Method to handle the ac tab entries. Will be called whenever a entry on the ac tab is completed or focus is lost
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()

        self.l_config["ac"][obj_name] = state

        if obj_name == "ac_entry_step_size":
            self.log.info(f"Step size entered: {state}")
        elif obj_name == "ac_entry_freq":
            self.log.info(f"Frequency entered: {state}")
        elif obj_name == "ac_entry_ac_volts":
            self.log.info(f"Ac Volts entered: {state}")

    _ac_menus = 'ac_menu_abnormal, ac_menu_profile'
    def _when_ac_menus__activated(self):
        """Method to handle the ac tab menus. Will be called whenever a menu on the ac tab is activated
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.currentText()

        self.l_config["ac"][obj_name] = state

        if obj_name == "ac_menu_abnormal":
            self.log.info(f"Abnormal waveform selected: {state}")
        elif obj_name == "ac_menu_profile":
            self.log.info(f"Profile selected: {state}")
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
        """Method to handle the ac tab radio buttons. Will be called whenever a radio button on the ac tab is toggled
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["ac"][obj_name] = state

        if obj_name == "ac_radio_single" and state:
            self.log.info("Single selected")
        elif obj_name == "ac_radio_split" and state:
            self.log.info("Split selected")
        elif obj_name == "ac_radio_three" and state:
            self.log.info("Three selected")

    #--------------------------------------------------------
    #                       RLC Tab                         #
    #--------------------------------------------------------
    _rlc_buttons = 'rlc_butt_off, rlc_butt_on'
    def _when_rlc_buttons__clicked(self):
        """Method to handle the rlc tab buttons. Will be called whenever a button on the rlc tab is clicked
        """
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "rlc_butt_off":
            self.log.info("RLC off clicked")
            self.rlc.turn_off()
        elif obj_name == "rlc_butt_on":
            self.log.info("RLC on clicked")
            rlc_config = self.l_config["rlc"]
            try:
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
        """Method to handle the rlc tab entries. Will be called whenever a entry on the rlc tab is completed or focus is lost
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()

        self.l_config["rlc"][obj_name] = state

        if obj_name == "rlc_entry_ac_volts":
            self.log.info(f"Ac Volts entered: {state}")
        elif obj_name == "rlc_entry_freq":
            self.log.info(f"Frequency entered: {state}")
        elif obj_name == "rlc_entry_reactive_pwr":
            self.log.info(f"Reactive power entered: {state}")
        elif obj_name == "rlc_entry_real_pwr":
            self.log.info(f"Real power entered: {state}")

    _rlc_checks = 'rlc_check_auto'
    def _when_rlc_checks__stateChanged(self):
        """Method to handle the rlc tab check buttons. Will be called whenever a check button on the rlc tab is toggled
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["rlc"][obj_name] = state

        if obj_name == "rlc_check_auto":
            self.log.info (f"Auto set RLC parameters checked: {state}")
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
        """Method to handle the rlc tab autofill entries. Will be called whenever a snooped entry is completed
        """
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
        """Method to handle the rlc tab auto buttons. Will be called whenever a snooped button is clicked
        """
        obj = self.sender()
        obj_name = obj.objectName()

        if self.rlc_check_auto.isChecked():
            if obj_name == "ac_butt_apply":
                    rlc_config = self.rlc.turn_on(rlc_config)
                    self.l_config["rlc"].update(rlc_config)

    #--------------------------------------------------------
    #                       SAS Tab                         #
    #--------------------------------------------------------
    _sas_buttons = 'sas_butt_off, sas_butt_on, sas_butt_apply'
    def _when_sas_buttons__clicked(self):
        """Method to handle the sas tab buttons. Will be called whenever a button on the sas tab is clicked
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.text()

        if obj_name == "sas_butt_off":
            self.log.info("SAS off clicked")
            self.sas.turn_off()
        elif obj_name == "sas_butt_on":
            self.log.info("SAS on clicked")
            self.sas.turn_on()
        elif obj_name == "sas_butt_apply":
            self.log.info("Apply clicked")
            sas_data =  self.sas.apply(self.l_config["sas"])
            self.sas_plot_pvi(sas_data)
            self.sas_timer.start()
            self.rlc_auto_update_params()

    _sas_entries = 'sas_entry_vmp, sas_entry_pmp, sas_entry_ff, sas_entry_irrad'
    def _when_sas_entries__editingFinished(self):
        """Method to handle the sas tab entries. Will be called whenever a entry on the sas tab is complted or focus is lost
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()

        self.l_config["sas"][obj_name] = state
        
        if obj_name == "sas_entry_vmp":
            self.log.info(f"Vmp entered: {state}")
        elif obj_name == "sas_entry_pmp":
            self.log.info(f"Pmp entered: {state}")
        elif obj_name == "sas_entry_ff":
            self.log.info(f"Fill Factor entered: {state}")
        elif obj_name == "sas_entry_irrad":
            self.log.info(f"Irradiance entered: {state}")

    #--------------------------------------------------------
    #                       Scope Tab                       #
    #--------------------------------------------------------
    _scope_buttons = 'scope_butt_cap, scope_butt_apply, scope_butt_browse'
    def _when_scope_buttons__clicked(self):
        """Method to handle the scope tab buttons. Will be called whenever a button on the scope tab is clicked
        """
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "scope_butt_cap":
            self.log.info("Capture clicked")
            self.scope.capture_display(self.l_config["scope"])
        elif obj_name == "scope_butt_apply":
            self.log.info("Apply labels clicked")
            self.scope.label(self.l_config["scope"])
        elif obj_name == "scope_butt_browse":
            path = str(QFileDialog.getExistingDirectory())
            self.scope_line_cap_path.setText(path)
            self.log.info(f"Capture path entered: {path}")
            self.l_config["scope"][obj_name] = path
        
    _scope_checks = 'scope_check_auto, scope_check_date, scope_check_invert'
    def _when_scope_checks__stateChanged(self):
        """Method to handle the scope tab check buttons. Will be called whenever a checkbutton on the scope tab is toggled
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.isChecked()

        self.l_config["scope"][obj_name] = state

        if obj_name == "scope_check_auto":
            self.log.info (f"Auto capture checked: {state}")
            if state: 
                self.scope.auto_capture_on(self.l_config["scope"])
            else:
                self.scope.auto_capture_off()
        elif obj_name == "scope_check_date":
            self.log.info (f"Date checked: {state}")
        elif obj_name == "scope_check_invert":
            self.log.info (f"Invert checked: {state}")
    
    _scope_entries = 'scope_line_cap_name, scope_line_cap_path, scope_line_ch1_lab, scope_line_ch2_lab, scope_line_ch3_lab, scope_line_ch4_lab'
    def _when_scope_entries__editingFinished(self):
        """Method to handle the scope tab entries. Will be called whenever a entry on the scope tab is completed or focus is lost
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.text()
        
        self.l_config["scope"][obj_name] = state

        if obj_name == "scope_line_cap_name":
            self.log.info(f"Capture name entered: {state}")
        elif obj_name == "scope_line_cap_path":
            self.log.info(f"Capture path entered: {state}")
        elif obj_name == "scope_line_ch1_lab":
            self.log.info(f"CH1 label entered: {state}")
        elif obj_name == "scope_line_ch2_lab":
            self.log.info(f"CH2 label entered: {state}")
        elif obj_name == "scope_line_ch3_lab":
            self.log.info(f"CH3 label entered: {state}")
        elif obj_name == "scope_line_ch4_lab":
            self.log.info(f"CH4 label entered: {state}")

    #--------------------------------------------------------
    #                     Chamber Tab                       #
    #--------------------------------------------------------
    _chamber_buttons = 'chamber_butt_apply'
    def _when_chamber_buttons__clicked(self):
        """Method to handle the chamber tab buttons. Will be called whenever a button on the chamber tab is clicked
        """
        obj = self.sender()
        obj_name = obj.objectName()

        if obj_name == "chamber_butt_apply":
            self.log.info("Apply clicked")
            self.chamber.apply(self.l_config["chamber"]["chamber_entry_temp"])

    _chamber_entries = 'chamber_entry_temp'
    def _when_chamber_entries__editingFinished(self):
        """Method to handle the chamber tab entries. Will be called whenever a entry on the chamber tab is completed or focus is lost
        """
        obj = self.sender()
        obj_name = obj.objectName()
        state = obj.value()
        
        self.l_config["chamber"][obj_name] = state

        if obj_name == "chamber_entry_temp":
            self.log.info(f"Temperature entered: {state}")


def main():
    """Funciton to invoke the main process
    """
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
