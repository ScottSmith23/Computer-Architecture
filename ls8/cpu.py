"""CPU functionality."""

import sys
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 10
        self.reg = [None] * 10
        self.pc = 0
        self.running = True


    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self,pc,val):
        self.ram[pc] = val

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
        #elif op == "SUB": etc
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

    def ldi(self, regval, value):
        self.reg[regval] = value

    def prn(self, regval):
        print(self.reg[regval])

    def HLT(self):
        self.running = False

    def run(self):
        """Run the CPU."""

        HLT = 1
        LDI = 0b10000010 
        PRN = 0b01000111
        op_a = self.ram[self.pc + 1]
        op_b = self.ram[self.pc + 2]

        while self.running:
            instruction = self.ram_read(self.pc)

            if instruction == HLT:
                self.HLT()
            elif instruction == LDI:
                self.ldi(op_a,op_b)
                self.pc += 3
            elif instruction == PRN:
                self.prn(op_a)
                self.pc += 2
            else:
                print('instruction error')
