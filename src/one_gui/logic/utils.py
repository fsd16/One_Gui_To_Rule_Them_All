from typing import Dict, Any, TypeVar
from pathlib import Path
from serial.tools.list_ports import comports
from pyvisa import ResourceManager

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