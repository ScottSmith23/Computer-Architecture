"""CPU functionality."""

import sys
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.reg = [None] * 10
        self.pc = 0
        self.running = True


    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self,pc,val):
        self.ram[pc] = val

    # def load(self):
    #     """Load a program into memory."""

    #     address = 0

    #     # For now, we've just hardcoded a program:

    #     program = [
    #         # From print8.ls8
    #         0b10000010, # LDI R0,8
    #         0b00000000,
    #         0b00001000,
    #         0b01000111, # PRN R0
    #         0b00000000,
    #         0b00000001, # HLT
    #     ]

    #     for instruction in program:
    #         self.ram[address] = instruction
    #         address += 1

    def load(self,filename):
    # TODO do some logic here
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    # store val in memory
                    self.ram[address] = val

                    address += 1

                    # print(f"{x:08b}: {x:d}")

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b] 
        elif op == "MUL":
            val = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = val
            self.pc += 3             
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

    def hlt(self):
        self.running = False

    def mul(self,reg_a,reg_b):
        self.alu("MUL",reg_a,reg_b)

    def run(self):
        """Run the CPU."""

        HLT = 1
        LDI = 0b10000010 
        PRN = 0b01000111
        MUL = 0b10100010


        while self.running:
            instruction = self.ram_read(self.pc)
            op_a = self.ram[self.pc + 1]
            op_b = self.ram[self.pc + 2]

            if instruction == HLT:
                self.hlt()
            elif instruction == LDI:
                self.ldi(op_a,op_b)
                self.pc += 3
            elif instruction == PRN:
                self.prn(op_a)
                self.pc += 2
            elif instruction == MUL:
                self.mul(op_a,op_b)
            else:
                print('instruction error')
