import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QErrorMessage

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
        
        self.ac_menu_abnormal.addItems(self.ac_src.AB_WAVEFORMS)
        self.ac_menu_phase.addItems(self.ac_src.PROFILES)
        
        self.auto_connect()    
    
    _closers = 'sas_butt_close, ac_butt_close, scope_butt_close, rlc_butt_close'
    def _when_closers__clicked(self):
        print("Close was clicked")
        sys.exit()
    
    # AC Tab
    def _on_ac_butt_off__clicked(self):
        print("AC off was clicked")
        self.ac_src.ac_off()
    
    def _on_ac_butt_on__clicked(self):
        print("AC on was clicked")
        self.ac_src.ac_on()
        
    def _on_ac_butt_apply__clicked(self):
        print("Apply was clicked")
        
        if self.ac_check_abnormal.isChecked():
            self.ac_src.ac_apply_abnormal()
        else:
            self.ac_src.ac_apply()
        
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
        self.scope.scope_label()
    
    def _on_scope_butt_cap__clicked(self):
        print("Capture was clicked")
        self.scope.scope_capture()
        
    def _on_scope_check_auto__stateChanged(self):
        print ('Check is', self.sender().isChecked())
        
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
        self.rlc.rlc_off()
    
    def _on_rlc_butt_on__clicked(self):
        print("RLC on was clicked")
        try:
            self.rlc.rlc_on()
            self.rlc_entry_real_pwr.setValue(round(self.rlc.RLC_VALUES["real_pwr"]))
            self.rlc_entry_reactive_pwr.setValue(round(self.rlc.RLC_VALUES["reactive_pwr"]))
        except self.rlc.NoInput:
            self.errorMsg.showMessage("Why do I even exist?")
        except self.rlc.VoltageInvalid:
            self.errorMsg.showMessage("Need to specify voltage")
        except self.rlc.PowerInvalid:
            self.errorMsg.showMessage("Need to specify real and/or reactive power")
        except self.rlc.FrequencyInvalid:
            self.errorMsg.showMessage("Need to specify frequency with reactive power")

    def _rlc_on_entry_ac_volts__valueChanged(self):
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
        self.sas.sas_off()
    
    def _on_sas_butt_on__clicked(self):
        print("SAS on was clicked")
        self.sas.sas_on()
        
    def _on_sas_butt_apply__clicked(self):
        print("Apply was clicked")
        self.sas.sas_apply()

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