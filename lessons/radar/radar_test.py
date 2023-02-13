from radar import *
import time

def main():
    set_radar_scan_angle(120)
    while True:
        angle, distance, status = radar_scan()
        print(f'angle:{angle}, distance:{distance}, status:{status}')
        time.sleep(0.02)
        
if __name__ == '__main__':
    main()
    