#-*- coding:utf-8 -*-
#/usr/python2
#发送网络数据包

import socket
import struct
import sys

ip = sys.argv[1]
input_file = sys.argv[2]  #读取报文数据

fp = open(input_file)
buf = fp.read()

print ("[+] sending buffer size", len(buf))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, 80))
s.send(buf)
print(buf)
resp = s.recv(2048)
print(resp)

#http格式及注意事项
'''
Content-Length: 报文大小包括换行
'''