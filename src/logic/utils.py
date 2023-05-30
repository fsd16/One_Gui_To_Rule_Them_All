from typing import Dict, Any, TypeVar
from pathlib import Path

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