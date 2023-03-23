from .Rover import Rover
from .clean import clean_area

def main_start(serial=None, connection=None):
    if serial != None:
        print(serial)
        rover = Rover(rover_serial=serial, connection=connection)
        clean_area(rover=rover)

if __name__ == '__main__':
    pass
else:
    main_start()