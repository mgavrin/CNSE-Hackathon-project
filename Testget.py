# -*- coding: utf-8 -*-
"""
Created on Sat Nov 07 18:58:37 2015

@author: Gaurav Mukherjee
"""

""" Code to port UDP data to a data file"""

""" Read the UDP output"""
import socket
   
UDP_IP = "127.0.0.1"
UDP_PORT = 20101
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
   
while True:
   data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
   print "received message:", data





""" Write the output to a txt"""