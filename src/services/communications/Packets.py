import struct


class Packets:
    def __init__(self,packets): 
        #packets is a dict where key -> id value -> data_type
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
     
    def serialize_packet(self,packet_id,*values):
        self.validate_packet(packet_id,values)        
        binary_packet = struct.pack('<H',packet_id)
        for value, data_type in zip(values,self._dict_packets[packet_id]):
            match data_type:
                case "uint8" : 
                    self.validate_uint8(value)
                    binary_packet += struct.pack('<B',value)
                case "enum":
                    self.validate_enum(value)
                    binary_packet += struct.pack('<B',value)
                case "int8": 
                    self.validate_int8(value)
                    binary_packet += struct.pack('<b',value)
                case "uint16" : 
                    self.validate_uint16(value)
                    binary_packet += struct.pack('<H',value)
                case "int16": 
                    self.validate_int16(value)
                    binary_packet += struct.pack('<h',value)
                case "uint32": 
                    self.validate_uint32(value)
                    binary_packet += struct.pack('<I',value)
                case "int32" : 
                    self.validate_int32(value)
                    binary_packet += struct.pack('<i',value)
                case "float32" : 
                    self.validate_float32(value)
                    binary_packet += struct.pack('<f',float(value))
                case "uint64": 
                    self.validate_uint64(value)
                    binary_packet += struct.pack('<Q',value)
                case "int64": 
                    self.validate_int64(value)
                    binary_packet += struct.pack('<q',value)
                case "float64" : 
                    self.validate_float64(value)
                    binary_packet += struct.pack('<d',float(value))
                case _:
                    raise ValueError(f"Unsupported data type: {data_type}") 
        return binary_packet
    
    def validate_enum(self,value):
        if not (0 <= value <= 255) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for uint8 or not the data_type expected")
    
    def validate_uint8(self,value):
         if not (0 <= value <= 255) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for uint8 or not the data_type expected")
        
    def validate_int8(self,value):
        if not (-128 <= value <= 127) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for int8 or not the data_type expected")
    def validate_uint16(self,value):
        if not (0 <= value <= 0xFFFF) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for uint16 or not the data_type expected")
    
    def validate_int16(self,value):
        if not (-0x8000 <= value <= 0x7FFF) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for int16 or not the data_type expected")
    
    def validate_uint32(self,value):
         if not (0 <= value <= 0xFFFFFFFF) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for uint32 or not the data_type expected")
    def validate_int32(self,value):
         if not (-0x80000000 <= value <= 0x7FFFFFFF) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for int32 or not the data_type expected")
    def validate_uint64(self,value):
        if not (0 <= value <= 0xFFFFFFFFFFFFFFFF) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for uint64 or not the data_type expected")
    
    def validate_int64(self,value):
        if not (-0x8000000000000000 <= value <= 0x7FFFFFFFFFFFFFFF) or not isinstance(value,int):
            raise ValueError(f"Value {value} out of range for int64 or not the data_type expected")
        
    def validate_float32(self,value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError(f"Value {value} is not a valid float32")
    
    def validate_float64(self,value):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError(f"Value {value} is not a valid float64")