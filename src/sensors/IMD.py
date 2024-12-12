from pin.pinout import Pinout
from services.PWM import PWM
from services.digital_in import DigitalInService
from shared_memory import SharedMemory
from test_lib.input.aggregate import Multiple
from test_lib.input.input import Input
from test_lib.input.timed import After
from enum import Enum

class Case(Enum):
    ShortCircuit    = 0
    Normal          = 10
    UnderVoltage    = 20
    EquipmentFault  = 40
    GroundFault     = 50

class IMDInput(Input):
    def __init__(self, frequency : int, duty_cycle : int):
        self.frequency = frequency
        self.duty_cycle = duty_cycle

    async def apply(self):
        self.m_hs.set_frequency(self.frequency)
        self.m_hs.set_duty_cycle(self.duty_cycle)

class IMD:
    def __init__(self, shm:SharedMemory, ok_hs:Pinout, m_hs:Pinout):
        self.ok_hs = DigitalInService(shm, ok_hs)
        self.m_hs = PWM(shm, m_hs)

    def generate_case(self, case : Case, initial_duty_cycle, duty_cycle) -> Input: 
        """
        Args:
            case: this must be one of five possible cases defined as an enum in Case class

            initial_duty_cycle: duty cycle during the 2 initial seconds
            It must be inside one of this two ranges:
            - 5% - 10%. It indicates that the fast init is going well
            - 90% - 95%. It indicates that the fast init is going bad
            If the value is outside this two ranges, this function will raise a value exception.
            
            duty_cycle: depend on the case, it should have inside one range or another:
            - Cases Normal and UnderVoltage: between 5% and 95%. This duty cycle
            indicates the resistance. You can use the resistance to compute this
            duty cycle using resistance_to_duty_cycle function
            - Fault cases (Equipment or Ground): beetween 47.5% and 52.5%
            If the value is outside any of this ranges, this function will raise a value exception.
        """ 
        if (5 <= initial_duty_cycle <= 10 or 90 <= initial_duty_cycle <= 95):
            raise ValueError("Initial duty cycle can be only between 5%% and 10%, or between 90%% and 95%")
        
        if (0 <= duty_cycle <= 100):
            raise ValueError("Duty cycle must be between 0%% and 100%%")
        
        if not isinstance(case, Case):
            raise TypeError("case must be an instance of the class Case")
        
        if case in (Case.Normal, Case.UnderVoltage):
            if (5 <= duty_cycle <= 95):
                raise ValueError("Duty cycle must be between 5%% and 95%%")
            
        if case in (Case.EquipmentFault, Case.GroundFault):
            if (47.5 <= duty_cycle <= 52.5):
                raise ValueError("Duty cycle must be between 47.5%% and 52.5%%")
        
        return Multiple(IMDInput(30, initial_duty_cycle), After(2, IMDInput(case, duty_cycle)))
    
    
    def resistance_to_duty_cycle(self, resistance) -> float:
        """
        Auxiliar method used to transform the resistance you deserve to 
        the duty cycle that you need to pass to generate_case() function
        """ 
        return ((0.9*1200000)/(resistance + 1200000)) + 0.05