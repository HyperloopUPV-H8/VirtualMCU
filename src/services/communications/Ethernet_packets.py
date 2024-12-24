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
                self._dict_packets[id].append(data_type)

    def serialize_packet(self,packet_id,*values):
        if packet_id not in self._dict_packets:
            raise KeyError(f"Packet ID {packet_id} not found in the map")
        
        expected_sizes = self._dict_packets[packet_id]
        
        if len(values) != len(expected_sizes):
            raise ValueError(f"Expected {len(expected_sizes)} but received {len(values)}")
        
        binary_packet = struct.pack('<H',packet_id)
        for value, data_type in zip(values,expected_sizes):
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
                    binary_packet += struct.pack('<f',value)
                case "uint64": 
                    binary_packet += struct.pack('<Q',value)
                case "int64": 
                    binary_packet += struct.pack('<q',value)
                case "float64" : 
                    binary_packet += struct.pack('<d',value)
                case _:
                    raise ValueError(f"Unsupported data type: {data_type}") 
        return binary_packet