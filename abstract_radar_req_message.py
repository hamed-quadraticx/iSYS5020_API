from abc import ABC, abstractmethod


#abstract class used to define radar request messages
class ReqMessage(ABC):
    def __init__(self,radar_obj):
        self.radar_obj = radar_obj

        self.SD = 0x00
        self.LE = 0x00
        self.LEr =0x00
        self.DA = 0x00 
        self.SA = 0x00
        self.FC = [0x00]
        self.FCS = 0x00
        self.ED = 0x00
   
    
    #function used to calcualte request message check sum
    def calculate_check_sum(self):
        for i in self.FC :
            self.FCS = self.FCS + i
        self.FCS = self.FCS + self.DA
        self.FCS = self.FCS + self.SA
        self.FCS =self.FCS& 0xFF
        print('the Check sum = {}'.format(hex(self.FCS)))

    def build_Req_message(self):
        msg = [self.SD,self.LE,self.LEr,self.SD,self.DA,self.SA]
        for i in self.FC :
            msg.append(i)
        self.calculate_check_sum()
        msg.append(self.FCS)
        msg.append(self.ED)
        return msg

    def send_req_message(self,delay_value=0.1):
        #check if the radar object was initialized
        if self.radar_obj is None :
            return False
        
        msg_arr = self.build_Req_message()
        print('build req message array :')
        print (' , '.join(format(x, '02x') for x in msg_arr))
    
        received_raw_data = self.radar_obj.wrire_Req_read_response(msg_arr,delay_value)
        if received_raw_data is False or received_raw_data is None :
            print('failed to write and read response')
            return None

        print('recived response raw data :')
        print (' , '.join(format(x, '02x') for x in received_raw_data))
        return received_raw_data

    @abstractmethod
    def validate_received_rawdata(self,msg_arr):
        pass
            
        

        
        
            












