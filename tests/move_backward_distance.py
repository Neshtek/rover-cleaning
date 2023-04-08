from pymavlink import mavutil
import RPi.GPIO as GPIO
import time
import math


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Rover:
    def __init__(self, rover_serial, connection):
        vehicle = mavutil.mavlink_connection(connection)
        vehicle.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (vehicle.target_system, vehicle.target_component))

        _ = vehicle.messages.keys() #All parameters that can be fetched

        self.serial = rover_serial
        self.vehicle = vehicle
        self.working_status = False
        self.front_edge = Ultrasonic(21,20)
        self.back_edge = Ultrasonic(7,8)
        self.drone_serial = "ERROR000000000"
        self.drone_status = "Free"
        self.rover_status = "Free"
        self.update_rover()

class Ultrasonic:
    def __init__(self, TRIGGER, ECHO):
        print('Created')
        self.TRIGGER = TRIGGER
        self.ECHO = ECHO
        self.drive_ok = False
        self.area_completed = False
        GPIO.setup(self.TRIGGER, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER, False)
    
        start_time = time.time()
        stop_time = time.time()
    
        # save start_time
        while GPIO.input(self.ECHO) == 0:
            start_time = time.time()
    
        # save time of arrival
        while GPIO.input(self.ECHO) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2
    
        if distance > 30:
            return 30
        else:
            return distance
    
    def check_drive_ok(self):
        edge_dist = self.get_distance()    
        if edge_dist <= 10:
            #print ("Measured Distance = %.1f cm" % edge_dist)
            return True
        else:
            #print ("Measured Distance = %.1f cm" % edge_dist)
            return False
            time.sleep(1) #time too much
            d_edge = self.get_distance()
            if d_edge > 10:
                return False
                print ("Measured Distance 2 = %.1f cm" % d_edge)
            else:
                pass
        print ("Measured Distance = %.1f cm" % edge_dist)
        time.sleep(0.1)

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('127.0.0.1:14550')

# Wait for the first heartbeat
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (the_connection.target_system, the_connection.target_component))

mode = 'GUIDED'
mode_H = 'HOLD'
mode_id_H = the_connection.mode_mapping()[mode_H]

speed = 0
dist = 0.5
# Get mode ID
mode_id = the_connection.mode_mapping()[mode]
# Set new mode
print(the_connection)
the_connection.mav.set_mode_send(
    the_connection.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)

the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

the_connection.mav.command_long_encode(
		0, 0,
		mavutil.mavlink.MAV_CMD_DO_SET_REVERSE,
		0,
		1,
		0,
		0,
		0,
		0,0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

system = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)

initial = system.x
current = initial
the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                the_connection.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, int(0b110111000110), dist, 0, 0, speed, 0, 0, 0, 0, 0, 0, 0))

while True:
    change = abs(current - initial)
    if change >= dist:
        break
    the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                the_connection.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, int(0b110111000110), dist, 0, 0, speed, 0, 0, 0, 0, 0, 0, 0))

    
    if rover.back_edge.check_drive_ok() == False:
        the_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, the_connection.target_system,
                the_connection.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, int(0b110111000110), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        
        #the_connection.mav.set_mode_send(
        #    the_connection.target_system,
        #    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        #    mode_id_H)
        
        break
        
    system = the_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
    current = system.x

