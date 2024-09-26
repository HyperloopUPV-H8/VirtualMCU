from gpio import GPIO
from gpio.pinout import Pinout

def main() -> int:
    lcu_gpio = GPIO("lcu")

    print(f"One GPIO memory zone takes {lcu_gpio.mem_size() / 1024} KB")
    
    lcu_gpio.write_pin(Pinout.PB0, bytearray([0xFF, 0xFF, 0xFF, 0xFF]))
    print(lcu_gpio.read_pin(Pinout.PB0))

    # GPIO shared memory gets cleaned up by the garbage collector!
    return 0

if __name__ == "__main__":
    exit(main())