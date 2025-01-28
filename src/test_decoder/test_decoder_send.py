import socket
import struct

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

id = 100
tem = 10.0
is_active = True
state = 1

binary_packet = struct.pack('<H',id)
binary_packet+=struct.pack('<f', tem)
binary_packet+=struct.pack('<B', is_active)
binary_packet+=struct.pack('<B', state)

sock.bind(('127.0.0.1', 8801))
sock.sendto(binary_packet, ('localhost', 8800))

id = 101
pres = 32
binary_packet_1 = struct.pack('<H', id)
binary_packet_1 += struct.pack('<i', pres)
sock.sendto(binary_packet_1, ('localhost', 8800))
