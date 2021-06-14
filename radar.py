import time
import serial
import binascii
import copy
# Importing the threading module
import threading 
from RadarAPI.TargetList_Interfaces.ethernet_interface import EhternetInterface
from RadarAPI.TargetList_Interfaces.spi_interface import SPIInterface


from .radar_enums import TargetListInterface

from .get_address import GetAddress_req
from .get_name import GetName_req
from .get_ethernetconfig import GetEthernetConfig_req
from .get_destinationIP import GetDestinationIP_req
from .start_acq import StartAcq_req
from .stop_Acq import StopAcq_req
from .get_targetlist_interface import Get_TargetListInterface_req
from .radar_enums import Save_Location,TargetListInterface
from .set_address import SetAddress_req
from .set_ethernetConfig import SetEthernetConfig_req
from .set_destinationIP import SetDestinationIP_req
from .set_targetlist_Interface import SetTargetListInterface_req




  
# radar class holds all radar data and defines the configuration port which will be used to configure the radar
class Radar :
    serial_port = None
    lock = threading.Lock()
    def __init__(self,uart_port_name,address_no):
        
        self.serial_port = serial.Serial(port=uart_port_name,
                                         baudrate=115200,
                                         bytesize=serial.EIGHTBITS,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,)

        # basic attributes
        self.address_no = address_no
        self.name ='NA'
        ####
        # Device ethernet configuration 
        self.IP_address ='NA'
        self.subnet_mask='NA'
        self.gateway='NA'
        ####
        # destination ip address for the device which will receive the target list 
        self.destination_ip =''
        self.destination_targetlist_portno=0
        self.destination_rec_portno=0
        ####
        self.targetlist_interface_type = TargetListInterface.off
        self._TargetList = []
        self.interface_obj = None



    # apply the strategy design pattern for target list interface due to the two interfaces availabel to get the targets list (SPI , Ethernet)
    def set_targetList_interface(self,data_loc,interface_obj):
        req = SetTargetListInterface_req(self,data_loc,TargetListInterface(interface_obj).value)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False

        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('set radar target list interface failed')
            return
        
        if interface_obj is TargetListInterface.ETH :
             self.interface_obj =ethernet_interface.EhternetInterface(self)
             print(' set radar target list interface ETH !!!!')
        elif interface_obj is TargetListInterface.SPI :
             self.interface_obj =spi_interface.SPIInterface(self,0, 0)
             print(' set radar target list interface SPI !!!!')

        
   
    def get_targetlist_interface(self,data_loc):
        req = Get_TargetListInterface_req(self,data_loc)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False
        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('get radar target list interface was failed')
            return
       
        print('Radar target list interface type is {}'.format(self.targetlist_interface_type))
        
    def get_radar_name(self):
        req = GetName_req(self)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False
        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('get radar name failed')
            return
        
        print('Radar name is {}'.format(self.name))

    def set_radar_address(self,new_address):
        req = SetAddress_req(self,new_address)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False

        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('set radar address failed')
            return
        
        self.address_no = new_address
        print(' the new Radar address is {}'.format(self.address_no))

    def get_radar_address(self):
        req = GetAddress_req(self)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False
        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('get radar address failed')
            return
        
        print('Radar address is {}'.format(self.address_no))
       
    def get_IP_Configuration(self,data_loc):
        req = GetEthernetConfig_req(self,data_loc)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False
        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('get radar ethernet configuration failed')
            return
        
        print('Radar ip is {}'.format(self.IP_address))
        print('Radar subnet mask is {}'.format(self.subnet_mask))
        print('Radar gateway is {}'.format(self.gateway))

    def set_IP_Address(self, data_loc,new_ip_address,new_subnet_mask, new_gateway):
        req = SetEthernetConfig_req(self,data_loc,new_ip_address,new_subnet_mask, new_gateway)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False

        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('set radar ethernet configuration failed')
            return

        self.IP_address = new_ip_address
        self.gateway = new_gateway
        self.subnet_mask = new_subnet_mask
        print(' set radar ethernet configuration done !!!!')

    def get_destination_IP(self,data_loc):
        req = GetDestinationIP_req(self,data_loc)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False
        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('get radar destination ethernet configuration failed')
            return
        
        print('Radar destination device ip is {}'.format(self.destination_ip))
        print('Radar target list port is {}'.format(self.destination_targetlist_portno))
        print('Radar record target list port is {}'.format(self.destination_rec_portno))
        
    def set_destination_IP(self,data_loc,dest_ip_address,list_portno, rec_portno):
        req = SetDestinationIP_req(self,data_loc,dest_ip_address,list_portno, rec_portno)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False

        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('set radar edestination IP failed')
            return
        self.destination_ip = dest_ip_address
        self.destination_targetlist_portno = list_portno
        self.destination_rec_portno =rec_portno
        print(' set radar destination IP done !!!!')    
    
    def start_acquisition(self):
        req = StartAcq_req(self)
        msgarr = req.send_req_message()
        if msgarr is None :
            print('failed to send req or receive response ')
            return False
        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('start acq failed')
            return
        
        print('acq started !!')
        
    def stop_acquisition(self):
        req = StopAcq_req(self)
        msgarr = req.send_req_message(10)
        if msgarr is None :
            print('failed to send req or receive response ')
            return False
        chk = req.validate_received_rawdata(msgarr)
        if chk is False :
            print('stop acq failed')
            return
        
        print('acq stopped !!')
        
    def parsing_TargetsList(self):
        self.interface_obj.parsing_TargetList()
    
    def add_target(self,target_obj):
        if target_obj is None :
            return False
        lock.acquire()
        self._TargetList.append(target_obj)
        lock.release()
        return True

    def get_TargetList(self):
        lock.acquire()
        temp_list = copy.deepcopy(self._TargetList) 
        lock.release()
        return temp_list


    # method use to write the request message raw bytes and receive the incoming response raw data to be validate later
    def wrire_Req_read_response(self,msg_arr,delay_value=0.1):
        if msg_arr is None:
            return False
        received_data=[]
        try:
            self.serial_port.write(msg_arr)
            time.sleep(delay_value)

            while  self.serial_port.inWaiting() > 0 :
                read_byte = self.serial_port.read(size=1)
                #hex_string = binascii.hexlify(read_byte).decode('utf-8')
                received_data.append(read_byte[0])
            
            self.serial_port.flush()
            self.serial_port.flushInput()
            self.serial_port.flushOutput()
        except KeyboardInterrupt:
            print("application was closed by user request")
            return False

        except Exception as exception_error:
            print("Error occurred")
            print("Error: " + str(exception_error))
            return False
        
        return received_data

############################################################################################################################################################

############################################################################################################################################################







