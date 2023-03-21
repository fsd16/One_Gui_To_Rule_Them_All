import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui.ui_One_Gui_To_Rule_Them_All import Ui_MainWindow
from logic.pps import PPS_308_Bench

import smartside.signal as smartsignal

class MainWindow(QMainWindow, Ui_MainWindow, smartsignal.SmartSignal): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.ac_source = PPS_308_Bench("GPIB0::1::INSTR")
        
        self.menu_abnormal.addItems(self.ac_source.AB_WAVEFORMS)
        self.menu_phase.addItems(self.ac_source.PROFILES)
        
        self.auto_connect()
        
    
    _closers = 'butt_close, butt_close_2, butt_close_3'
    def _when_closers__clicked(self):
        print("Close was clicked")
        sys.exit()
    
    # PPS Tab
    def _on_butt_ac_off__clicked(self):
        print("AC off was clicked")
        self.ac_source.pps_off()
    
    def _on_butt_ac_on__clicked(self):
        print("AC on was clicked")
        self.ac_source.pps_on()
        
    def _on_butt_apply__clicked(self):
        print("Apply was clicked")
        
        if self.check_abnormal.isChecked():
            self.ac_source.pps_apply_abnormal()
        else:
            self.ac_source.pps_apply()
        
    def _on_check_abnormal__stateChanged(self):
        print ('Abnormal was checked', self.sender().isChecked())

    def _on_entry_ac_volts__valueChanged(self):
        print("Ac Volts entered:", self.sender().value())
        self.ac_source.set_ac_rms_volts(self.sender().value())

    def _on_entry_freq__valueChanged(self):
        print("Frequency entered:", self.sender().value())
        self.ac_source.set_ac_freq(self.sender().value())
        
    def _on_entry_step_size__valueChanged(self):
        print("Step size entered:", self.sender().value())
        self.entry_ac_volts.setSingleStep(self.sender().value())
    
    def _on_menu_abnormal__activated(self):
        print("Abnormal waveform selected:", self.sender().currentText())
        self.ac_source.set_ab_waveform(self.sender().currentText())
        
    def _on_menu_phase__activated(self):
        print("Profile selected:", self.sender().currentText())
        # self.ac_source.set_ac_profile(self.sender().currentText())
        profile = self.ac_source.PROFILES[self.sender().currentText()]
        self.entry_ac_volts.setValue(profile[0])
        self.entry_freq.setValue(profile[1])
        
        if profile[2] == "split":
            self.radio_split.setChecked(True)
        elif profile[2] == "single":
            self.radio_single.setChecked(True)
        elif profile[2] == "three":
            self.radio_three.setChecked(True)

    def _on_radio_single__toggled(self):
        if self.radio_single.isChecked():
            print("Single is selected")
            self.ac_source.set_ac_config("single")
            
    def _on_radio_split__toggled(self):
        if self.radio_split.isChecked():
            print("Split is selected")
            self.ac_source.set_ac_config("split")
            
    def _on_radio_three__toggled(self):
        if self.radio_three.isChecked():
            print("Three is selected")
            self.ac_source.set_ac_config("three")
        
    # Scope tab
    def _on_butt_apply_lab__pressed(self):
        print("Apply labels was pressed")
    
    def _on_butt_cap__pressed(self):
        print("Capture was pressed")
        
    def _on_check_auto__stateChanged(self):
        print ('Check is', self.sender().isChecked())
        
    def _on_check_date__stateChanged(self):
        print ('Check is', self.sender().isChecked())

    def _on_check_invert__stateChanged(self):
        print ('Check is', self.sender().isChecked())
    
    def _on_line_cap_name__editingFinished(self):
        print("Capture name entered:", self.sender().text())

    def _on_line_cap_path__editingFinished(self):
        print("Capture path entered:", self.sender().text())
    
    def _on_line_ch1_lab__editingFinished(self):
        print("CH1 label entered:", self.sender().text())
        
    def _on_line_ch2_lab__editingFinished(self):
        print("CH2 label entered:", self.sender().text())
        
    def _on_line_ch3_lab__editingFinished(self):
        print("CH3 label entered:", self.sender().text())
        
    def _on_line_ch4_lab__editingFinished(self):
        print("CH4 label entered:", self.sender().text())
        
    # RLC tab
    def _on_butt_rlc_off__pressed(self):
        print("RLC off was pressed")
    
    def _on_butt_rlc_on__pressed(self):
        print("RLC on was pressed")

    def _on_entry_ac_volts_2__valueChanged(self):
        print("Ac Volts entered:", self.sender().value())

    def _on_entry_freq_2__valueChanged(self):
        print("Frequency entered:", self.sender().value())
        
    def _on_entry_reactive_pwr__valueChanged(self):
        print("Reactive power entered:", self.sender().value())

    def _on_entry_real_pwr__valueChanged(self):
        print("Real power entered:", self.sender().value())
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())