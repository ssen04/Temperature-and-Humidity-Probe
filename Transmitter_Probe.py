import struct
import time
import datetime
from pyModbusTCP.client import ModbusClient

end = datetime.datetime.now() + datetime.timedelta(hours=48)

print("End date and time: ", end)

probe = ModbusClient(host="192.168.5.20", port=502, unit_id=241, auto_open=True)


# Converts the data from two registers to a 32-bit float
# Takes the holding register data and the index of the register as inputs
# Returns 32-bit float
def data_from_register(registers, i):
    return struct.unpack('!f', bytes.fromhex('{0:04x}'.format(registers[i]) + '{0:04x}'.format(registers[i - 1])))[0]


# Reads the holding registers of the probe and returns the values as 32-bit float
# Returns True, Relative Humidity, Temperature and Dew Point if read successfully
# Returns False, None, None, None if not
def holding_registers_data():
    try:
        registers = probe.read_holding_registers(0, 10)

    except Exception as e:
        print(e)
        return False, None, None, None
    try:
        rh = data_from_register(registers, 1)
        t = data_from_register(registers, 3)
        dp = data_from_register(registers, 9)

    except Exception as e:
        print(e)
        return False, None, None, None

    return True, rh, t, dp


# Logging the data

# Reads relative humidity, temperature and dew point from holding_registers_data() and writes the values to a csv file with the date and time
def data_logger():
    successful, rh, t, dp = holding_registers_data()
    if (successful):
        dt = datetime.datetime.now()

        try:
            with open("datalog.csv", "a") as f:
                line = f"Date and Time: {dt}, RH: {rh}, Temperature: {t}, Dew Point {dp}\n"
                print(line)
                f.write(line)
        except Exception as e:
            print(e)
        probe.close()
        time.sleep(1)

    else:
        probe.close()
        time.sleep(0.5)


def main():
    while datetime.datetime.now() < end:
        data_logger()


if __name__ == "__main__":
    main()
