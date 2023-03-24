from .util import keyboard_shutdown
from time import sleep
import math
from .Rover import Rover

length = 45
breadth = 30

def change_lane(rover:Rover):
    print("Changing Lane")
    sleep(1)
    # Calculated values for lane change diagonal distance
    hypotenuse_dist = math.sqrt(((length/2) ** 2) + (breadth ** 2))
    # Calculated angle for lane change
    theta = math.atan(breadth / (length/2))

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
        while True:
            rover.move_forward(speed=2)
            print("moving forward1")
            if rover.front_edge.check_drive_ok() == False:
                rover.move_forward(speed=0)                 # STOP
                break
            sleep(1)

        while True:
            rover.move_backward(speed=2)
            print("moving back3")
            if rover.back_edge.check_drive_ok() == False:
                rover.move_backward(speed=0)                # STOP
                break
            sleep(1)
            
        change_lane(rover=rover)
        sweep(rover=rover)

    except KeyboardInterrupt:
        keyboard_shutdown()  
  

def start_clean(rover:Rover):
    print('check drone status')
    rover.working_status = True
    rover.setup_arm()
    rover.change_vehicle_mode('GUIDED')
    sleep(2)
    
    try:
        rover.move_backward_dist(speed=2, dist=((3*length)/2))
        print("Undocking")
        #wait(5)
        #wait till drone takeoff
        while True:
            rover.move_forward(speed=2)
            print("moving forward1")
            sleep(1)

            if rover.front_edge.check_drive_ok() == False:
                rover.change_yaw(math.radians(-90))
                print("Orienting to corner")
                sleep(1)

            rover.move_backward(speed=2)
            print("moving back1")
            if rover.back_edge.check_drive_ok() == False:
                print("Corner Detected")
                rover.move_backward(speed=0)
                print("Sweep function called")
                sweep(rover=rover)
                break
    
    except KeyboardInterrupt:
        keyboard_shutdown()

if __name__ == '__main__':
    pass