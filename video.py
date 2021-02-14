import cv2
from socket import socket,AF_INET,SOCK_DGRAM
from time import sleep

addr = ("192.168.10.1",8889)
vaddr = ("192.168.10.1",11111)


drone = socket(AF_INET,SOCK_DGRAM)
drone.bind(addr)
server = socket(AF_INET,SOCK_DGRAM)
server.bind(("192.168.10.2",8889))


server.sendto("command".encode("utf-8"),addr)

sleep(2)

video = socket(AF_INET,SOCK_DGRAM)
video.bind(vaddr)


