from uarm.wrapper import SwiftAPI
from time import sleep

count = 0

class Arm:
    def __init__(self):
        self.arm = SwiftAPI()
        self.arm.reset()
        sleep(2)

    def rest(self):
        self.arm.set_position(x=0, y=180, z=146, wait=True, timeout=10, speed=10000)
        print("moving to rest pos!")

    def correction(self):
        print("=================check start!=================\n")
        self.arm.set_position(x=227, y=0, z=60, wait=True, speed=10000)
        sleep(1)
        self.arm.set_position(x=227, y=0, z=47, wait=True, timeout=10, speed=10000)
        print("check center\n")
        sleep(1)
        input()
        self.arm.set_position(x=292, y=75, z=60, wait=True, speed=10000)
        sleep(1)
        self.arm.set_position(x=292, y=75, z=47, wait=True, timeout=10, speed=10000)
        print("check left-up\n")
        sleep(1)
        input()
        self.arm.set_position(x=293, y=-75, z=60, wait=True, speed=10000)
        sleep(1)
        self.arm.set_position(x=293, y=-75, z=47, wait=True, timeout=10, speed=10000)
        print("check right-up\n")
        sleep(1)
        input()
        self.arm.set_position(x=160, y=75, z=60, wait=True, speed=10000)
        sleep(1)
        self.arm.set_position(x=160, y=75, z=47, wait=True, timeout=10, speed=10000)
        print("check left-down\n")
        sleep(1)
        input()
        self.arm.set_position(x=160, y=-75, z=60, wait=True, speed=10000)
        sleep(1)
        self.arm.set_position(x=160, y=-75, z=47, wait=True, timeout=10, speed=10000)
        print("check right-down\n")
        sleep(1)
        input()
        self.arm.set_position(x=0, y=180, z=146, wait=True, timeout=10, speed=10000)

        print("=================check finish!=================\n")


    def move(self, color, coords):
        global count
        count += 1

        if coords == "pass" or coords == "resign":
            return None
        y, x = coords
        y = int(ord(y) - ord('A'))
        x = int(x) - 1

        if count == 1:
            x_take = 309
        elif count == 2:
            x_take = 280
        elif count == 3:
            x_take = 254
        elif count == 4:
            x_take = 223
        elif count == 5:
            x_take = 200
        elif count == 6:
            x_take = 170
        elif count == 7:
            x_take = 144
            count = 0

        if color == "B":
            xp = x_take
            yp = -145
            zp = 100
        elif color == "W":
            xp = x_take
            yp = 157
            zp = 100
        else:
            print("Wrong color input!")

        self.arm.set_position(x=xp, y=yp, z=zp, wait=True, speed=10000)
        self.arm.flush_cmd(wait_stop=True)
        self.arm.set_position(z=54, wait=True, speed=10000)
        sleep(1.5)
        self.arm.set_pump(True)
        sleep(2)
        self.arm.set_position(z=100, wait=True, speed=10000)
        self.arm.set_position(x=294-x*22, y=-66+y*24, z=100, wait=True, speed=10000)
        self.arm.flush_cmd(wait_stop=True)
        print("moving to:", coords)
        self.arm.set_position(z=54, wait=True, speed=10000) # original z is -26
        sleep(1)
        self.arm.set_pump(False)
        sleep(0.5)
        self.arm.set_position(z=100, wait=True, speed=10000)
        sleep(0.5)
        self.arm.flush_cmd()

    def remove(self, coords, remove_list):
        self.arm.set_position(x=1, y=2, z=45, wait=True, speed=10000)
        x, y = coords
        remove_list

    def remove_chess(self, color, coords):
        y, x = coords
        y = int(y) - 1
        x = int(x) - 1

        self.arm.set_position(x=294-x*22, y=-66+y*24, z=100, wait=True, speed=10000)
        self.arm.flush_cmd(wait_stop=True)
        self.arm.set_position(z=54, wait=True, speed=10000)
        sleep(1.5)
        self.arm.set_pump(True)
        sleep(2)
        print("removing :", coords)
        self.arm.set_position(z=100, wait=True, speed=10000)
        self.arm.set_position(x=342, y=0, z=90, wait=True, speed=10000)
        self.arm.flush_cmd(wait_stop=True)
        self.arm.set_pump(False)
        sleep(0.5)

    def take_photo(self):
        self.arm.set_position(x=166, y=4, z=220, wait=True, timeout=10,speed=10000)
        print("Take Picture place!")

    def game_over(self):
        self.arm.set_position(x=0, y=170, z=100, wait=True, timeout=10, speed=10000)
        print("Game over!")
