from machine import Pin, time_pulse_us
import time

class Ultrasonic():
    SOUND_SPEED = 340.0 # m/s

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
        pulse_width_s = time_pulse_us(self._echo, Pin.on) / 10000
        distance = (pulse_width_s / 2.0) * self.SOUND_SPEED
        return distance