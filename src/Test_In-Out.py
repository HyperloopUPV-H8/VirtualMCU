from src.shared_memory import SharedMemory
from src.pin import DigitalIn,Pinout,PinType,Pin
from src.services.digital_in import DigitalInService
import time

shm = SharedMemory("sim_tests")



button=DigitalInService(shm,Pinout.PA0)

for i in range(100):
    button.toggle()
    time.sleep(0.5)

