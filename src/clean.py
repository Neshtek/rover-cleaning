from .util import keyboard_shutdown
from time import sleep
import math
from .Rover import Rover

length = 45
breadth = 30

#True = edge detected

def moveF(rover, spd):
    rover.moveForward(speed=spd)

def moveB(rover, spd):
    rover.moveBackward(speed=spd)

def moveF_L(rover, spd, d):
    rover.moveForward_L(speed=spd,d=d)

def moveB_L(rover, spd, d):
    rover.moveBackward_L(speed=spd,d=d)

def changeDirection(rover, angle):
    rover.changeYaw(angle=angle,speed=0.02)


def change_lane(rover:Rover):
    print("Changing Lane")
    sleep(1)
    # Calculated values for lane change diagonal distance
    hypotenuse_dist = math.sqrt(((length/2) ** 2) + (breadth ** 2))
    # Calculated angle for lane change
    theta = math.atan((length/2) / breadth)

    try:
        while True:
            rover.move_forward_dist(speed=2, dist=(length/2))
            print("moving forward2")
            sleep(1)
            rover.change_yaw(angle=-(theta))
            print("changing direction")
            sleep(1)
    
            # No Further Lanes
            if rover.front_edge.check_drive_ok() == False:
                print("No Further Lanes")
                rover.change_yaw(angle=theta)
                print("changing direction due to no lanes!")
                rover.move_backward_dist(speed=2, dist=(length/2))
                print("moving back4")
                print("odometry called")
            
            # Available Lanes
            else:
                rover.move_forward_dist(speed=2, dist=hypotenuse_dist)
                print("moving forward2")
                rover.change_yaw(angle=theta)
                rover.move_backward_dist(speed=2, dist=length)
                print("moving back3")
                return

    except KeyboardInterrupt:
        keyboard_shutdown()

def sweep(rover:Rover):
    print("Sweeping")
    sleep(1)
    try:
        while(rover.front_edge.check_drive_ok() == True):
            moveF(rover=rover,spd=2)
            print("moving forward1")
            sleep(1)

        while (rover.back_edge.check_drive_ok() == True):
            moveB(rover=rover,spd=2)
            print("moving back3")
            sleep(1)
            
        change_lane(rover=rover)
        sweep(rover=rover)

    except KeyboardInterrupt:
        keyboard_shutdown()  
  

def cleanArea(rover):
    
    print('check drone status')
    rover.workingStatus = True
    rover.setupAndArm()
    rover.changeVehicleMode('GUIDED')
    sleep(2)
    
    try:
        moveF_L(rover,spd=2, d=int((length)))
        print("Undocking")
        #wait(5)
        #wait till drone takeoff
        while(True):
            moveB(rover,spd=2)
            print("moving back1")
            sleep(1)

            if (rover.ul_back_edge.checkDriveOk() == True):
                changeDirection(rover, 90)
                print("Orienting to corner")
                sleep(1)

            moveB(rover,spd=2)
            print("moving back1")
            if (rover.ul_back_edge.checkDriveOk() == True):
                print("Corner Detected")
                print("Sweep function called")
                sweep(rover=rover)
                break
    
    except KeyboardInterrupt:
        keyboard_shutdown()