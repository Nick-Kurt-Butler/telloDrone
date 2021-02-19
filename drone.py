from keyboard import is_pressed as keydown
from socket import socket,AF_INET,SOCK_DGRAM
from threading import Thread
from time import sleep
import cv2
from os import system
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import MiniBatchKMeans

class Drone:
	def __init__(self):
		ip = "192.168.10.1"
		self.addr = (ip,8889)
		self.video_addr = ("192.168.10.3",11111)
		self.server = socket(AF_INET,SOCK_DGRAM)
		self.server.bind(("192.168.10.3",8889))
		self.x,self.y,self.z,self.t = (0,0,0,0)
		self.in_air = 0
		print("Waiting for ok response")
		self.send("command")
		while self.recv() != "ok":
			self.send("command")
		print("Drone Initiated")

		Thread(target=self.stream,daemon=True).start()
		Thread(target=self.recv_loop,daemon=True).start()
		self.run()

	def run(self):
		Thread(target=self.stay_alive,daemon=True).start()
		Thread(target=self.update,daemon=True).start()
		while not(keydown("q")):
			self.move()
		self.kill()

	def kill(self):
		self.send("emergency")

	def move(self):
		if keydown("space"):
			self.send("takeoff")
			sleep(1)
		if keydown("z"):
			sleep(.1)
			self.send("flip l")
			sleep(.1)
		if keydown("x"):
			sleep(.1)
			self.send("flip f")
			sleep(.1)
		if keydown("c"):
			sleep(.1)
			self.send("flip r")
			sleep(.1)
		if keydown("v"):
			sleep(.1)
			self.send("flip b")
			sleep(.1)
		if keydown("l"):
			self.send("land")
		if keydown("right") and self.x < 100:
			self.x += 1
		if keydown("left") and self.x > -100:
			self.x -= 1
		if keydown("up") and self.y < 100:
			self.y += 1
		if keydown("down") and self.y > -100:
			self.y -= 1
		if keydown("w") and self.z < 100:
			self.z += 1
		if keydown("s") and self.z > -100:
			self.z -= 1
		if keydown("d") and self.t < 100:
			self.t += 1
		if keydown("a") and self.t > -100:
			self.t -= 1

	def takeoff(self):
		self.send("takeoff")
		self.in_air = 1

	def land(self):
		self.send("land")
		self.in_air = 0

	def send(self,command):
		self.server.sendto(command.encode("utf-8"),self.addr)

	def update(self):
		while True:
			command = "rc "+str(self.x)+" "+str(self.y)
			command += " "+str(self.z)+" "+str(self.t)
			if keydown("f") and keydown("right"):
				self.send("flip r")
				print(self.recv())
			self.send(command)
			self.x,self.y,self.z,self.t = (0,0,0,0)
			sleep(0.1)

	def recv(self):
		data, addr = self.server.recvfrom(2**10)
		return data.decode()

	def recv_loop(self):
		while True:
			print(self.recv())

	def stream(self):
		print("sending streamon")
		self.send("streamon")
		while self.recv() != "ok":
			self.send("streamon")
		cap = cv2.VideoCapture('udp://192.168.10.1:11111')
		print("streaming ok")
		while True :
			ret, frame = cap.read()
			cv2.imshow("Operation Overthrow Feed", frame)
			if cv2.waitKey(1) == 27:
				break
		cap.release()
		cv2.destroyAllWindows()

	def follow_color(self,color,frame):
		"""
		Using a numpy frame and color choice the
		drone with auto adjust to follow a given
		color.
		"""
		return

	def video_data(self):
		self.send("streamon")
		while self.recv() != "ok":
			self.send("streamon")
		cap = cv2.VideoCapture('udp://192.168.10.1:11111')
		while True :
			ret, frame = cap.read()
			frame = np.array(frame)
			"""
			Put function here to control drone using camera data


			"""
		cap.release()


	def stay_alive(self):
		while True:
			self.send("command")
			self.send("battery?")
			system("clear")
			print("battery:",self.recv())
			sleep(10)
