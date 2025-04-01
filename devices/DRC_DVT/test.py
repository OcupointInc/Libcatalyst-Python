from libcatalyst.drivers.ftdi_driver import FTDISPIDriver
from libcatalyst.sensors.io_expanders.MCP23S17T import MCP23S17T

# Enable debug to have it print all registers being written
driver = FTDISPIDriver("configs/DRC_DVT_FTDI.json", debug=False)
cs_pins = ["CS_IO0", "CS_IO1", "CS_IO2", "CS_IO3", "CS_IO4", "CS_IO5", "CS_IO6"]

# Set all pins to be outputs and set them low initially
io_expanders = {}  # Store io_expander instances for later use
for cs in cs_pins:
    io_expander = MCP23S17T(driver, cs)
    io_expander.set_bank_direction("A", 0x00)
    io_expander.set_bank_direction("B", 0x00)
    io_expander.write_bank_state("A", 0x00)
    io_expander.write_bank_state("B", 0x00)
    io_expanders[cs] = io_expander

# Set all of the enable bits to their predefined states as specified in the comments.

# Table to use digital logic for everything
#IO Expander CS	Pin Name	Bank 	Index	Name	State
#5	GPA1			A	1	SEL10	0
#4	GPB0			B	0	SEL17	0
#5	GPB5			B	5	SEL2	0
#4	GPA3			A	3	SEL21	0
#5	GPB4			B	4	SEL3	1
#5	GPB3			B	3	SEL32	0
#5	GPA7			A	7	SEL33	1
#5	GPB0			B	0	SEL34	0
#5	GPA3			A	3	SEL35	0
#5	GPA2			A	2	SEL36	1
#4	GPB5			B	5	SEL40	0
#4	GPB3			B	3	SEL46	0
#4	GPA7			A	7	SEL48	1
#4	GPA6			A	6	SEL50	0
#4	GPA2			A	2	SEL51	1
#4	GPA1			A	1	SEL55	0
#5	GPA6			A	6	SEL6	0
#4	GPB4			B	4	SEL74	1
#5	GPB6			B	6	SPDT_EN	1
#4	GPB6			B	6	SPDT_EN2	1

# Access specific IO expanders.
io_expander_cs5 = io_expanders["CS_IO5"]
io_expander_cs4 = io_expanders["CS_IO4"]


# Set individual bits to their specified states.
io_expander_cs5.set_bit("A", 1, 0) # SEL10
io_expander_cs4.set_bit("B", 0, 0) # SEL17
io_expander_cs5.set_bit("B", 5, 0) # SEL2
io_expander_cs4.set_bit("A", 3, 0) # SEL21
io_expander_cs5.set_bit("B", 4, 1) # SEL3
io_expander_cs5.set_bit("B", 3, 0) # SEL32
io_expander_cs5.set_bit("A", 7, 1) # SEL33
io_expander_cs5.set_bit("B", 0, 0) # SEL34
io_expander_cs5.set_bit("A", 3, 0) # SEL35
io_expander_cs5.set_bit("A", 2, 1) # SEL36
io_expander_cs4.set_bit("B", 5, 0) # SEL40
io_expander_cs4.set_bit("B", 3, 0) # SEL46
io_expander_cs4.set_bit("A", 7, 1) # SEL48
io_expander_cs4.set_bit("A", 6, 0) # SEL50
io_expander_cs4.set_bit("A", 2, 1) # SEL51
io_expander_cs4.set_bit("A", 1, 0) # SEL55
io_expander_cs5.set_bit("A", 6, 0) # SEL6
io_expander_cs4.set_bit("B", 4, 1) # SEL74
io_expander_cs5.set_bit("B", 6, 1) # SPDT_EN
io_expander_cs4.set_bit("B", 6, 1) # SPDT_EN2

# Set all other bits high.
for cs in cs_pins:
    io_expander = io_expanders[cs]
    for bank in ["A", "B"]:
        for i in range(8):
            #Check if it's the correct IO expander and bit number that we've already set. If so, skip setting it to 1, as we already set it to its pre-defined state
            if cs == "CS_IO5" and bank == "A" and i == 1: #SEL10
                continue
            if cs == "CS_IO4" and bank == "B" and i == 0: #SEL17
                continue
            if cs == "CS_IO5" and bank == "B" and i == 5: #SEL2
                continue
            if cs == "CS_IO4" and bank == "A" and i == 3: #SEL21
                continue
            if cs == "CS_IO5" and bank == "B" and i == 4: #SEL3
                continue
            if cs == "CS_IO5" and bank == "B" and i == 3: #SEL32
                continue
            if cs == "CS_IO5" and bank == "A" and i == 7: #SEL33
                continue
            if cs == "CS_IO5" and bank == "B" and i == 0: #SEL34
                continue
            if cs == "CS_IO5" and bank == "A" and i == 3: #SEL35
                continue
            if cs == "CS_IO5" and bank == "A" and i == 2: #SEL36
                continue
            if cs == "CS_IO4" and bank == "B" and i == 5: #SEL40
                continue
            if cs == "CS_IO4" and bank == "B" and i == 3: #SEL46
                continue
            if cs == "CS_IO4" and bank == "A" and i == 7: #SEL48
                continue
            if cs == "CS_IO4" and bank == "A" and i == 6: #SEL50
                continue
            if cs == "CS_IO4" and bank == "A" and i == 2: #SEL51
                continue
            if cs == "CS_IO4" and bank == "A" and i == 1: #SEL55
                continue
            if cs == "CS_IO5" and bank == "A" and i == 6: #SEL6
                continue
            if cs == "CS_IO4" and bank == "B" and i == 4: #SEL74
                continue
            if cs == "CS_IO5" and bank == "B" and i == 6: #SPDT_EN
                continue
            if cs == "CS_IO4" and bank == "B" and i == 6: #SPDT_EN2
                continue
            io_expander.set_bit(bank, i, 1)