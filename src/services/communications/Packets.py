import struct


class Packets:
    def __init__(self,*packets): 
        #packets is a list where first goes an ID uint16_t and then string with types
        self._dict_packets = {}
        for packet in packets:
            if len(packet) < 1:
                raise ValueError ("Every packet need a ID at least")
            if not isinstance(packet[0],int) or not (0 <= packet[0] <= 0xFFFF):
                raise ValueError(f"The id must be an uint16_t, {packet[0]}")
            id = packet[0]
            self._dict_packets[id] = list()
            for data_type in packet[1:]:
                if data_type == "enum":
                    enum_names = None
                    for names in data_type:
                      enum_names.append(data_type)
                    self._dict_packets[id].append({data_type,enum_names})
                else:
                    self._dict_packets[id].append(data_type)

    
    def validate_packet(self,packet_id,values):
        #validate id
        if packet_id not in self._dict_packets:
            raise KeyError(f"Packet ID {packet_id} not found in the map")
        
        expected_sizes = self._dict_packets[packet_id]    
        if len(values) != len(expected_sizes):
            raise ValueError(f"Expected {len(expected_sizes)} but received {len(values)}")
        #validate types
        for value,data_type in zip(values,self._dict_packets[packet_id]):
            match data_type:
                case "uint8" | "enum":
                    if not (0 <= value <= 255) or not isinstance(value,int):
                        raise ValueError(f"Value {value} out of range for uint8 or not the data_type expected")
                case "int8":
                    if not (-128 <= value <= 127) or not isinstance(value,int):
                        raise ValueError(f"Value {value} out of range for int8 or not the data_type expected")
                case "uint16":
                    if not (0 <= value <= 0xFFFF) or not isinstance(value,int):
                        raise ValueError(f"Value {value} out of range for uint16 or not the data_type expected")
                case "int16":
                    if not (-0x8000 <= value <= 0x7FFF) or not isinstance(value,int):
                        raise ValueError(f"Value {value} out of range for int16 or not the data_type expected")
                case "uint32":
                    if not (0 <= value <= 0xFFFFFFFF) or not isinstance(value,int):
                        raise ValueError(f"Value {value} out of range for uint32 or not the data_type expected")
                case "int32":
                    if not (-0x80000000 <= value <= 0x7FFFFFFF) or not isinstance(value,int):
                        raise ValueError(f"Value {value} out of range for int32 or not the data_type expected")
                case "float32":
                    if not (isinstance(value, float) or isinstance(value, int)):
                        raise ValueError(f"Value {value} is not a valid float32")
                case "uint64":
                    if not (0 <= value <= 0xFFFFFFFFFFFFFFFF) or not isinstance(value,int):
                        raise ValueError(f"Value {value} out of range for uint64 or not the data_type expected")
                case "int64":
                    if not (-0x8000000000000000 <= value <= 0x7FFFFFFFFFFFFFFF) or not isinstance(value,int):
                        raise ValueError(f"Value {value} out of range for int64 or not the data_type expected")
                case "float64":
                    if not (isinstance(value, float) or isinstance(value, int)):
                        raise ValueError(f"Value {value} is not a valid float64")
                case _:
                    raise ValueError(f"Unsupported data type: {data_type}")
    
    def serialize_packet(self,packet_id,*values):
        self.validate_packet(packet_id,values)        
        binary_packet = struct.pack('<H',packet_id)
        for value, data_type in zip(values,self._dict_packets[packet_id]):
            match data_type:
                case "uint8" | "enum": 
                    binary_packet += struct.pack('<B',value)
                case "int8": 
                    binary_packet += struct.pack('<b',value)
                case "uint16" : 
                    binary_packet += struct.pack('<H',value)
                case "int16": 
                    binary_packet += struct.pack('<h',value)
                case "uint32": 
                    binary_packet += struct.pack('<I',value)
                case "int32" : 
                    binary_packet += struct.pack('<i',value)
                case "float32" : 
                    binary_packet += struct.pack('<f',float(value))
                case "uint64": 
                    binary_packet += struct.pack('<Q',value)
                case "int64": 
                    binary_packet += struct.pack('<q',value)
                case "float64" : 
                    binary_packet += struct.pack('<d',float(value))
                case _:
                    raise ValueError(f"Unsupported data type: {data_type}") 
        return binary_packet