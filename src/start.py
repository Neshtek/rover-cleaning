from .Rover import Rover
from .clean import start_clean

def main_start(serial=None, connection=None):
    if serial != None:
        print(serial)
        rover = Rover(rover_serial=serial, connection=connection)
        start_clean(rover=rover)

if __name__ == '__main__':
    pass
else:
    main_start()