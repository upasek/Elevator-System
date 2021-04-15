import threading
import socket
from time import sleep

# array Data Structure
upList = []
upDes = []
downList = []
downDes = []
currentFloor = 1

# ========================================== server ================================================ #


class server:
    global upList
    global downList

    @staticmethod
    def serverSocket():
        serverSocket = socket.socket()

        serverSocket.bind(('localhost', 47796))

        serverSocket.listen(1)

        cli, add = serverSocket.accept()
        while True:
            data = cli.recv(1024).decode().split(',')
            if not data:
                break

            if int(data[0]) == 1:
                upList.append((int(data[1]), int(data[2])))
            elif int(data[0]) == -1:
                downList.append((int(data[1]), int(data[2])))

        cli.close()


# ======================================== Door function ======================================== #

def openDoor():
    print('Door opening')


def closeDoor():
    print('Door closing')
    idle()

# ========================================= idle state ========================================== #


def idle():
    global upList, downList, currentFloor, upDes, downDes
    sleep(3)
    if len(upList) <= 0 and len(downList) <= 0 and len(upDes) <= 0 and len(downDes) <= 0:
        print('Elevator is idle at floor ', currentFloor)


# =============================== Elevator up motion ========================================== #


class upMotion:

    @classmethod
    def move(cls):
        global currentFloor

        li1 = [dat[0] for dat in upList]

        if len(li1) > 0:

            if currentFloor > min(li1):
                down()

            print("\nElevator is moving in upward direction\n")

            for floor in range(currentFloor, 10, 1):
                m = [dat[0] for dat in upList]

                print('Elevator at floor', floor)

                if floor in m:
                    sleep(3), openDoor()
                    sleep(3), closeDoor()
                    for item in upList:
                        if item[0] == floor and item[1] not in upDes:
                            upDes.append(int(item[1]))

                    for j in upList:
                        if j == tuple((floor, upDes[-1])):
                            upList.remove(j)

                if floor in upDes:
                    currentFloor = floor
                    upDes.remove(floor)
                    sleep(3), openDoor()
                    sleep(3), closeDoor()
                    if len(upDes) <= 0:
                        break

                sleep(3)

# =============================== Elevator down motion ========================================== #


class downMotion:

    @classmethod
    def move(cls):
        global currentFloor

        li2 = [item[0] for item in downList]

        if len(li2) > 0:
            if currentFloor < max(li2):
                up()

            print("\nElevator is moving in downward direction\n")

            for i in range(currentFloor, 0, -1):
                m = [item[0] for item in downList]

                print('Elevator at floor', i)

                if i in m:
                    sleep(3), openDoor()
                    sleep(3), closeDoor()
                    for item in downList:
                        if item[0] == i and item[1] not in downDes:
                            downDes.append(int(item[1]))

                    for j in downList:
                        if j == tuple((i, downDes[-1])):
                            downList.remove(j)

                if i in downDes:
                    currentFloor = i
                    downDes.remove(i)
                    sleep(3), openDoor()
                    sleep(3), closeDoor()
                    if len(downDes) <= 0:
                        break

                sleep(3)

# ===============================  Elevator move upward ========================================== #


def up():
    global currentFloor
    floor = currentFloor
    m = [item[0] for item in downList]
    max_floor = max(m)

    print("\nElevator is moving in upward direction\n")

    while floor <= max_floor:
        print('Elevator at floor', floor)

        n = [dat[0] for dat in upList]
        m = [item[0] for item in downList]

        if floor in n:
            sleep(3), openDoor()
            sleep(3), closeDoor()
            for item in upList:
                if item[0] == floor and item[1] not in upDes:
                    upDes.append(int(item[1]))

            for j in upList:
                if j == tuple((floor, upDes[-1])):
                    upList.remove(j)

            if max(upDes) > max(m):
                max_floor = max(upDes)

        if floor in upDes:
            currentFloor = floor
            upDes.remove(floor)
            sleep(3), openDoor()
            sleep(3), closeDoor()

        currentFloor = floor
        floor += 1
        sleep(3)


# ===============================  Elevator move downward ========================================== #


def down():
    global currentFloor
    floor = currentFloor
    m = [item[0] for item in upList]
    min_floor = min(m)

    print("\nElevator is moving in downward direction\n")

    while currentFloor >= min_floor:

        print('Elevator at floor', floor)

        n = [item[0] for item in downList]
        m = [item[0] for item in upList]

        if floor in n:
            sleep(3), openDoor()
            sleep(3), closeDoor()
            for item in downList:
                if item[0] == floor and item[1] not in downDes:
                    downDes.append(int(item[1]))

            for j in downList:
                if j == tuple((floor, downDes[-1])):
                    downList.remove(j)

            if min(downDes) < min(m):
                min_floor = min(downDes)

        if floor in downDes:
            currentFloor = floor
            downDes.remove(floor)
            sleep(3), openDoor()
            sleep(3), closeDoor()

        currentFloor = floor
        floor -= 1
        sleep(3)


# =============================== main Elevator ========================================== #


class Elevator:

    def __init__(self):
        print('Elevator in idle at floor 1')
        while True:
            upMotion.move()
            downMotion.move()


# =============================== main function ========================================== #


if __name__ == '__main__':
    ob1 = server()

    t1 = threading.Thread(target=ob1.serverSocket, args=())
    t2 = threading.Thread(target=Elevator, args=())

    t1.start()
    t2.start()
