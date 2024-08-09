import json
import struct

from common import combine_registers, read_test_data, registers_to_float
from pymodbus.client import ModbusSerialClient


class ReadEnergyUnit32():
    client = None

    def __init__(self):
        self._setup()

    def _setup(self):
        self.client = ModbusSerialClient(port='COM5', baudrate=19200, parity='N', stopbits=1, bytesize=8, timeout=1)

    def read_energy(self):
        self.client.connect()
        list_data = read_test_data('test_data_gp_energy.json')
        for modbus_address in list_data:
            regs = self.client.read_holding_registers(address=int(modbus_address[1], 16), count=modbus_address[2],
                                                      slave=1)
            readings = combine_registers(regs.registers[0], regs.registers[1])
            print(f'{modbus_address[0]} : {readings}')
        self.client.close()


class ReadRealTimeParameterFloat():
    client = None

    def __init__(self):
        self._setup()

    def _setup(self):
        self.client = ModbusSerialClient(port='COM5', baudrate=19200, parity='N', stopbits=1, bytesize=8, timeout=1)

    def read_real_time_parameter_float(self):
        self.client.connect()
        list_data = read_test_data('test_data_gp_real_time_parameter.json')
        for modbus_address in list_data:
            regs = self.client.read_holding_registers(address=int(modbus_address[1], 16), count=modbus_address[2],
                                                      slave=1)
            readings = registers_to_float(regs.registers[0], regs.registers[1])
            print(f'{modbus_address[0]} : {readings}')
        self.client.close()
