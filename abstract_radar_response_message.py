from abc import ABC, abstractmethod

#abstract class used to define radar request messages
class ResponseMessage(ABC):
    def __init__(self,msg):
        self.msg_arr = msg
        self.SD = 0x00
        self.LE = 0x00
        self.LEr =0x00
        self.DA = 0x00 
        self.SA = 0x00
        self.FC = 0x00
        self.PDU = [0x00]
        self.FCS = 0x00
        self.ED = 0x00

   
    
    #function used to calcualte response message check sum
    def calculate_check_sum(self):
        print('start calculate check sum')
        self.FCS = self.FCS + self.FC
        self.FCS = self.FCS +self.DA 
        self.FCS = self.FCS  + self.SA
        for i in self.PDU :
            self.FCS =self.FCS  + i 
           
        self.FCS =self.FCS & 0xFF

        print('the Check sum = {}'.format(hex(self.FCS)))


    @abstractmethod
    def validate_msg(self):
        pass

   
        
        
            












