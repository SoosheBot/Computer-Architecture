"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # the RAM
        self.reg = [0] * 8 # registers
        self.pc = 0 # counts the program
        self.SP = 7 # points to the stack
        self.MAR = None # memory address register
        self.MDR = None # memory data register
        self.running = False # is the program running default False
        self.equal = False # E flag, default, false
         
  
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.equal = True
            else:
                self.equal = False
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
    
    # instructions suggested adding MAR and MDR to CPU class for ram_read and ram_write
    # reads the RAM -- helper function
    def ram_read(self, address):
        self.MAR = address
        self.MDR = self.ram[self.MAR]
        return self.MDR

    # see above
    # writes to the RAM -- helpr function
    def ram_write(self, address, value):
        self.MAR = address
        self.MDR = value
        self.ram[self.MAR] = self.MDR


    # defines a push value to set up the PUSH function -- helper function
    def push_val(self, value):
        self.reg[self.SP] -= 1
        self.ram_write(value, self.reg[self.SP])
    


    # defines a pop value to set up the POP function -- helper function
    def pop_val(self):
        value = self.ram_read(self.reg[self.SP])
        self.reg[self.SP] += 1
        return value

    # Sets the value of a register to an integer.
    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3



    # Prints the numeric value stored in the given register.
    # Prints the decimal integer value that is stored in the given register to the console
    def PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2
    


    # Halts the CPU (and exits the emulator).
    def HLT(self, operand_a, operand_b):
        self.pc += 1
        sys.exit(0)
    


    # Pushes the value in the given register on the stack.
    # Decrements the `SP`. (in push_value)
    # Copies the value in the given register to the address pointed to by SP (also in pop_value).
    def PUSH(self, operand_a, operand_b):
        self.push_val(self.reg[operand_a])
        self.pc += 2
    
    # Pops the value at the top of the stack into the given register
    # Copies the value from the address pointed to by `SP` to the given register (pop_value)
    # Increments SP (pop_value)
    def POP(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop_val()
        self.pc += 2
    
    # Calls a subroutine (function) at the address stored in the register. The address of the instruction directly after is pushed on to the stack so we can return to where we left off when the subroutine finishes.
    # The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.
    def CALL(self, operand_a, operand_b):
        self.push_val(self.pc + 2)
        self.pc = self.reg[operand_a]
    
    
    # Returns from the subroutine.
    # Pops the value from the top of the stack and store it in the `PC`.
    def RET(self, operand_a, operand_b):
        self.pc = self.pop_val()



    # Multiplies the values in two registers together and store the result in registerA. This is an alu instruction!
    def MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc +=3



    # Adds the value in two registers and stores the result in registerA.
    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc +=3



    # Jumps to the address stored in the given register.
    # Sets the `PC` to the address stored in the given register.
    def JMP(self, operand_a, operand_b):
        self.pc = self.reg[operand_a]



    # If `equal` flag is set (true), this jumps to the address stored in the given register.
    def JEQ(self, operand_a, operand_b):
        if self.equal == True:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2



    # If `equal` flag is clear (false, 0), this jumps to the address stored in the given register
    def JNE(self, operand_a, operand_b):
        if self.equal == False:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2



    # Compare the values in two registers.
    ## * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
    ## * If registerA is less than registerB, set the Less-than `L` flag to 1, otherwise set it to 0.
    ## * If registerA is greater than registerB, set the Greater-than `G` flag to 1, otherwise set it to 0.
    def CMP(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3



    # Reads the memory address that’s stored in register PC, and stores that result in IR, the Instruction Register
    def run(self):
        self.pc = 0
        run_inst = {
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
        while not self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            run_inst[IR](operand_a, operand_b)

        return self.running
