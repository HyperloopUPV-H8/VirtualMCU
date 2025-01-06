import struct


class Packets:
    def __init__(self,packets): 
        self._dict_packets = packets #dictionary for the packets
        self._enum_vector = [[] for _ in range(len(self._dict_packets))] #list of list of strings the index = id_packet 
        
        for packet_id,packet in self._dict_packets.items():
            for data_type in packet:
                if "enum" in data_type:
                    start = data_type.index('(') +1
                    end = data_type.index(')')
                    variants = data_type[start:end].split(',')
                    self._enum_vector[packet_id].append(variants)

    
    def validate_packet(self,packet_id,values):
        #validate id
        self.validate_uint16(packet_id)
        if packet_id not in self._dict_packets:
            raise KeyError(f"Packet ID {packet_id} not found in the map")
        
        expected_sizes = self._dict_packets[packet_id]    
        if len(values) != len(expected_sizes):
            raise ValueError(f"Expected {len(expected_sizes)} but received {len(values)}")
     
    def serialize_packet(self,packet_id,*values):
        self.validate_packet(packet_id,values)        
        binary_packet = struct.pack('<H',packet_id)
        enums_visited = 0
        for value, data_type in zip(values,self._dict_packets[packet_id]):
            match data_type:
                case "uint8" : 
                    self.validate_uint8(value)
                    binary_packet += struct.pack('<B',value)
                case data_type if data_type.startswith("enum"):
                    value = self.validate_enum(value,enums_visited,packet_id)
                    binary_packet += struct.pack('<B',value)
                    enums_visited +=1
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
    
    def validate_enum(self,value,enums_visited,packet_id) -> int:
        if packet_id >= len(self._enum_vector) or enums_visited >= len(self._enum_vector[packet_id]):
            raise IndexError(f"Invalid enum access: packet_id {packet_id}, number of enum: {enums_visited}")
        
        list_enum_packets = self._enum_vector[packet_id]
        enum_variants = list_enum_packets[enums_visited]
            
        if isinstance(value,str):
          
            if value in enum_variants:
                return enum_variants.index(value)
            else:
                raise ValueError(f"Value: {value} no se encuentra en el enum")
                
        if isinstance(value,int) and (0 <= value <= len(enum_variants)):
            return value
        
        raise ValueError(f"Invalid enum value: {value}. Must be a valid string or integer within enum range.")
        
    
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
        
        
        
def main():
    # Definición de paquetes con sus respectivos tipos de datos
    packets = {
        0: ["uint8", "enum(RED,GREEN,BLUE)", "enum(ON,OFF)","enum(sleep,coding,eating)"],  # Paquete con un uint8, un enum y un int16
        1: ["uint16", "enum(ON,OFF)", "float32"],       # Paquete con un uint16, un enum y un float32
    }

    # Inicialización de la clase Packets
    packet_handler = Packets(packets)
    serialized = None
    # Prueba del paquete 0
    try:
        packet_id = 0
        values = [10, "GREEN","OFF",1]  # Valores a serializar
        serialized = packet_handler.serialize_packet(packet_id, *values)
        print(f"Paquete {packet_id} serializado: {serialized.hex()}")
    except Exception as e:
        print(f"Error al serializar paquete {packet_id}: {e}")
    # Prueba del paquete 1
    try:
        packet_id = 1
        values = [65535, "ON", 3.14]  # Valores a serializar
        serialized = packet_handler.serialize_packet(packet_id, *values)
        print(f"Paquete {packet_id} serializado: {serialized.hex()}")
    except Exception as e:
        print(f"Error al serializar paquete {packet_id}: {e}")
    # Prueba con un valor fuera de rango para uint8
    try:
        packet_id = 0
        values = [300, "BLUE", 100]  # Valores fuera de rango
        serialized = packet_handler.serialize_packet(packet_id, *values)
        print(f"Paquete {packet_id} serializado: {serialized}")
    except Exception as e:
        print(f"Error al serializar paquete {packet_id} con valor fuera de rango: {e}")
    # Prueba con un valor no incluido en el enum
    try:
        packet_id = 0
        values = [20, "YELLOW", 100]  # "YELLOW" no está en el enum
        serialized = packet_handler.serialize_packet(packet_id, *values)
        print(f"Paquete {packet_id} serializado: {serialized}")
    except Exception as e:
        print(f"Error al serializar paquete {packet_id} con valor inválido para enum: {e}")
    # Prueba con un paquete no definido
    try:
        packet_id = 99  # ID de paquete no definido
        values = [10, "ON", 3.14]
        serialized = packet_handler.serialize_packet(packet_id, *values)
        print(f"Paquete {packet_id} serializado: {serialized}")
    except Exception as e:
        print(f"Error al serializar paquete no definido {packet_id}: {e}")
 

if __name__ == "__main__":
    main()
