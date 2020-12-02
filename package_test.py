from CUSTOM_PACKAGES import IC_MCP23S08 as io_expander
import time

A0_ADDR = 0 
A1_ADDR = 0

ic = io_expander.IC_MCP23S08(A0_ADDR, A1_ADDR)
time.sleep(10)