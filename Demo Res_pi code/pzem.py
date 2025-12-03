import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import time

try:
    master = modbus_rtu.RtuMaster(
        serial.Serial(
            port="COM4",     # <-- change if needed
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1
        )
    )

    master.set_timeout(1.0)
    # master.set_rtu_byte_timeout(1.0)  # REMOVE THIS LINE - your version doesn't support it

    slave_id = 1

    print("Reading PZEM-004T V1...")

    while True:
        # Read 10 input registers starting from 0
        data = master.execute(slave_id, cst.READ_INPUT_REGISTERS, 0, 10)

        # Decode PZEM V1 values
        voltage = data[0] / 10.0
        current = ((data[1] & 0xFFFF) | (data[2] << 16)) / 1000.0
        power   = ((data[3] & 0xFFFF) | (data[4] << 16))
        energy  = ((data[5] & 0xFFFF) | (data[6] << 16))

        print("--------------------------------")
        print("Voltage:", voltage, "V")
        print("Current:", current, "A")
        print("Power:  ", power, "W")
        print("Energy: ", energy, "Wh")
        print("--------------------------------\n")

        time.sleep(1)

except Exception as e:
    print("Error:", e)
