# Program is 3 bits (8 values)
# 3 registers (A,B,C)
# 8 instructions (opcode)

# Combo operands 0 through 3 represent literal values 0 through 3.
# Combo operand 4 represents the value of register A.
# Combo operand 5 represents the value of register B.
# Combo operand 6 represents the value of register C.
# Combo operand 7 is reserved and will not appear in valid programs.

# Opcode table
# 0: adv : division: RegA <- int(RegA / 2^^COMBO)
# 1: bxl : bitwiseXor: RegB <- XOR(RegB, LiteralOperand)
# 2: bst : mod8: RegB <- COMBO % 8
# 3: jnz : jump-a: IF(RegA==0, NOOP, IP<-LITERAL)  -- DON'T IP+=2 after
# 4: bxc : bitwiseXor bxc: B <- B XOR C -- operand unused
# 5: out : print(COMBO % 8)
# 6: bdv : division : RegB <- int(RegA / 2^^COMBO)
# 7: cdv : division : RegC <- int(RegA / 2^^COMBO)

OP_CODES_WITH_LITERAL_OPERANDS = {1, 3}
import math


class Computer:
    def __init__(self, a: int, b: int, c: int, program: list[int]):
        self.RegA = a
        self.RegB = b
        self.RegC = c
        self.program = program
        self.ip = 0
        self.output = []

    def run(self):
        while 0 <= self.ip < len(self.program):
            self.tick()
        print(",".join(map(str, self.output)))
        return self

    def tick(self):
        # Responsible for incrementing the IP appropriatley after itself, since jnz messes things up
        if self.op_code == 0:
            self.RegA = int(self.RegA / math.pow(2, self.operand))
        elif self.op_code == 1:
            self.RegB = self.RegB ^ self.operand
        elif self.op_code == 2:
            self.RegB = self.operand % 8
        elif self.op_code == 3 and self.RegA != 0:
            self.ip = self.operand
            return  # Return early so we don't increment IP after.
        elif self.op_code == 4:
            self.RegB = self.RegB ^ self.RegC
        elif self.op_code == 5:
            self.output.append(self.operand % 8)
        elif self.op_code == 6:
            self.RegB = int(self.RegA / math.pow(2, self.operand))
        elif self.op_code == 7:
            self.RegC = int(self.RegA / math.pow(2, self.operand))

        self.ip += 2

    @property
    def op_code(self):
        return self.program[self.ip]

    @property
    def operand(self) -> int:
        operand = self.program[self.ip + 1]
        if self.op_code in OP_CODES_WITH_LITERAL_OPERANDS:
            return operand
        if operand <= 3:
            return operand
        if operand == 4:
            return self.RegA
        if operand == 5:
            return self.RegB
        if operand == 6:
            return self.RegC
        raise ValueError(f"Unexpected operand: {operand=} for {op_code}")


# Computer(729, 0, 0, [0, 1, 5, 4, 3, 0]).run()
Computer(64196994, 0, 0, [2, 4, 1, 1, 7, 5, 1, 5, 4, 0, 0, 3, 5, 5, 3, 0]).run()
