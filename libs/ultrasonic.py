from machine import Pin, time_pulse_us
import time

class Ultrasonic():
    SOUND_SPEED = 340.0 # m/s
    MAX_DISTANCE = 300 # cm
    TIMEOUT = int((2*MAX_DISTANCE)/SOUND_SPEED/100* 1000000) # 17647 us
    
    def __init__(self, trig_Pin, echo_Pin):
        """Initialize Input(echo) and Output(trig) Pins."""
        self._trig = Pin(trig_Pin, Pin.OUT)
        self._echo = Pin(echo_Pin, Pin.IN)

    def _pulse(self):
        """Trigger ultrasonic module with 10us pulse."""
        self._trig.high()
        time.sleep_us(10)
        self._trig.low()

    def get_distance(self):
        """Measure pulse length and return calculated distance [cm]."""
        self._pulse()
        pulse_width = time_pulse_us(self._echo, Pin.on, self.TIMEOUT) / 1000000.0
        #pulse_width = time_pulse_us(self._echo, Pin.on) / 1000000.0
        distance = pulse_width * self.SOUND_SPEED / 2 * 100
        return distance
    
if __name__ == '__main__':
    # init
    sonar = Ultrasonic(6, 7)

    # get distance
    while True:
        distance = sonar.get_distance()
        print(distance)
        time.sleep(0.2)
    
