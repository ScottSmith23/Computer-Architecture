"""CPU functionality."""

import sys
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.sp = 7
        self.reg[self.sp] = 244
        


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
            print("FILE",filename)
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
        print("ldi")

    def prn(self, regval):
        print(self.reg[regval])
        print("print")
        
    def hlt(self):
        self.running = False
        print("halt")

    def mul(self,reg_a,reg_b):
        self.alu("MUL",reg_a,reg_b)
        print("mul")

    def push(self,reg_a):
        self.sp -= 1
        self.ram[self.sp] = self.reg[reg_a]
        print("push")

    def pop(self,reg_a):
        self.reg[reg_a] = self.ram[self.sp]
        self.sp += 1
        print("pop")

    def call(self, register_index):
        print("call")
        self.reg[7] -= 1
         
        next_address = self.pc
        self.ram_write(self.reg[7], next_address)

        self.pc = self.reg[register_index]

    def ret(self):
        print("return")
        # Return from subroutine.
        # Pop the value from the top of the stack and store it in the PC.
        value_to_pop = self.ram[self.reg[7]]
        self.pc = value_to_pop
        self.reg[7] += 1

    def run(self):
        """Run the CPU."""

        HLT = 1
        LDI = 0b10000010 
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        operations = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010000: self.call,
            0b00010001: self.ret,
        }


        while self.running:
            instruction = self.ram_read(self.pc)
            op_a = self.ram[self.pc + 1]
            op_b = self.ram[self.pc + 2]
            print(bin(instruction))
            num_of_args = instruction >> 6
            # move down to next instruction
            self.pc += 1 + num_of_args
            
            if num_of_args == 0:
                operations[instruction]()
            elif num_of_args == 1:
                operations[instruction](op_a)
            elif num_of_args == 2:
                operations[instruction](op_a, op_b)   
            
            else:
                print('instruction error')
                self.hlt()
