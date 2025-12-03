import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import requests
import time

# ---------- CONFIG ----------
DEVICE_ID = "testdevice1"
SERVER_URL = "http://192.168.43.197:8000"
PORT = "/dev/ttyUSB0"   # Change this for Raspberry Pi
BAUD = 9600
# ----------------------------


# ------------------ PZEM INITIALIZE ------------------
def init_pzem():
    try:
        master = modbus_rtu.RtuMaster(
            serial.Serial(
                port=PORT,
                baudrate=BAUD,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )
        )
        master.set_timeout(1.0)
        print("PZEM V1 connected successfully.")
        return master
    except Exception as e:
        print("PZEM connection error:", e)
        return None


# ------------------ READ PZEM VALUES ------------------
def read_pzem(master):
    try:
        data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

        voltage = data[0] / 10.0
        current = ((data[1] | (data[2] << 16))) / 1000.0
        power = (data[3] | (data[4] << 16))
        energy = (data[5] | (data[6] << 16)) / 1000.0  # Wh → kWh

        return voltage, current, energy

    except Exception as e:
        print("Error reading PZEM:", e)
        return None, None, None


# ------------------ API: SEND READING ------------------
def send_reading(kwh, voltage, ampere):
    url = SERVER_URL + "/api/reading/add/"
    data = {
        "device_id": DEVICE_ID,
        "kilowatt_hours": kwh,
        "voltage": voltage,
        "ampere": ampere
    }

    try:
        r = requests.post(url, json=data)
        print("Reading sent:", r.json())
    except Exception as e:
        print("Error sending reading:", e)


# ------------------ API: CHECK COMMANDS ------------------
def check_commands():
    url = SERVER_URL + "/api/commands/" + DEVICE_ID + "/"

    try:
        r = requests.get(url)
        data = r.json()

        if data["status"] == "success":
            for cmd in data["commands"]:
                command_id = cmd["command_id"]
                command = cmd["command"]

                print("Received command:", command)

                if command == "turn_off":
                    print("Turning OFF relay")
                    success = True
                elif command == "turn_on":
                    print("Turning ON relay")
                    success = True
                else:
                    success = False

                update_command(command_id, "executed" if success else "failed")

    except Exception as e:
        print("Error checking commands:", e)


# ------------------ API: UPDATE COMMAND STATUS ------------------
def update_command(command_id, status):
    url = SERVER_URL + "/api/command/update/"
    data = {"command_id": command_id, "status": status}

    try:
        r = requests.post(url, json=data)
        print("Command update:", r.json())
    except Exception as e:
        print("Error updating command:", e)


# ------------------ MAIN LOOP ------------------
master = init_pzem()

while True:
    if master:
        voltage, current, kwh = read_pzem(master)

        if voltage is not None:
            print("Voltage:", voltage, "V")
            print("Current:", current, "A")
            print("Energy:", kwh, "kWh\n")

            send_reading(kwh, voltage, current)

    check_commands()
    time.sleep(10)


