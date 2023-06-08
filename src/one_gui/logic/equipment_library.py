import importlib

class EquipmentDrivers:
    def __init__(self):
        self.AC_SOURCE_DRIVERS = {
            "None": None,
            "PPS_308": 'enphase_equipment.ac_source.pacific_power_source.PPS_308',
            "AmetekAsterion": 'enphase_equipment.ac_source.ametek.AmetekAsterion'
        }

        self.SCOPE_DRIVERS = {
            "None": None,
            "DSO-X 3034A": 'enphase_equipment.oscilloscope.agilent.AgilentDSOX3034A',
            "DSO-X 3034T": 'enphase_equipment.oscilloscope.agilent.AgilentDSOX3034A',
            "MSO-X 3034A": 'enphase_equipment.oscilloscope.agilent.AgilentMSOX3034A',
            "MSO-X 3034T": 'enphase_equipment.oscilloscope.agilent.AgilentMSOX3034A',
        }

        self.RLC_DRIVERS = {
            "None": None,
            "RLC-700": 'enphase_equipment.rlc_load.enphase_rlc_v2.EnphaseRLCV2'
        }

        self.SAS_DRIVERS = {
            "None": None,
            "E4360A": 'enphase_equipment.solar_array_simulator.agilent.AgilentE4360A'
        }

        self.CHAMBER_DRIVERS = {
            "None": None,
            "WatlowF4": 'enphase_equipment.thermal_chamber.watlow.WatlowF4',
            "Espec": 'enphase_equipment.thermal_chamber.espec.Espec',
            "Thermotron": 'enphase_equipment.thermal_chamber.thermotron_v2.Thermotron',
        }

def import_class_from_string(path):
    '''Takes `path`, a string, and returns a class.'''
    module = '.'.join(path.split('.')[:-1])
    class_ = path.split('.')[-1]
    imported_module = importlib.import_module(name=module)
    return getattr(imported_module, class_)