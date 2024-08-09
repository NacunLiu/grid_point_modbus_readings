from pymodbus.client import ModbusSerialClient
from common import read_test_data, combine_registers, registers_to_float
import time
import logging
import colorlog


class Settings():
    client = None

    def __init__(self):
        self._setup()

        # 创建控制台处理器
        console_handler = logging.StreamHandler()

        # 设置带颜色的格式
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'blue',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(formatter)

        # 获取或创建日志记录器
        self.logger = logging.getLogger(self.__class__.__name__)

        # 确保没有重复添加处理器
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)

        # 设置日志级别
        self.logger.setLevel(logging.INFO)

    def _setup(self):
        self.client = ModbusSerialClient(port='COM5', baudrate=19200, parity='N', stopbits=1, bytesize=8, timeout=1)

    def settings_test(self):
        self.client.connect()
        list_data = read_test_data('test_data_gp_settings.json')
        readings = []
        # read and compare the register value with default
        for modbus_address in list_data:
            time.sleep(1)
            # if the address is R/W then read the address and see if it's as default
            if modbus_address[3] == 'RW':
                regs = self.client.read_holding_registers(address=int(modbus_address[1], 16), count=modbus_address[2],
                                                          slave=1)
                i = 0
                reading = 0x0000
                while i < modbus_address[2]:
                    if i > 0:
                        reading << 16 | 0x0000
                        reading = reading + regs.registers[i]
                    else:
                        reading = regs.registers[i]
                    i += 1
                if reading == modbus_address[4]:
                    self.logger.info(f" Read Settings PASSED {modbus_address[0]} reading is {reading}")
                else:
                    self.logger.warning(f"FAILED read {modbus_address[0]} failed value is {reading}")

            # elif modbus_address[3] == 'RW':
            #     regs = self.client.read_holding_registers(address=int(modbus_address[1], 16), count=modbus_address[2],
            #                                               slave=1)
            #     # to be compatible with 1 and 2 count register address value use a loop and decision for
            #     # 1 register add value directly
            #     # 2 registers to move 16 bit to left and then add the new value
            #     i = 0
            #     reading = 0x0000
            #     while i < modbus_address[2]:
            #         if i > 0:
            #             reading << 16 | 0x0000
            #             reading = reading + regs.registers[i]
            #         else:
            #             reading = regs.registers[i]
            #         i += 1
            #
            #     self.logger.info(f"{modbus_address[0]} reading is {reading}")
            # # if the address is write only write to the address and see if error happens
            # elif modbus_address[3] == 'W':
            #     resp = self.client.write_registers(address=int(modbus_address[1], 16), count=modbus_address[2], slave=1)
            #     if resp.isError():
            #         self.logger.warning(f"write to modbus address{modbus_address[1]} failed")
            #     else:
            #         regs = self.client.read_holding_registers(address=int(modbus_address[1], 16),
            #                                                   count=modbus_address[2], slave=1)
            #         i = 0
            #         reading = 0x0000
            #         while i < modbus_address[2]:
            #             if i > 0:
            #                 reading << 16 | 0x0000
            #                 reading = reading + regs.registers[i]
            #             else:
            #                 reading = regs.registers[i]
            #             i += 1
            #         try:
            #             assert reading == modbus_address[4]
            #         except Exception as e:
            #             self.logger.warning(f"write to modbus address {modbus_address[1]} failed")

        self.client.close()
