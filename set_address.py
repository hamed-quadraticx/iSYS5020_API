from .abstract_radar_req_message import ReqMessage
from .abstract_radar_response_message import ResponseMessage


################################################## class for request  ############################################################
class SetAddress_req(ReqMessage):
   def __init__(self,radar_obj,new_address):
      self.radar_obj = radar_obj
      self.SD = 0x68
      self.LE = 0x07
      self.LEr =0x07
      self.DA = radar_obj.address_no 
      self.SA = 0x01 # master address = 1
      self.FC = [0xD3,0x00,0x01,0x00]
      self.FC.append(new_address)
      self.FCS = 0x00
      self.ED = 0x16
   
   def validate_received_rawdata(self,msg_arr):
      setaddress_response_obj = SetAddress_response(self.radar_obj,msg_arr)
      is_valid =  setaddress_response_obj.validate_msg()
      if is_valid is False:
         print('invalid set address response message')
         return False
      
      return True










###################################################### class for response ###################################################33
class SetAddress_response(ResponseMessage):
   def __init__(self,radar_obj,msg):
      self.radar_obj = radar_obj

      self.msg_arr = msg
      self.SD = 0x68
      self.LE = 0x03
      self.LEr =0x03
      self.DA = 0x01 # master address =1
      self.SA = radar_obj.address_no # radar address
      self.FC = 0xD3
      self.PDU = []
      self.FCS = 0x00
      self.ED =  0x16

   def validate_msg(self):
     
      if self.msg_arr is None or len(self.msg_arr) != 9 :
         return False

      if  self.SD in self.msg_arr is False :
         return False
      
      if self.ED in self.msg_arr is False :
         return False

      startIndex = self.msg_arr.index(self.SD) 
     
      print('start index =  {}'.format(startIndex))
      print ('self LE = {}'.format(hex(self.LE)))
      print ('msg LE = {}'.format(hex(self.msg_arr[startIndex+1])))

      print ('self LEr = {}'.format(hex(self.LEr)))
      print ('msg LEr = {}'.format(hex(self.msg_arr[startIndex+2])))

      print ('self SD = {}'.format(hex(self.SD)))
      print ('msg SD = {}'.format(hex(self.msg_arr[startIndex+3])))

      print ('self DA = {}'.format(hex(self.DA)))
      print ('msg DA = {}'.format(hex(self.msg_arr[startIndex+4])))

      print ('self ED = {}'.format(hex(self.ED)))
      print ('msg ED = {}'.format(hex(self.msg_arr[startIndex+8])))

      print ('self FC = {}'.format(hex(self.FC)))
      print ('msg FC = {}'.format(hex(self.msg_arr[startIndex+6])))

      if self.LE != self.msg_arr[startIndex+1] or  self.LEr != self.msg_arr[startIndex+2]  or  self.SD != self.msg_arr[startIndex+3] or self.DA != self.msg_arr[startIndex+4] or self.FC != self.msg_arr[startIndex+6] or self.ED != self.msg_arr[startIndex+8] :
         print('not matched response message array')
         return False
      
      self.SA = self.msg_arr[startIndex+5]
    
      self.calculate_check_sum()
      print('the received check sum is  : {}'.format( self.msg_arr[startIndex+7]))
      print('the calculated check sum is : {}'.format(self.FCS))
      if self.FCS  != self.msg_arr[startIndex+7] :
        print('check sum is not matched ')
        return False

      print('received a valid set address Ack !!')
      return True


      
        
      
      

      


    