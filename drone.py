from keyboard import is_pressed as keydown
from socket import socket,AF_INET,SOCK_DGRAM
from threading import Thread
from time import sleep
import cv2
from os import system
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from sklearn.cluster import MiniBatchKMeans

class Drone:
	def __init__(self):
		ip = "192.168.10.1"
		self.addr = (ip,8889)
		self.video_addr = ("192.168.10.2",11111)
		self.server = socket(AF_INET,SOCK_DGRAM)
		self.server.bind(("192.168.10.2",8889))
		self.x,self.y,self.z,self.t = (0,0,0,0)
		self.frame = 0
		print("Waiting for ok response")
		self.send("command")
		self.frame = 0
		self.cap = 0
		while self.recv() != "ok":
			self.send("command")
		print("Drone Initiated")

	def control(self):
		self._stay_alive()
		self._update()
		while not(keydown("q")):
			self._move()
		self.kill()

	def kill(self):
		self.send("emergency")

	def _move(self):
		if keydown("space"):
			self.send("takeoff")
			sleep(1)
		if keydown("l"):
			self.send("land")
		if keydown("right") and self.x < 97:
			self.x += 3
		if keydown("left") and self.x > -97:
			self.x -= 3
		if keydown("up") and self.y < 97:
			self.y += 3
		if keydown("down") and self.y > -97:
			self.y -= 3
		if keydown("w") and self.z < 97:
			self.z += 3
		if keydown("s") and self.z > -97:
			self.z -= 3
		if keydown("d") and self.t < 97:
			self.t += 3
		if keydown("a") and self.t > -97:
			self.t -= 3

	def takeoff(self):
		self.send("takeoff")

	def land(self):
		self.send("land")

	def send(self,command):
		self.server.sendto(command.encode("utf-8"),self.addr)

	def _update(self):
		def f():
			while True:
				command = "rc "+str(self.x)+" "+str(self.y)
				command += " "+str(self.z)+" "+str(self.t)
				if keydown('z') or keydown('x') or keydown('c') or keydown('v'):
					if keydown("z"):
						self.send("flip l")
					if keydown("x"):
						self.send("flip f")
					if keydown("c"):
						self.send("flip r")
					if keydown("v"):
						self.send("flip b")
					sleep(0.1)
				elif keydown("space"):
					self.send("takeoff")
				elif keydown("l"):
					self.send("land")
				else:
					self.send(command)
				self.x,self.y,self.z,self.t = (0,0,0,0)
				sleep(0.1)
		Thread(target=f,daemon=True).start()

	def recv(self):
		data, addr = self.server.recvfrom(2**10)
		return data.decode()

	def recv_loop(self):
		while True:
			print(self.recv())

	def stream(self):
		def f():
			while True :
				cv2.imshow("Drone Feed", self.frame)
				if cv2.waitKey(1) == 27:
					break
			cap.release()
			cv2.destroyAllWindows()
		Thread(target=f,daemon=True).start()

	def _get_major_color(self):
		frame = self.frame
		kmeans = MiniBatchKMeans(1)
		frame = frame.reshape(720*960,3)
		kmeans.fit(frame)
		return kmeans.cluster_centers_[kmeans.predict(frame)][0]

	def _get_com(self,color):
		"""
		gets center of mass of color in an rbg array
		"""
		data = np.array(self.frame)
		t = 20 # range of color threshold
		bin_map = cv2.inRange(data,color-t,color+t)
		y,x = ndimage.measurements.center_of_mass(bin_map)
		w,h = bin_map.shape
		num = (np.sum(bin_map)/(w*h))*100
		print(num)
		x -= 360
		if x == x:
			if x > 10:
				self.t += 5
			elif x < -10:
				self.t -= 5
		# y 480

	def connect_video(self):
		self.send("streamon")
		while self.recv() != "ok":
			self.send("streamon")
		print("streamon")
		self.cap = cv2.VideoCapture('udp://192.168.10.1:11111')
		def f():
			while True:
				ret, self.frame = self.cap.read()
		Thread(target=f,daemon=True).start()

	def follow_color(self):
		self._update()
		sleep(5)
		color = np.array(self._get_major_color())
		print("Color Succesfully Calibrated. Press enter to takeoff.")
		input()
		self.takeoff()
		# initialize variables
		xm,ym = (0,0)
		# main loop to move drone based on x and y
		while not(keydown("q")):
			if keydown("l"):
				self.land()
			if keydown("space"):
				self.takeoff()
			self._get_com(color)
		self.kill()
		cap.release()
		cv2.destroyAllWindows()

	def _stay_alive(self):
		def f():
			while True:
				self.send("command")
				self.send("battery?")
				system("clear")
				print("battery:",self.recv())
				sleep(10)
		Thread(target=f,daemon=True).start()
