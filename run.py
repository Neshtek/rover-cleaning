import argparse
import src.settings as settings
import src.start as start

def main():
    serial = settings.get_serial()
    parser = argparse.ArgumentParser()
    parser.add_argument('--connect', default='127.0.0.1:14550')
    args = parser.parse_args()

    print ('Connecting to vehicle on: %s' % args.connect)
    start.main_start(serial=serial, connection=args.connect)

if __name__ == '__main__':
    main()