from gpio import GPIOMap
from gpio.mode import PinMode, PinState
from gpio.pinout import Pinout

def main() -> int:
    lcu_gpio_map = GPIOMap("lcu")

    print(f"One LCU memory zone takes {lcu_gpio_map.mem_size() / 1024} KB")

    pwm_pin = None
    digital_input_pin = None
    digital_output_pin = None
    
    try:
        pwm_pin = lcu_gpio_map.pin(Pinout.PB0, mode=PinMode.PWM_OUT)
        pwm_pin.reset()
        digital_input_pin = lcu_gpio_map.pin(Pinout.PB1, mode=PinMode.INPUT)
        digital_input_pin.reset()
        digital_output_pin = lcu_gpio_map.pin(Pinout.PB2, mode=PinMode.OUTPUT)
        digital_output_pin.reset()

        pwm_pin.set(41.0, 1000.0)
        
        print("duty: ", pwm_pin.duty_cycle)
        print("freq: ", pwm_pin.frequency_khz)

        digital_input_pin.set()

        print("digital_input: ", digital_input_pin.state)

        for _ in range(8):
            digital_output_pin.toggle()
        
        print("digital_output: ", digital_output_pin.state)
    finally:
        if pwm_pin is not None:
            pwm_pin.close()
        if digital_input_pin is not None:
            digital_input_pin.close()
        if digital_output_pin is not None:
            digital_output_pin.close()
        lcu_gpio_map.close()

    return 0

if __name__ == "__main__":
    exit(main())