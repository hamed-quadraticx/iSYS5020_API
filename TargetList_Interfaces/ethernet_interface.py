#imports
import logging
import multiprocessing
import threading
import socket
import sys
import time

from iSYS5020_API.radar_enums import TargetListInterface

from datetime import datetime
from .target_list_header import Target_List_Header
from .target_Data_Packet import Target_Data_Packet, Target_Data

logging.basicConfig(format='%(levelname)s - %(asctime)s : %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)



# ethernet interface to receive the targets list 
class EhternetInterface:
    def __init__(self,radar_obj,enable_log=False):
        self.radar_obj = radar_obj
        self.enable_log = enable_log
        self.type = TargetListInterface.ETH
        self.udp_socket =  socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        logging.info(f'init radar udp socket.')
        _address = (radar_obj.destination_ip,radar_obj.destination_targetlist_portno)
        logging.info(f'socket data : {radar_obj.destination_ip}, {radar_obj.destination_targetlist_portno}')
        self.udp_socket.bind(_address)
        logging.info(f'radar udp socket binding to {radar_obj.destination_ip} : {radar_obj.destination_targetlist_portno}')

        if enable_log :
            now = datetime.now()
            log_file_name='targetList_'+str(now)+'.txt'
            print("file name =", log_file_name)
            log_file_obj = open(log_file_name, "x")
            log_file_obj.write("Target list :")




    def parsing_TargetList(self):
        data , addr = self.udp_socket.recvfrom(1024)
        logging.info(f'parsing_TargetList: received from {addr} = {(" , ".join(format(x, "02x") for x in data))} ')

        if self.enable_log :
            log_file_obj.write("\n")
            log_file_obj.write(f'{str(datetime.now())} : received from {addr} = \n {(" , ".join(format(x, "02x") for x in data))}')
        
        header_obj = Target_List_Header(data)
        chk_valid_header = header_obj.parse()

        if chk_valid_header and header_obj.no_of_packets > 0 and header_obj.no_of_targets > 0 :
            data , addr = self.udp_socket.recvfrom(1024)
            logging.info(f'parsing_TargetList: received from {addr} = {(" , ".join(format(x, "02x") for x in data))} ')

            if self.enable_log :
                log_file_obj.write("\n")
                log_file_obj.write(f'{str(datetime.now())} : received from {addr} = \n {(" , ".join(format(x, "02x") for x in data))}')

            data_packet = Target_Data_Packet( self.radar_obj, header_obj.frame_id,header_obj.no_of_packets, header_obj.no_of_targets, data)
            data_packet.parse()

            





        


        

