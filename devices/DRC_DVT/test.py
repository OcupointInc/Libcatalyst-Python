from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.sensors.io_expanders.MCP23S17T import MCP23S17T

# Enable debug to have it print all registers being written
driver = FTDISPIDriver("configs/DRC_DVT_FTDI.json", debug=False)
cs_pins = ["CS_IO0", "CS_IO1", "CS_IO2", "CS_IO3", "CS_IO4", "CS_IO5", "CS_IO6"]

# Set all pins to be outputs and set them low
for cs in cs_pins:
    io_expander = MCP23S17T(driver, cs)
    io_expander.set_bank_direction("A", 0x00)
    io_expander.set_bank_direction("B", 0x00)
    io_expander.write_bank_state("A", 0x00)
    io_expander.write_bank_state("B",0x00)

# Set all of the enable bits high

# Table to use digital logic for everything
#IO Expander CS	Pin Name	Bank 	Index	Name	State
#5	GPA1			SEL10	0
#4	GPB0			SEL17	0
#5	GPB5			SEL2	0
#4	GPA3			SEL21	0
#5	GPB4			SEL3	1
#5	GPB3			SEL32	0
#5	GPA7			SEL33	1
#5	GPB0			SEL34	0
#5	GPA3			SEL35	0
#5	GPA2			SEL36	1
#4	GPB5			SEL40	0
#4	GPB3			SEL46	0
#4	GPA7			SEL48	1
#4	GPA6			SEL50	0
#4	GPA2			SEL51	1
#4	GPA1			SEL55	0
#5	GPA6			SEL6	0
#4	GPB4			SEL74	1
#5	GPB6			SPDT_EN	1
#4	GPB6			SPDT_EN2	1