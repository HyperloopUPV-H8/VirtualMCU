import socket, queue
from threading import Thread
from abc import ABC, abstractmethod
from pin.pinout import Pinout
from shared_memory import SharedMemory
from test_lib.input.input import Input
from test_lib.condition.condition import Condition, ConditionFailedException
from services.communications.packets.spipacket import SPIPacket


class SPIPeripheral(ABC):
    """
    This is an abstract class that represent an SPI peripheral.
    The protocol simulation has been implemented using a very simple command protocol:
    if you are a master, you must send commands to the slave before send any packet to
    select the slave. The commands are this:
    - SLAVE_SELECT: this command is sended under the number '1'
    - SLAVE_DESELECT: this command is sended under the number '2'
    - NORMAL_PACKET: this command is sended under the number '0',
        followed by the message intented to send.
    To the other side, if you are a slave, you must check the command before processing the data.
    Communication itself has been implemented using UDP protocol.
    Messages are handled using queues and threads, one for transmission and other for reception.
    """

    @abstractmethod
    def _send(self):
        pass

    @abstractmethod
    def _recv(self):
        pass

    def __init__(self, ip, port):
        self.socket = socket.socket(
            type=socket.SOCK_DGRAM
        )  # Socket used to send and receive SPI data
        self.socket.bind((ip, port))

        self.transmission_queue = (
            queue.Queue()
        )  # Queue used to store messages that should be sended
        self.reception_queue = queue.Queue()  # Queue used to store received messages
        self.transmission_thread = Thread(
            target=self._send, args=("Transmitter")
        )  # Thread that manages data transmission
        self.reception_thread = Thread(
            target=self._recv, args=("Receiver")
        )  # Thread that manages data reception

        self.transmission_thread.start()
        self.reception_thread.start()

    def receive(self) -> bytes:
        return self.reception_queue.get

    @abstractmethod
    def transmit(self):
        pass

    def __del__(self):
        self.stop = True
        self.transmission_thread.join()
        self.reception_thread.join()
        self.socket.close()

    def generate_send_raw(self, data: bytes) -> Input:
        return SPIInput(self, data)

    def generate_send_packet(self, types: str, *data) -> Input:
        packet = SPIPacket(types)
        packet.build(data)
        return self.generate_send_raw(self, packet.data)

    def wait_for_raw(self, data: bytes) -> Condition:
        return SPICondition(self, data)

    def wait_for_packet(self, packet: SPIPacket) -> Condition:
        return SPICondition(self, packet.data)


class SPIInput(Input):
    def __init__(self, spi: SPIPeripheral, data: bytes):
        self._data = data
        self._spi = spi

    def apply(self):
        self._spi.transmit(self._data)


class SPICondition(Condition):
    def __init__(self, spi: SPIPeripheral, data: bytes):
        self._data = data
        self._spi = spi

    def check(self):
        if self._spi.receive() != self._data:
            raise ConditionFailedException()


class SPIMaster(SPIPeripheral):
    def _send(self):
        while not self.stop:
            msg = self.transmission_queue.get
            total_sent = 0
            while total_sent < len(msg):
                sent = self.socket.sendto(msg[sent:], self.send_address)
                if sent == 0:
                    raise RuntimeError("Socket connection broken")
                total_sent += sent

    def _recv(self):
        while not self.stop:
            received = self.socket.recv(1024)
            self.reception_queue.put(received)

    def transmit(self, msg, ip_slave, port_slave):
        """
        Transmits data simulating SPI communication, considering that you are a Master.

        Args:
            msg: message to be sended
            ip_slave: ip address of the slave you want to select and send the data
            port_slave: port of the slave you want to select and send the data
        """
        if self.send_address != (ip_slave, port_slave):
            self.transmission_queue.put(b"2")  # Sending SLAVE_DESELECT command
            self.send_address = (ip_slave, port_slave)
            self.transmission_queue.put(b"1")  # Sending SLAVE_SELECT command
        self.transmission_queue.put(b"0" + msg)


class SPISlave(SPIPeripheral):
    def _send(self):
        while not self.stop and self._selected:
            msg = self.transmission_queue.get
            total_sent = 0
            while total_sent < len(msg):
                sent = self.socket.sendto(msg[sent:], self.send_address)
                if sent == 0:
                    raise RuntimeError("Socket connection broken")
                total_sent += sent

    def _recv(self):
        while not self.stop:
            received = self.socket.recv(1024)
            if received[0] == 1:  # Received SLAVE_SELECT command
                self.selected = True
            elif received[0] == 2:  # Received SLAVE_DESELECT command
                self.selected = False
            else:
                self.reception_queue.put(received[1:])

    def __init__(self, ip, port, ip_master, port_master, SS: Pinout = None):
        super().__init__(ip, port)
        self.send_address = (
            ip_master,
            port_master,
        )  # Address of the client that should receive de data sended
        self.ss = SS  # MCU Slave select Pin "connected" to this peripheral. It has sense only if the master is a MCU
        self._selected = False  # Flag used to control that we send data only if we are selected by the master

    def is_selected(self) -> bool:
        """
        Returns:
            bool: if this peripheral is selected, meaning that it has his SS Pin activated in Shared Memory
        """
        pin = SharedMemory.get_pin(self.SS, pin.PinType.SPI)
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
        if self.SS != None and self.is_selected:
            self.transmission_queue.put(msg)
        else:
            raise Exception("This peripheral is not selected")

    def receive(self) -> bytes:
        """
        Receives data simulating SPI communication, considering that you are a slave.

        If the master is a MCU, to use this function,
        you must check that your peripheral is selected, using is_selected function.
        If this peripheral is not selected, this function raises an exception.
        """
        if self.SS != None and self.is_selected:
            return super().receive()
        else:
            raise Exception("This peripheral is not selected")
