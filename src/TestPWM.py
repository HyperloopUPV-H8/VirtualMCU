from shared_memory import SharedMemory
from src.pin import DigitalIn,Pinout,PinType,Pin
from src.services.digital_in import DigitalInService
from src.services.PWM import PWM
from src.services.ADC import ADC
import time
shm = SharedMemory("sim_tests")

pin=PWM(shm,Pinout.PB0)

pin.set_frequency(10000)
pin.set_duty_cycle(0.5)

