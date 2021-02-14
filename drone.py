from keyboard import is_pressed as keydown
from socket import socket,AF_INET,SOCK_DGRAM
from threading import Thread
from time import sleep
import cv2

class Drone:
	def __init__(self):
		ip = "192.168.10.1"
		self.addr = (ip,8889)
		self.video_addr = ("192.168.10.2",11111)
		self.server = socket(AF_INET,SOCK_DGRAM)
		self.server.bind(("192.168.10.2",8889))
		self.x,self.y,self.z,self.t = (0,0,0,0)
		self.in_air = 0
		print("Waiting for ok response")
		self.send("command")
		while self.recv() != "ok":
			self.send("command")
		print("Drone Initiated")

		#Thread(target=self.stream,daemon=True).start()
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
		print(command)
		self.server.sendto(command.encode("utf-8"),self.addr)

	def update(self):
		while True:
			command = "rc "+str(self.x)+" "+str(self.y)
			command += " "+str(self.z)+" "+str(self.t)
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
			#img = cv2.resize(frame, (720, 960))
			cv2.imshow("Operation Overthrow Feed", frame)
			if cv2.waitKey(1) == 27:
				break
		cap.release()
		cv2.destroyAllWindows()

	def stay_alive(self):
		while True:
			self.send("command")
			sleep(1)
