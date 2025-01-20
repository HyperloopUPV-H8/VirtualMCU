import socket, queue
from threading import Thread
from abc import ABC, abstractmethod
from vmcu.pin.pinout import Pinout
from vmcu.pin import PinType
from vmcu.shared_memory import SharedMemory
from dataclasses import dataclass


class SPIPeripheral(ABC):
    @abstractmethod
    def _send(self):
        pass

    @abstractmethod
    def _recv(self):
        pass

    def __init__(self, ip: str, port: str, shm: SharedMemory):
        self._shm = shm
        self._stop = False
        self._socket = socket.socket(type=socket.SOCK_DGRAM)
        self._socket.bind((ip, port))

        self._transmission_queue = queue.Queue()
        self._reception_queue = queue.Queue()
        self._transmission_thread = Thread(target=self._send)
        self._reception_thread = Thread(target=self._recv)

        self._transmission_thread.start()
        self._reception_thread.start()

        self._send_address = None

    def receive(self) -> bytes:
        return self._reception_queue.get()

    @abstractmethod
    def transmit(self):
        pass

    def __del__(self):
        self._stop = True
        self._transmission_thread.join()
        self._reception_thread.join()
        self._socket.close()


class SPIMaster(SPIPeripheral):
    @dataclass
    class MCUSlave:
        ip: str
        port: int
        chip_select: Pinout

    def _send(self):
        while not self._stop:
            msg = self._transmission_queue.get()
            total_sent = 0
            sent = 0
            while total_sent < len(msg):
                sent = self._socket.sendto(msg[sent:], self._send_address)
                if sent == 0:
                    raise RuntimeError("Socket connection broken")
                total_sent += sent

    def _recv(self):
        while not self._stop:
            received = self._socket.recv(1024)
            self._reception_queue.put(received)

    def __init__(self, ip: str, port: int, shm: SharedMemory):
        super().__init__(ip, port, shm)

    def transmit(self, msg, slave: MCUSlave):
        self._send_address = (slave.ip, slave.port)
        if self._chip_select != None and self._chip_select != slave.chip_select:
            pin = self._shm.get_pin(self._chip_select)
            pin.data.is_on = False
        self._chip_select = slave.chip_select
        pin = self._shm.get_pin(self._chip_select)
        pin.data.is_on = True
        self._transmission_queue.put(msg)


class SPISlave(SPIPeripheral):
    def _send(self):
        while not self._stop:
            msg = self._transmission_queue.get()
            total_sent = 0
            sent = 0
            while total_sent < len(msg):
                sent = self._socket.sendto(msg[sent:], self._send_address)
                if sent == 0:
                    raise RuntimeError("Socket connection broken")
                total_sent += sent

    def _recv(self):
        while not self._stop:
            self._reception_queue.put(self._socket.recv(1024))

    def __init__(
        self, ip, port, ip_master, port_master, shm: SharedMemory, CS: Pinout = None
    ):
        super().__init__(ip, port, shm)
        self._send_address = (
            ip_master,
            port_master,
        )
        self._chip_select = CS  # MCU Chip Select Pin "connected" to this peripheral. It has sense only if the master is a MCU

    def _is_selected(self) -> bool:
        """
        Returns:
            bool: if this peripheral is selected, meaning that it has his CS Pin activated in Shared Memory
        """
        pin = self._shm.get_pin(pin=self._chip_select, pin_type=PinType.SPI)
        return pin.data.is_on

    def transmit(self, msg: bytes):
        """
        Transmits data simulating SPI communication, considering that you are a slave.

        If the master is a MCU, to use this function,
        you must check that your peripheral is selected, using is_selected function.
        If this peripheral is not selected, this function raises an exception.

        Args:
            msg: message to send through SPI
        """
        if self._chip_select != None and self._is_selected():
            self._transmission_queue.put(msg)
        else:
            raise Exception("This peripheral is not selected")

    def receive(self) -> bytes:
        """
        Receives data simulating SPI communication, considering that you are a slave.

        If the master is a MCU, to use this function,
        you must check that your peripheral is selected, using is_selected function.
        If this peripheral is not selected, this function raises an exception.
        """
        if self._chip_select != None and self._is_selected():
            return super().receive()
        else:
            raise Exception("This peripheral is not selected")
