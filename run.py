from grid_point_energy_reading import ReadEnergyUnit32, ReadRealTimeParameterFloat
import time


read_real_time_parameter_float = ReadRealTimeParameterFloat()
read_real_time_parameter_float.read_real_time_parameter_float()

read_energy_unit32 = ReadEnergyUnit32()
read_energy_unit32.read_energy()

time.sleep(60)

read_energy_unit32.read_energy()