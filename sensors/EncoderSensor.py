from src.services.Encoder import Encoder
from src.pin.pinout import Pinout
from src.pin import memory
from src.shared_memory import SharedMemory
from test_lib.input.aggregate import Multiple
from test_lib.input.input import Input, InputFailedException
from test_lib.condition.condition import Condition
from test_lib.condition.checked import Checked

COUNTER_DISTANCE_IN_METERS = 0.0001
N_FRAMES = 100
FRAME_SIZE_IN_SECONDS = 0.005
START_COUNTER = 2**31 - 1

class EncoderSensor():
    def __init__(self,shm:SharedMemory,pin1:Pinout,pin2:Pinout):
        self._encoder=Encoder(shm,pin1,pin2)
        self.position=0
        self.direction=memory.Encoder.Direction.Forwards
        self.speed=0.0
        self.acceleration=0.0
        self.counter=0

    class EncoderSensorException(InputFailedException):
        def __str__(self):
            return "The encoder is not on"
    
    def _check_pin_state(self) -> bool:
        if not self._encoder.get_is_on():
            raise self.EncoderSensorException()
        else:
            return True

    def generate_speed(self,direction:memory.Encoder.Direction.value,speed:float,acceleration:float)->Input:
        delta_counter = int(speed * N_FRAMES * FRAME_SIZE_IN_SECONDS / COUNTER_DISTANCE_IN_METERS)
        self.direction = direction
        if direction == memory.Encoder.Direction.Backwards:
            self.counter -= delta_counter
        else:
            self.counter += delta_counter
            
        self.position = (self.counter - START_COUNTER) * COUNTER_DISTANCE_IN_METERS
        self.speed = speed
        self.acceleration = acceleration
        return Checked(self._check_pin_state,
            Multiple(self._encoder.generate_direction(direction),
            self._encoder.generate_counter(self.counter)))
        
    def generate_counter(self,direction:memory.Encoder.Direction.value,counter:int)->Input:
        self.direction = direction
        self.counter = counter
        return Checked (self._check_pin_state, Multiple(self._encoder.generate_direction(direction),self._encoder.generate_counter(counter)))