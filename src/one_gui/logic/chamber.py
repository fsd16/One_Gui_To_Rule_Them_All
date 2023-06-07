from logic.equipment_library import import_class_from_string

class Chamber():
    def __init__(self, driver_path, *args, **kwargs):
        parent_class = import_class_from_string(driver_path)
        self.__class__ = type(self.__class__.__name__,
                            (parent_class, object),
                            dict(self.__class__.__dict__))
            
        super(self.__class__, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    chamber = Chamber('enphase_equipment.thermal_chamber.watlow.WatlowF4', 2)
    chamber.set_temperature(25)
    chamber.close()