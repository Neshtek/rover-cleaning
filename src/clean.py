from .util import keyboard_shutdown
from time import sleep
import math
from .Rover import Rover

length = 0.45
breadth = 0.30

def change_lane(rover:Rover):
    print("Changing Lane")
    sleep(1)
    # Calculated values for lane change diagonal distance
    hypotenuse_dist = math.sqrt(((length/2) ** 2) + (breadth ** 2))
    # Calculated angle for lane change
    theta = math.atan(breadth / (length/2))

    try:
        while True:
            rover.move_forward_dist(speed=0.1, dist=(length/2))
            print("moving forward2")
            sleep(1)
            rover.change_yaw(angle=-(theta))
            print("changing direction")
            sleep(1)
    
            # No Further Lanes
            if rover.front_edge.check_drive_ok() == False:
                print("No Further Lanes")
                sleep(1)
                rover.change_yaw(angle=theta)
                print("changing direction due to no lanes!")
                sleep(1)
                rover.move_backward_dist(speed=0.1, dist=(length/2))
                print("moving back4")
                sleep(1)
                print("odometry called")
                keyboard_shutdown()
                
            # Available Lanes
            else:
                rover.move_forward_dist(speed=0.1, dist=hypotenuse_dist)
                print("moving forward2")
                sleep(1)
                rover.change_yaw(angle=theta)
                rover.move_backward_dist(speed=0.1, dist=length)
                print("moving back3")
                sleep(1)
                return

    except KeyboardInterrupt:
        keyboard_shutdown()

def sweep(rover:Rover):
    print("Sweeping")
    sleep(1)
    try:
        while True:
            rover.move_forward(speed=0.1)
            print("moving forward1")
            sleep(1)
            if rover.front_edge.check_drive_ok() == False:
                rover.move_forward(speed=0.1)                 # STOP
                break
            sleep(1)

        while True:
            rover.move_backward(speed=0.1)
            print("moving back3")
            sleep(1)
            if rover.back_edge.check_drive_ok() == False:
                rover.move_backward(speed=0.1)                # STOP
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
    sleep(1)
    
    try:
        print('Undocking')
        rover.move_backward_dist(speed=0.1, dist=((3*length)/2))
        print("undocked")
        sleep(1)
        #wait(5)
        #wait till drone takeoff
        while True:
            print('move Forward start')
            rover.move_forward(speed=0.1)
            print("moving forward1")
            sleep(1)

            if rover.front_edge.check_drive_ok() == False:
                rover.change_yaw(math.radians(-90))
                print("Orienting to corner")
                sleep(1)
                break

        while True:
            rover.move_backward(speed=0.1)
            print("moving back1")
            sleep(1)
            if rover.back_edge.check_drive_ok() == False:
                print("Corner Detected")
                sleep(1)
                rover.move_backward(speed=0.1)
                print("Sweep function called")
                sleep(1)
                sweep(rover=rover)
    
    except KeyboardInterrupt:
        keyboard_shutdown()

if __name__ == '__main__':
    pass