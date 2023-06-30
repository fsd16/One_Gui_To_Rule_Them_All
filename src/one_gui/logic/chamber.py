from one_gui.logic.utils import import_class_from_string

class Chamber:
    def __init__(self, driver_path, address, *args, **kwargs):
        parent_class = import_class_from_string(driver_path)
        self.parent_instance = parent_class(address)
        # self.__class__ = type(self.__class__.__name__,
        #                     (parent_class, object),
        #                     dict(self.__class__.__dict__))
            
        # super(self.__class__, self).__init__(*args, **kwargs)

    def apply(self, temperature):
        self.parent_instance.set_temperature(temperature)
    
    def close(self):
        self.parent_instance.close()
        
class Mock_Chamber:
    def __init__(self, *args, **kwargs):
        pass

    def apply(self, *args, **kwargs):
        pass
    
    def close(self):
        pass

if __name__ == '__main__':
    chamber = Chamber('enphase_equipment.thermal_chamber.watlow.WatlowF4', 2)
    chamber.set_temperature(25)
    chamber.close()