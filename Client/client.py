import socket

# =============================== client ========================================== #

clientSer = socket.socket()

clientSer.connect(('localhost', 47796))

while True:
    direction = input('up => 1 or down => -1 : ')
    floor = input('Enter floor num : ')
    destination = input('Enter destination : ')

    clientSer.sendall(str.encode(','.join([str(direction), str(floor), str(destination)])))
