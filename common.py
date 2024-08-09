import json
import struct


def combine_registers(reg1, reg2):
    return (reg1 << 16) | reg2


def read_test_data(file_address):
    with open(file_address, 'r') as f:
        test_data = json.load(f)
    list_data = []
    for item in test_data:
        list_data.append(tuple(item.values()))
    return list_data


# use for converting 2 register values to 1 float value
def registers_to_float(reg1, reg2):
    # Combine the two 16-bit registers into a 32-bit integer
    combined_registers = (reg1 << 16) | reg2
    # Convert the 32-bit integer to 4 bytes
    combined_bytes = combined_registers.to_bytes(4, byteorder='big')
    # Unpack the bytes as a 32-bit float
    float_value = struct.unpack('>f', combined_bytes)[0]
    return float_value
