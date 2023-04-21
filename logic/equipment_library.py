class EquipmentDrivers:
    def __init__(self):
        print("init")
        self.AC_SOURCE_DRIVERS = {
            "PPS_308": 'enphase_equipment.ac_source.pacific_power_source.PPS_308',
            "AmetekAsterion": 'enphase_equipment.ac_source.ametek.AmetekAsterion'
        }

        self.SCOPE_DRIVERS = {
            "DSO-X 3034A": 'enphase_equipment.oscilloscope.agilent.AgilentDSOX3034A',
            "DSO-X 3034T": 'enphase_equipment.oscilloscope.agilent.AgilentDSOX3034A',
            "MSO-X 3034A": 'enphase_equipment.oscilloscope.agilent.AgilentMSOX3034A',
            "MSO-X 3034T": 'enphase_equipment.oscilloscope.agilent.AgilentMSOX3034A',
        }

        self.RLC_DRIVERS = {
            "RLC-700": 'enphase_equipment.rlc_load.enphase_rlc_v2.EnphaseRLCV2'
        }

        self.SAS_DRIVERS = {
            "E4360A": 'enphase_equipment.solar_array_simulator.agilent.AgilentE4360A'
        }