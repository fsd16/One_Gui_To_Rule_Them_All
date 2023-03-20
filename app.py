import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui.ui_One_Gui_To_Rule_Them_All import Ui_MainWindow
from logic.pps import PPS

import smartside.signal as smartsignal

class MainWindow(QMainWindow, Ui_MainWindow, smartsignal.SmartSignal, PPS):
    def __init__(self, *args, **kwargs):
        super().__init__(("GPIB0::1::INSTR"), *args, **kwargs)
        self.setupUi(self)
        
        self.auto_connect()
    
    
    _closers = 'butt_close, butt_close_2, butt_close_3'
    def _on_closers__pressed(self):
        print("Close was pressed")
        sys.exit(app.exec_())
    
    # PPS Tab
    def _on_butt_ac_off__pressed(self):
        print("AC off was pressed")
    
    def _on_butt_ac_on__pressed(self):
        print("AC on was pressed")
    
    def _on_butt_apply__pressed(self):
        self.pps_apply()
        print("Apply was pressed")
        
    def _on_check_abnormal__stateChanged(self):
        print ('Check is', self.sender().isChecked())

    def _on_entry_ac_volts__valueChanged(self):
        print("Ac Volts entered:", self.sender().value())

    def _on_entry_freq__valueChanged(self):
        print("Frequency entered:", self.sender().value())
        
    def _on_entry_step_size__valueChanged(self):
        print("Step size entered:", self.sender().value())
        self.entry_ac_volts.setSingleStep(self.sender().value())
        
    def _on_radio_single__clicked(self):
        print("Single is selected")
    
    def _on_radio_split__clicked(self):
        print("Split is selected")
    
    def _on_radio_three__clicked(self):
        print("Three is selected")
        
    # Scope tab
    def _on_butt_apply_lab__pressed(self):
        print("Apply was pressed")
    
    def _on_butt_cap__pressed(self):
        print("AC off was pressed")
        
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
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())