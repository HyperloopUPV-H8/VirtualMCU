from pin.pinout import Pinout
from services.InputCapture import InputCapture
from services.digital_in import DigitalInService
from services.digital_out import DigitalOutService
from shared_memory import SharedMemory
from src.pin import memory
from test_lib.input.aggregate import Multiple
from test_lib.input.input import Input, InputFailedException
from test_lib.input.timed import After
from enum import Enum


class Case(Enum):
    ShortCircuit = 0
    Normal = 10
    UnderVoltage = 20
    EquipmentFault = 40
    GroundFault = 50


class IMD:
    def __init__(
        self, shm: SharedMemory, ok_hs: Pinout, m_hs: Pinout, power_on: Pinout
    ):
        self.power_on = DigitalOutService(shm, power_on)
        self.ok_hs = DigitalInService(shm, ok_hs)
        self.m_hs = InputCapture(shm, m_hs)

    def _IMDInput(self, frequency, duty_cycle, good_state: bool) -> Input:
        if self.power_on.get_pin_state() == memory.DigitalOut.State.Low:
            raise InputFailedException
        elif good_state is True:
            return Multiple(
                self.ok_hs.generate_state(memory.DigitalIn.State.High),
                self.m_hs.generate_duty(duty_cycle),
                self.m_hs.generate_frequency(frequency),
            )
        else:
            return Multiple(
                self.ok_hs.generate_state(memory.DigitalIn.State.Low),
                self.m_hs.generate_duty(duty_cycle),
                self.m_hs.generate_frequency(frequency),
            )

    def generate_fast_start(self, duty_cycle) -> Input:
        if 5 <= duty_cycle <= 10:
            return self._IMDInput(30, duty_cycle, True)
        if 90 <= duty_cycle <= 95:
            return self._IMDInput(30, duty_cycle, False)
        else:
            raise ValueError(
                "Duty cycle for fast start can be only between 5%% and 10%%, or between 90%% and 95%%"
            )

    def generate_short_circuit(self) -> Input:
        return self._IMDInput(0, 0, 0)

    def generate_normal(self, duty_cycle) -> Input:
        if 5 <= duty_cycle <= 95:
            raise ValueError("Duty cycle for normal state must be between 5%% and 95%%")
        return self._IMDInput(10, duty_cycle, True)

    def generate_undervoltage(self, duty_cycle) -> Input:
        if not 5 <= duty_cycle <= 95:
            raise ValueError(
                "Duty cycle for undervoltage state must be between 5%% and 95%%"
            )
        return self._IMDInput(20, duty_cycle, False)

    def generate_equipment_fault(self, duty_cycle) -> Input:
        if not 47.5 <= duty_cycle <= 52.5:
            raise ValueError(
                "Duty cycle for equipment fault must be between 47.5%% and 52.5%%"
            )
        return self._IMDInput(40, duty_cycle, False)

    def generate_ground_fault(self, duty_cycle) -> Input:
        if not 47.5 <= duty_cycle <= 52.5:
            raise ValueError(
                "Duty cycle for ground fault must be between 47.5%% and 52.5%%"
            )
        return self._IMDInput(50, duty_cycle, False)

    def generate_power_up(self, case: Case, initial_duty_cycle, duty_cycle) -> Input:
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
        if case is Case.ShortCircuit:
            return Multiple(
                self.generate_fast_start(initial_duty_cycle),
                After(2, self.generate_short_circuit(duty_cycle)),
            )

        if case is Case.Normal:
            return Multiple(
                self.generate_fast_start(initial_duty_cycle),
                After(2, self.generate_normal(duty_cycle)),
            )

        if case is Case.UnderVoltage:
            return Multiple(
                self.generate_fast_start(initial_duty_cycle),
                After(2, self.generate_undervoltage(duty_cycle)),
            )

        if case is Case.EquipmentFault:
            return Multiple(
                self.generate_fast_start(initial_duty_cycle),
                After(2, self.generate_equipment_fault(duty_cycle)),
            )

        if case is Case.GroundFault:
            return Multiple(
                self.generate_fast_start(initial_duty_cycle),
                After(2, self.generate_ground_fault(duty_cycle)),
            )

    def resistance_to_duty_cycle(self, resistance) -> float:
        """
        Auxiliar method used to transform the resistance you deserve to the duty cycle that
        you need to pass to generate_normal() and generate_undervoltage() functions
        """
        DIVISOR_RESISTANCE = 1200000
        return ((0.9 * DIVISOR_RESISTANCE) / (resistance + DIVISOR_RESISTANCE)) + 0.05
