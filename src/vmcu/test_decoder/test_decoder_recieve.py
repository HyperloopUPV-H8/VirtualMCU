from src.services.communications.DatagramSocket import DatagramSocket
from src.services.communications.Decoder_Data import Decoder
import time



ds = DatagramSocket('127.0.0.1', 8800, '127.0.0.1', 8801)

package_data = [(100, "temp:float32,is_active:bool,state:enum(idle-fault)"), (101, "preasure:int32")] #I assume that it's the format, it might change
dec = Decoder(package_data, ds)
dec.start()

while 1:
    time.sleep(1)
    temp = dec['temp']
    is_active = dec['is_active']
    state = dec['state']
    preasure = dec['preasure']
    print(f'T={temp} A={is_active} S={state} P={preasure}')