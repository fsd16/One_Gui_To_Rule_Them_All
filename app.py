import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QErrorMessage, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, QRadioButton, QComboBox
from PySide6.QtCore import QSettings
from pyqtconfig import ConfigManager
from pydantic.utils import deep_update

from ui.ui_One_Gui_To_Rule_Them_All import Ui_MainWindow
from logic.ac_src import AC_SRC
from logic.scope import Scope
from logic.rlc import RLC
from logic.sas import SAS

import smartside.signal as smartsignal

class MainWindow(QMainWindow, Ui_MainWindow, smartsignal.SmartSignal): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.errorMsg = QErrorMessage()
        
        self.ac_src = AC_SRC("GPIB0::1::INSTR")
        self.scope = Scope("GPIB0::28::INSTR")
        self.rlc = RLC(relay_controller_comport='COM3',
                    phase_controller_comport='COM4')
        self.sas = SAS("GPIB0::15::INSTR")

        # self.load_config()
        
        self.ac_menu_abnormal.addItems(self.ac_src.AB_WAVEFORMS)
        self.ac_menu_phase.addItems(self.ac_src.PROFILES)
        
        self.auto_connect()    
    
    def load_config(self):

        with open("config.json", "r") as jsonfile:
            self.config = json.load(jsonfile)
        
        default_config = self.config["default"]
        self.ac_src.set_config(default_config["ac"])
        self.scope.set_config(default_config["scope"])
        self.rlc.set_config(default_config["rlc"])
        self.sas.set_config(default_config["sas"])
        
        children = []
        children += self.findChildren(QSpinBox)
        children += self.findChildren(QDoubleSpinBox)
        children += self.findChildren(QLineEdit)
        children += self.findChildren(QCheckBox)
        children += self.findChildren(QRadioButton)
        children += self.findChildren(QComboBox)
        # print(children)

        for child in children:
            name = child.objectName()
            if not name.startswith('qt_'):
                if 'entry' in name:
                    wgtobj = getattr(self, name)
                    wgtobj.setValue(default_config["ac"][name])

        print("Config loaded")

    _closers = 'sas_butt_close, ac_butt_close, scope_butt_close, rlc_butt_close'
    def _when_closers__clicked(self):
        print("Close was clicked")
        # save config
        # ac_config = self.ac_src.get_config()
        # scope_config = self.scope.get_config()
        # rlc_config = self.rlc.get_config()
        # sas_config = self.sas.get_config()
        # current_config = {
        #     "ac": ac_config,
        #     "scope": scope_config,
        #     "rlc": rlc_config,
        #     "sas": sas_config,
        # }

        # self.config["current"] = deep_update(self.config["current"], current_config)

        # with open("config.json", "w") as jsonfile:
        #     json.dump(self.config, jsonfile)
        # print("Config saved")

        sys.exit()
    
    # AC Tab
    def _on_ac_butt_off__clicked(self):
        print("AC off was clicked")
        self.ac_src.turn_off()
    
    def _on_ac_butt_on__clicked(self):
        print("AC on was clicked")
        self.ac_src.turn_on()
        
    def _on_ac_butt_apply__clicked(self):
        print("Apply was clicked")
        
        if self.ac_check_abnormal.isChecked():
            self.ac_src.apply_abnormal()
        else:
            self.ac_src.apply()
        
    def _on_ac_check_abnormal__stateChanged(self):
        print ('Abnormal was checked', self.sender().isChecked())

    def _on_ac_entry_ac_volts__valueChanged(self):
        print("Ac Volts entered:", self.sender().value())
        self.ac_src.set_ac_rms_volts(self.sender().value())

    def _on_ac_entry_freq__valueChanged(self):
        print("Frequency entered:", self.sender().value())
        self.ac_src.set_ac_freq(self.sender().value())
        
    def _on_ac_entry_step_size__valueChanged(self):
        print("Step size entered:", self.sender().value())
        self.ac_entry_ac_volts.setSingleStep(self.sender().value())
    
    def _on_ac_menu_abnormal__activated(self):
        print("Abnormal waveform selected:", self.sender().currentText())
        self.ac_src.set_ab_waveform(self.sender().currentText())
        
    def _on_ac_menu_phase__activated(self):
        
        print("Profile selected:", self.sender().currentText())
        # self.ac_src.set_ac_profile(self.sender().currentText())
        profile = self.ac_src.PROFILES[self.sender().currentText()]
        self.ac_entry_ac_volts.setValue(profile[0])
        self.ac_entry_freq.setValue(profile[1])
        
        if profile[2] == "split":
            self.ac_radio_split.setChecked(True)
        elif profile[2] == "single":
            self.ac_radio_single.setChecked(True)
        elif profile[2] == "three":
            self.ac_radio_three.setChecked(True)

    def _on_ac_radio_single__toggled(self):
        if self.ac_radio_single.isChecked():
            print("Single is selected")
            self.ac_src.set_ac_config("single")
            
    def _on_ac_radio_split__toggled(self):
        if self.ac_radio_split.isChecked():
            print("Split is selected")
            self.ac_src.set_ac_config("split")
            
    def _on_ac_radio_three__toggled(self):
        if self.ac_radio_three.isChecked():
            print("Three is selected")
            self.ac_src.set_ac_config("three")
        
    # Scope tab
    def _on_scope_butt_apply__clicked(self):
        print("Apply labels was clicked")
        self.scope.label()
    
    def _on_scope_butt_cap__clicked(self):
        print("Capture was clicked")
        self.scope.capture_display()
        
    def _on_scope_check_auto__stateChanged(self):
        print ('Check is', self.sender().isChecked())
        if self.sender().isChecked():
            self.scope.auto_capture_on()
        else:
            self.scope.auto_capture_off()
        
    def _on_scope_check_date__stateChanged(self):
        print ('Check is', self.sender().isChecked())
        self.scope.set_date(self.sender().isChecked())
        
    def _on_scope_check_invert__stateChanged(self):
        print ('Check is', self.sender().isChecked())
        self.scope.set_invert(self.sender().isChecked())
        
    def _on_scope_line_cap_name__editingFinished(self):
        print("Capture name entered:", self.sender().text())
        self.scope.set_name(self.sender().text())
        
    def _on_scope_line_cap_path__editingFinished(self):
        print("Capture path entered:", self.sender().text())
        self.scope.set_path(self.sender().text())
    
    def _on_scope_line_ch1_lab__editingFinished(self):
        print("CH1 label entered:", self.sender().text())
        self.scope.set_ch1(self.sender().text())
        
    def _on_scope_line_ch2_lab__editingFinished(self):
        print("CH2 label entered:", self.sender().text())
        self.scope.set_ch2(self.sender().text())
        
    def _on_scope_line_ch3_lab__editingFinished(self):
        print("CH3 label entered:", self.sender().text())
        self.scope.set_ch3(self.sender().text())
        
    def _on_scope_line_ch4_lab__editingFinished(self):
        print("CH4 label entered:", self.sender().text())
        self.scope.set_ch4(self.sender().text())
        
    # RLC tab
    def _on_rlc_butt_off__clicked(self):
        print("RLC off was clicked")
        self.rlc.turn_off()
    
    def _on_rlc_butt_on__clicked(self):
        print("RLC on was clicked")
        try:
            self.rlc.turn_on()
            self.rlc_entry_real_pwr.setValue(round(self.rlc.SETTINGS["real_pwr"]))
            self.rlc_entry_reactive_pwr.setValue(round(self.rlc.SETTINGS["reactive_pwr"]))
        except self.rlc.NoInput:
            self.errorMsg.showMessage("Why do I even exist?")
        except self.rlc.VoltageInvalid:
            self.errorMsg.showMessage("Need to specify voltage")
        except self.rlc.PowerInvalid:
            self.errorMsg.showMessage("Need to specify real and/or reactive power")
        except self.rlc.FrequencyInvalid:
            self.errorMsg.showMessage("Need to specify frequency with reactive power")

    def _on_rlc_entry_ac_volts__valueChanged(self):
        print("Ac Volts entered:", self.sender().value())
        self.rlc.set_ac_rms_volts(self.sender().value())

    def _on_rlc_entry_freq__valueChanged(self):
        print("Frequency entered:", self.sender().value())
        self.rlc.set_ac_freq(self.sender().value())

    def _on_rlc_entry_reactive_pwr__valueChanged(self):
        print("Reactive power entered:", self.sender().value())
        self.rlc.set_reactive_pwr(self.sender().value())

    def _on_rlc_entry_real_pwr__valueChanged(self):
        print("Real power entered:", self.sender().value())
        self.rlc.set_real_pwr(self.sender().value())

    # SAS tab
    def _on_sas_butt_off__clicked(self):
        print("SAS off was clicked")
        self.sas.turn_off()
    
    def _on_sas_butt_on__clicked(self):
        print("SAS on was clicked")
        self.sas.turn_on()
        
    def _on_sas_butt_apply__clicked(self):
        print("Apply was clicked")
        self.sas.apply()

    def _on_sas_entry_irrad__valueChanged(self):
        print("Irradiance entered:", self.sender().value())
        self.sas.set_irrad(self.sender().value())

    def _on_sas_entry_ff__valueChanged(self):
        print("Fill Factor entered:", self.sender().value())
        self.sas.set_ff(self.sender().value())

    def _on_sas_entry_pmp__valueChanged(self):
        print("Pmp entered:", self.sender().value())
        self.sas.set_pmp(self.sender().value())

    def _on_sas_entry_vmp__valueChanged(self):
        print("Vmp entered:", self.sender().value())
        self.sas.set_vmp(self.sender().value())
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())