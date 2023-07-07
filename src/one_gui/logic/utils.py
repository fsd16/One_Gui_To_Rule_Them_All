# Finn Drabsch
# Enphase Energy
# 2023

from typing import Dict, Any, TypeVar
from pathlib import Path
from serial.tools.list_ports import comports
from pyvisa import ResourceManager
import importlib

KeyType = TypeVar('KeyType')

def dict_value_to_index(dict, value):
    return list(dict.values()).index(value)


def deep_update(mapping: Dict[KeyType, Any], *updating_mappings: Dict[KeyType, Any]) -> Dict[KeyType, Any]:
        updated_mapping = mapping.copy()
        for updating_mapping in updating_mappings:
            for k, v in updating_mapping.items():
                if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
                    updated_mapping[k] = deep_update(updated_mapping[k], v)
                else:
                    updated_mapping[k] = v

        return updated_mapping

# Ensure file name is unique
def uniquify(filepath):
    filepath_P = Path(filepath)
    counter = 1

    while filepath_P.exists():
        filepath_P = f"{filepath_P.stem} ({counter}){filepath_P.suffix}"
        counter += 1

    return filepath_P

def discover_addresses():
    """
    Generates a list of com ports and gpib addresses

    Returns:
        A sorted list of the available com and GPIB ports
    """
    # fetch a list of ListPortInfo object
    all_serial_port_info = comports()
    try:
        all_visa_addresses = ResourceManager().list_resources()
    except ValueError:
        all_visa_addresses = []

    # extract device name(path) from the list
    filtered_addresses = [port_info.device for port_info in all_serial_port_info]
    filtered_addresses += [address for address in all_visa_addresses if 'GPIB' in address]
    return sorted(filtered_addresses)

def import_class_from_string(path):
    '''Takes `path`, a string, and returns a class.'''
    module = '.'.join(path.split('.')[:-1])
    class_ = path.split('.')[-1]
    imported_module = importlib.import_module(name=module)
    return getattr(imported_module, class_)

class DummyClass:
    """Class to to be used as a dummy. Ideal behaviour is any interaction with the class does nothing. Not perfect when a specific return is expected 
    """

    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, key):
        return [0]
    
    def __iter__(self):
        while True:
            yield None

    def __getattribute__(self, name):
        return self
    
    def __getattr__(self, name):
        return self

    def __setattr__(self, name, value):
        pass

    def __delattr__(self, name):
        pass

    def __call__(self, *args, **kwargs):
        return self