from iSYS5020_API.radar_enums import TargetListInterface
#spi interface class to receive the targets list
class SPIInterface:
    def __init__(self,radar_obj,bus,device):
        self.bus =bus
        self.device = device
        self.type = TargetListInterface.SPI

    def parsing_TargetsList():
        pass
    
