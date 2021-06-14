from .abstract_radar_req_message import ReqMessage
from .abstract_radar_response_message import ResponseMessage


################################################## class for request  ############################################################
class GetAddress_req(ReqMessage):
   def __init__(self,radar_obj):
      self.radar_obj = radar_obj
      self.SD = 0x68
      self.LE = 0x05
      self.LEr =0x05
      self.DA = 0x00 # 0 for broadcast address
      self.SA = 0x01 # master address = 1
      self.FC = [0xD2,0x00,0x01]
      self.FCS = 0x00
      self.ED = 0x16
   
   def validate_received_rawdata(self,msg_arr):
      getaddress_response_obj = GetAddress_response(self.radar_obj,msg_arr)
      is_valid =  getaddress_response_obj.validate_msg()
      if is_valid is False:
         print('invalid get address response message')
         return False
      
      self.radar_obj.address_no  = int.from_bytes(getaddress_response_obj.PDU,"big")
      return True










###################################################### class for response ###################################################33
class GetAddress_response(ResponseMessage):
   def __init__(self,radar_obj,msg):
      self.radar_obj = radar_obj

      self.msg_arr = msg
      self.SD = 0x68
      self.LE = 0x05
      self.LEr =0x05
      self.DA = 0x01 # master address =1
      self.SA = 0x00 # radar address
      self.FC = 0xD2
      self.PDU = [0x00,0x00]
      self.FCS = 0x00
      self.ED =  0x16

   def validate_msg(self):
     
      if self.msg_arr is None or len(self.msg_arr) != 11 :
         return False

      if  self.SD in self.msg_arr is False :
         return False
      
      if self.ED in self.msg_arr is False :
         return False

      startIndex = self.msg_arr.index(self.SD) 
      #print('start index =  {}'.format(startIndex))

      #print ('self LE = {}'.format(hex(self.LE)))
      #print ('msg LE = {}'.format(hex(self.msg_arr[startIndex+1])))
      if self.LE != self.msg_arr[startIndex+1] or  self.LEr != self.msg_arr[startIndex+2]  or  self.SD != self.msg_arr[startIndex+3] or self.DA != self.msg_arr[startIndex+4] or self.FC != self.msg_arr[startIndex+6] or self.ED != self.msg_arr[startIndex+10] :
         print('not matched response message array')
         return False
      
      self.SA = self.msg_arr[startIndex+5]
      #print('response source address {}'.format(self.SA))
      #print('PDU index 0 {}'.format(hex(self.msg_arr[startIndex+7])))
      #print('PDU index 1 {}'.format(hex(self.msg_arr[startIndex+8])))
      self.PDU = [self.msg_arr[(startIndex+7)],self.msg_arr[(startIndex+8)]]


      self.calculate_check_sum()
      print('the received check sum is  : {}'.format(self.msg_arr[startIndex+9]))
      print('the calculated check sum is : {}'.format(self.FCS))
      if self.FCS  != self.msg_arr[startIndex+9] :
         return False

      print('received a valid device address message !!')
      return True



      
        
      
      

      


    