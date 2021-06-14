import enum

class Save_Location(enum.Enum):
   RAM = 0
   EEPROM = 1

class TargetListInterface(enum.Enum):
   off=0
   SPI = 1
   ETH = 2