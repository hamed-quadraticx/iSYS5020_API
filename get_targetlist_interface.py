from .abstract_radar_req_message import ReqMessage
from .abstract_radar_response_message import ResponseMessage
import enum
from .radar_enums import Save_Location,TargetListInterface



################################## class for request ########################################
class  Get_TargetListInterface_req(ReqMessage):
   def __init__(self,radar_obj, data_loc):
      self.radar_obj = radar_obj
      self.SD = 0x68
      self.LE = 0x06
      self.LEr =0x06
      # destination address will be the radar address the default address for isys5020 is hex = 0x64 dec =100
      if radar_obj is None:
        self.DA = 0x64 
      else :
        self.DA = radar_obj.address_no

      self.SA = 0x01 # master address = 1
      self.FC = [0xD2,0x00,0x2C,data_loc]
      self.FCS = 0x00
      self.ED = 0x16
    
   def validate_received_rawdata(self,msg_arr):
      getack_response_obj = Get_TargetListInterface_response(self.radar_obj,msg_arr)
      is_valid =  getack_response_obj.validate_msg()
      if is_valid is False:
          print('invalid start acq ack  message')
          return False
     
      temp_no = getack_response_obj.PDU[0]
      print('pdu[0] = {}'.format(temp_no))

      self.radar_obj.targetlist_interface_type  = TargetListInterface(temp_no).name
      return True







############################################## class for response ########################
class Get_TargetListInterface_response(ResponseMessage):
    def __init__(self,radar_obj,msg):
      self.radar_obj = radar_obj

      self.msg_arr = msg
      self.SD = 0x68
      self.LE = 0x04
      self.LEr =0x04
      self.DA = 0x01 # master address =1
      self.SA = 0x64 # default isys5020 radar address
      if radar_obj is not  None :
          self.SA = radar_obj.address_no

      self.FC = 0xD2
      self.PDU = []
      self.FCS = 0x00
      self.ED =  0x16

    #overrider for the validation function
    def validate_msg(self):
     
      if self.msg_arr is None or len(self.msg_arr) != 10 :
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
      print ('msg ED = {}'.format(hex(self.msg_arr[startIndex+9])))

      print ('self FC = {}'.format(hex(self.FC)))
      print ('msg FC = {}'.format(hex(self.msg_arr[startIndex+6])))

      if self.LE != self.msg_arr[startIndex+1] or  self.LEr != self.msg_arr[startIndex+2]  or  self.SD != self.msg_arr[startIndex+3] or self.DA != self.msg_arr[startIndex+4] or self.FC != self.msg_arr[startIndex+6] or self.ED != self.msg_arr[startIndex+9] :
         print('not matched response message array')
         return False
      
      self.SA = self.msg_arr[startIndex+5]
      self.PDU.append(self.msg_arr[(startIndex+7)])
      
      self.calculate_check_sum()
      print('the received check sum is  : {}'.format( self.msg_arr[startIndex+8]))
      print('the calculated check sum is : {}'.format(self.FCS))
      if self.FCS  != self.msg_arr[startIndex+8] :
        print('check sum is not matched ')
        return False

      print('received a valid target list interface Acq Ack message !!')
      return True
