from .abstract_radar_req_message import ReqMessage
from .abstract_radar_response_message import ResponseMessage





################################## class for request ########################################
class  SetEthernetConfig_req(ReqMessage):
   def __init__(self,radar_obj, data_loc,new_ip_address,new_subnet_mask, new_gateway):
      self.radar_obj = radar_obj
      self.data_loc =data_loc

      self.SD = 0x68
      self.LE = 0x12
      self.LEr =0x12
      # destination address will be the radar address the default address for isys5020 is hex = 0x64 dec =100
      if radar_obj is None:
        self.DA = 0x64 
      else :
        self.DA = radar_obj.address_no

      self.SA = 0x01 # master address = 1
      self.FC = [0xD3,0x00,0x29,self.data_loc]
      ### add new  ethernet data to the FC arraylist
      if new_gateway =='' or new_ip_address  =='' or new_subnet_mask =='':
          print('invalid ethernet config')
          return
      
      ip_ls =[]
      subnet_ls =[]
      gateway_ls=[]

      ip_ls = new_ip_address.split('.')
      subnet_ls = new_subnet_mask.split('.')
      gateway_ls = new_gateway.split('.')

      if len(ip_ls) != 4 or len(subnet_ls) != 4 or len(gateway_ls) != 4 :
          print('invalid ethernet configurations')
          return
      
      [self.FC.append(int(i)) for i in ip_ls]
      [self.FC.append(int(i)) for i in subnet_ls]
      [self.FC.append(int(i)) for i in gateway_ls]
    
      self.FCS = 0x00
      self.ED = 0x16

    
   def validate_received_rawdata(self,msg_arr):
      setethernet_response_obj = SetEthernetConfig_response(self.radar_obj,msg_arr)
      is_valid =  setethernet_response_obj.validate_msg()
      if is_valid is False:
          print('invalid ethernet configuration response message')
          return False
    
      print ('device ethernet configuration was changed !!!')
      return True







############################################## class for response ########################
class SetEthernetConfig_response(ResponseMessage):
    def __init__(self,radar_obj,msg):
      self.radar_obj = radar_obj

      self.msg_arr = msg
      self.SD = 0x68
      self.LE = 0x03
      self.LEr =0x03
      self.DA = 0x01 # master address =1
      self.SA = 0x64 # default isys5020 radar address
      if radar_obj is not  None :
          self.SA = radar_obj.address_no

      self.FC = 0xD3
      self.PDU = []
      self.FCS = 0x00
      self.ED =  0x16


    #overrider for the validation function
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

      print('received a valid set device ethernet configuration Ack message !!')
      return True







