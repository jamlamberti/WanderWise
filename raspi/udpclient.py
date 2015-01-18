import socket

# This is an example of a UDP client - it creates
# a socket and sends data through it

# create the UDP socket
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

data = "Did you hear me?\n"

# Simply set up a target address and port ...
raspiaddrstr = "158.130.161.107"
macbookaddrstr = "158.130.166.62"

addr = (raspiaddrstr,9999)

# ... and send data out to it!
UDPSock.sendto(data,addr)
