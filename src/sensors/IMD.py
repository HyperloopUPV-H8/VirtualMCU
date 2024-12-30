from pin.pinout import Pinout
from services.InputCapture import InputCapture
from services.digital_in import DigitalInService
from services.digital_out import DigitalOutService
from shared_memory import SharedMemory
from src.pin import memory
from test_lib.input.aggregate import Multiple
from test_lib.input.checked import Checked
from test_lib.input.input import Input, InputFailedException
from test_lib.condition.condition import Condition
from test_lib.input.timed import After
from enum import Enum

"""
    Factory resistance used to determine the state of the SST (Speed Start Measuring)
"""
RAN = 100000  # 100 KOhmios


class Case(Enum):
    ShortCircuit = 0
    Normal = 10
    UnderVoltage = 20
    EquipmentFault = 40
    GroundFault = 50


class IMDException(InputFailedException):
    def __str__(self):
        return "IMD is turned off"


class IMD:
    def __init__(
        self, shm: SharedMemory, ok_hs: Pinout, m_hs: Pinout, power_on: Pinout
    ):
        self.power_on = DigitalOutService(shm, power_on)
        self.ok_hs = DigitalInService(shm, ok_hs)
        self.m_hs = InputCapture(shm, m_hs)

    def _check_pin_state(self) -> bool:
        if self.power_on.get_pin_state() == memory.DigitalOut.State.Low:
            raise IMDException
        else:
            return True

    def _IMDInput(self, frequency, duty_cycle, good_state: bool) -> Input:
        return Checked(
            self._check_pin_state,
            Multiple(
                self.ok_hs.generate_state(
                    memory.DigitalIn.State.High
                    if good_state
                    else memory.DigitalIn.State.Low
                ),
                self.m_hs.generate_duty(duty_cycle),
                self.m_hs.generate_frequency(frequency),
            ),
        )

    def check_is_on(self) -> Condition:
        return self.power_on.wait_for_high()

    def _resistance_to_duty_cycle(self, resistance) -> float:
        """
        Auxiliar method used to transform the resistance you deserve to the duty cycle that
        you need to pass to generate_normal() and generate_undervoltage() functions
        """
        DIVISOR_RESISTANCE = 1200000
        return ((0.9 * DIVISOR_RESISTANCE) / (resistance + DIVISOR_RESISTANCE)) + 0.05

    def generate_fast_start(self, good_state: bool) -> Input:
        if good_state:
            return self._IMDInput(30, 7.5, True)
        else:
            return self._IMDInput(30, 92.5, False)

    def generate_short_circuit(self) -> Input:
        return self._IMDInput(0, 0, 0)

    def generate_normal(self, resistance) -> Input:
        duty_cycle = self._resistance_to_duty_cycle(resistance)
        if not 5 <= duty_cycle <= 95:
            raise ValueError("Duty cycle must be between 5%% and 95%%")
        return self._IMDInput(10, duty_cycle, True)

    def generate_undervoltage(self, resistance) -> Input:
        duty_cycle = self._resistance_to_duty_cycle(resistance)
        if not 5 <= duty_cycle <= 95:
            raise ValueError("Duty cycle must be between 5%% and 95%%")
        return self._IMDInput(20, duty_cycle, False)

    def generate_equipment_fault(self) -> Input:
        return self._IMDInput(40, 50, False)

    def generate_ground_fault(self) -> Input:
        return self._IMDInput(50, 50, False)

    def generate_power_up(self, case: Case, resistance) -> Input:
        """
        Args:
            case: this must be one of five possible cases defined as an enum in Case class

            resistance: used to determine the PWM duty cycle.
            It only has sense if case is Normal or UnderVoltage
        """

        if case is Case.ShortCircuit:
            return Multiple(
                self.generate_fast_start(True if resistance > 2 * RAN else False),
                After(2, self.generate_short_circuit()),
            )

        if case is Case.Normal:
            return Multiple(
                self.generate_fast_start(True if resistance > 2 * RAN else False),
                After(2, self.generate_normal(resistance)),
            )

        if case is Case.UnderVoltage:
            return Multiple(
                self.generate_fast_start(True if resistance > 2 * RAN else False),
                After(2, self.generate_undervoltage(resistance)),
            )

        if case is Case.EquipmentFault:
            return Multiple(
                self.generate_fast_start(True if resistance > 2 * RAN else False),
                After(2, self.generate_equipment_fault()),
            )

        if case is Case.GroundFault:
            return Multiple(
                self.generate_fast_start(True if resistance > 2 * RAN else False),
                After(2, self.generate_ground_fault()),
            )
