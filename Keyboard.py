import keyboard

while True:
	if keyboard.is_pressed("left"):
		print("left")
	if keyboard.is_pressed("right"):
		print("right")
	print("")
