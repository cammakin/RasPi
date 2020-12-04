from CUSTOM_PACKAGES import IC_MCP23S08 as io_expander
import time

A0_ADDR = 0 
A1_ADDR = 0

ic = io_expander.IC_MCP23S08(A0_ADDR, A1_ADDR)
ic.config_io_dir(0x00)
ic.test_module()

#for num in range(0,10):
 #   print(ic.READ_REG(num))

print("****************")
print(bin(ic.READ_REG(0x00)[2]))
ic.WRITE_GPIO_PIN(2, 1)
print((ic.READ_GPIO_PIN(2)))

time.sleep(10)
ic.cleanup()