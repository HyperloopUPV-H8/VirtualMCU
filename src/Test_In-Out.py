from shared_memory import SharedMemory
from pin import DigitalIn,Pinout,PinType,Pin

shm = SharedMemory("sim_tests")


button=shm.get_pin(Pinout.PA0, PinType.DigitalIn)

button.data.state=DigitalIn.State.High
