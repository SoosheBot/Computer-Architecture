"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
         
    # instructions suggested adding mar and mdr to CPU class for read and write
    def ram_read(self, mar):
        return self.ram[mar]

    # see above
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
       

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as program:
            for instruction in program:
                value = instruction.split("")[0].strip()
                if value == "":
                    continue
                x = int(value, 2)
                self.ram[address] = x
                address += 1

        # Commented out the hardcoded program
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] == self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                return True
            else:
                return False
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def push_val(self, value):
        self.reg[self.sp] -= 1
        self.ram_write(value, self.reg[self.sp])
    
    def pop_val(self):
        value = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        return value

    # def LDI(self, operand_a, operand_b):

    def run(self):
        self.pc = 0
        run_instructions = {
            1: self.HLT,
            17: self.RET,
            71: self.PRN,
            69: self.PUSH,
            70: self.POP,
            80: self.CALL,
            130: self.LDI,
            160: self.ADD,
            162: self.MUL,
            84: self.JMP,
            85: self.JEQ,
            86: self.JNE,
            167: self.CMP,
           }
        while not False:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            run_instructions[IR](operand_a, operand_b)

        return True
