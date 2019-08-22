"""CPU functionality."""

import sys

HLT  = 0b00000001
LDI  = 0b10000010
PRN  = 0b01000111
MUL  = 0b10100010
PUSH = 0b01000101
POP  = 0b01000110
CALL = 0b01010000
RET  = 0b00010001
ADD  = 0b10100000



SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xF4

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        with open(filename) as fp:
            for line in fp:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == '':
                    continue
                val = int(num, 2)
                self.ram[address] = val
                address += 1
        
        # print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            # self.trace()
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False
                sys.exit(1)

            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            
            elif ir == PUSH:
                self.reg[SP] -= 1
                self.ram_write(self.reg[operand_a], self.reg[SP])
                self.pc += 2
            
            elif ir == POP:
                self.reg[operand_a] = self.ram[self.reg[SP]]
                self.reg[SP] += 1
                self.pc += 2
            
            elif ir == CALL:
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2 
                self.pc = self.reg[operand_a]
                
            elif ir == RET:
                self.pc = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
            
            else:
                print(f'Error: Unknown instruction {ir} at {self.pc}')
                sys.exit(1)


    
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
