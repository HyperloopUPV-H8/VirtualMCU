import threading
import struct
import re

def calculate_byte_size(measurements):

    size = 0
    for measure in measurements:
        if measure == 'uint8' or measure == 'int8' or measure == 'bool' or 'enum' in measure:
            size += 1
        elif measure == 'uint16' or measure == 'int16':
            size += 2
        elif measure == 'uint32' or measure == 'int32' or measure == 'float32':
            size += 4
        elif measure == 'uint64' or measure == 'int64' or measure == 'float64':
            size += 8
              
    return size
class Decoder:
    def __init__(self, package_data, ds): #package_data its a array that contains string id and string with all measurements
        self.dict_measurement_types = {} #key string id of each measurament, contains an array from types
        self.dict_measurement_names = {} #contains array of names of each variable
        self.dict_measurement_value = {} #contains the value of each measurement
        self.dict_measurement_size = {} #contains size for each packet 
        self.ds = ds #datagramsocket

        for id, measurements in package_data.items():
            
            measurements_split = measurements.split(',')
            arr_measuremets = []
            arr_names = []
            for measure in measurements_split:
                pair = measure.split(':')
                arr_names.append(pair[0])
                arr_measuremets.append(pair[1])
                self.dict_measurement_value[pair[0]] = None

            self.dict_measurement_types[id] = arr_measuremets
            self.dict_measurement_names[id] = arr_names
            self.dict_measurement_size[id] = calculate_byte_size(arr_measuremets)

        self.recv_packet_thread = threading.Thread(target=self._recv_packet, daemon=True)
        self.recv_packet_running = False
    
    def start(self):
        self.recv_packet_running = True
        self.recv_packet_thread.start()

    def _recv_packet(self):
        buff = bytearray()
        id_packet = 0
        bytes_size = 0
        wait_new_packet = True

        while self.recv_packet_running:
            try:
                raw_data = self.ds.get_packet()
                buff += raw_data
                if wait_new_packet:
                    id_packet = struct.unpack('<H',buff[:2])[0]
                    buff = buff[2:]
                    
                    bytes_size = self.dict_measurement_size[id_packet]
                    wait_new_packet = False

                while len(buff) >= bytes_size and len(buff)>0:
                    data_buff = buff[:bytes_size]
                    buff = buff[bytes_size:]
                    self.deserialize(data_buff, id_packet)

                    if len(buff) >= 2:
                        id_packet = struct.unpack('<H',buff[:2])[0]
                        buff = buff[2:]
                        bytes_size = self.dict_measurement_size[id_packet]
                    else:  
                        bytes_size = 0
                        wait_new_packet = True
            except KeyError as e:
                print(f"Error to obtain key: {e}")
                buff.clear()
                bytes_size=0
                wait_new_packet = True
            except struct.error as e:
                print(f'Unpacking error: {e}')
                buff.clear()
                bytes_size=0
                wait_new_packet = True


            
                
    def deserialize(self, buffer, id_packet):

        for type, name in zip(self.dict_measurement_types[id_packet], self.dict_measurement_names[id_packet]):
            data = None
            match type:
                case "bool":
                    data = 'True' if struct.unpack('<B', buffer[:1])[0] else 'False'
                    buffer = buffer[1:]
                case "uint8":
                    data = struct.unpack('<B', buffer[:1])[0]
                    buffer = buffer[1:]
                case "int8":
                    data = struct.unpack('<b', buffer[:1])[0]
                    buffer = buffer[1:]
                case "uint16":
                    data = struct.unpack('<H', buffer[:2])[0]
                    buffer = buffer[2:]
                case "int16":
                    data = struct.unpack('<h', buffer[:2])[0]
                    buffer = buffer[2:]
                case "uint32":
                    data = struct.unpack('<I', buffer[:4])[0]
                    buffer = buffer[2:]
                case "int32":
                    data = struct.unpack('<i', buffer[:4])[0]
                    buffer = buffer[4:]
                case "float32":
                    data = struct.unpack('<f', buffer[:4])[0]
                    buffer = buffer[4:]
                case "uint64":
                    data = struct.unpack('<Q', buffer[:8])[0]
                    buffer = buffer[8:]
                case "int64":
                    data = struct.unpack('<q', buffer[:8])[0]
                    buffer = buffer[8:]
                case "float64":
                    data = struct.unpack('<d', buffer[:8])[0]
                    buffer = buffer[8:]
                case _:
                    if 'enum' in type:
                        value_data = struct.unpack('<B', buffer[:1])[0]
                        buffer = buffer[1:]
                        valores = (re.search(r'\((.*?)\)', type)).group(1).split('-')
                        data = valores[value_data]
                        
                    else:
                        raise ValueError(f"Unsupported data type: {type}")
            
            self.dict_measurement_value[name] = data
            

    
    def __getitem__(self, key):
        
        if key in self.dict_measurement_value:
            return self.dict_measurement_value[key]
        else:
            print("The key is not include in the dictionary")
            return None

    def stop(self):
        self.recv_packet_running = False
        self.recv_packet_thread.join()
        self.ds.stop()

    def __del__(self):
        self.stop()
