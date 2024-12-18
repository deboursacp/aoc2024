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
        return self

    def tick(self):
        if self.op_code == 0:
            self.RegA = self.RegA >> self.operand
        elif self.op_code == 1:
            self.RegB = self.RegB ^ self.operand
        elif self.op_code == 2:
            self.RegB = self.operand % 8
        elif self.op_code == 3 and self.RegA != 0:
            self.ip = self.operand
            return  # Return early so we don't increment IP.
        elif self.op_code == 4:
            self.RegB = self.RegB ^ self.RegC
        elif self.op_code == 5:
            self.output.append(self.operand % 8)
        elif self.op_code == 6:
            self.RegB = self.RegA >> self.operand
        elif self.op_code == 7:
            self.RegC = self.RegA >> self.operand

        self.ip += 2

    @property
    def op_code(self):
        return self.program[self.ip]

    @property
    def operand(self) -> int:
        operand = self.program[self.ip + 1]
        if self.op_code in {1, 3}:  # The only opcodes that don't use Combo Operand.
            return operand
        if operand <= 3:
            return operand
        if operand == 4:
            return self.RegA
        if operand == 5:
            return self.RegB
        if operand == 6:
            return self.RegC


# Unsurprisingly, brute forcing doesn't work:
# I can test an A value at about ~20k it/s.
# But the program is like 16 numbers, which means 48 bits (3 bits produces one output), so the right value is somewhere on the order of 2^48.

# Observations about the input program:
# each "loop" iteration (returning to ip=0) shaves off 3 bits of A
# The loop fortunatley doesn't have any branching, so i think i can just analyse the program.
# Only the 10 least significant bits matter for producing the first output (see notes below).

PROGRAM = [2, 4, 1, 1, 7, 5, 1, 5, 4, 0, 0, 3, 5, 5, 3, 0]


# Use backtracking to find a the solution.
# The last output of the program will be determined by the most significant bit(s) of A (up to 3 msb).
# So once you know which of those 3 bits give you the required program value, do the same with the next program value.
REVERSED_PROGRAM = list(reversed(PROGRAM))

# I actually had a bunch of code that only looked at the 10 least significant digits of A, since that's all the impacts the first output.
# But for brevity that can also be skipped, all we care about is the first output, and evaluating a computer's output is cheap.


def solve(reversed_program: list[int], depth: int = 0, a: int = 0):
    # Finds the viable 3 bits values that produce the output at memory_pos given the prefix of a.
    if depth == len(reversed_program):
        # We've fully matched the program.
        return a
    for i in range(8):
        # By iterating in ascending order, we ensure that we explore the smallest value first (we start at the msb).
        new_a = (a << 3) + i
        if Computer(new_a, 0, 0, PROGRAM).run().output[0] == reversed_program[depth]:
            maybe_match = solve(reversed_program, depth + 1, new_a)
            if maybe_match:
                return maybe_match


A = solve(REVERSED_PROGRAM)
print(f"{A=}")

# Random notes below that I wont bother cleaning up
"""
Here's what my program is doing:

B = Last 3 bits of A
Flip the last bit of B
C = Shift A right B times (so up to 7 times!)
B = B XOR 5 (which is the same as the last 3 bits of A with the first bit flipped)
B = B XOR C
A = A shift right 3 times
<Output last 3 bits of B>
Repeat till A is zero.

Note:
1) On each iteration: B and C don't depend on their respective previous values! It just depends on A!
2) A can be shifted up to 7 times, after which only the final 3 bits matter. So the 10 least signficant bits determin the first output value


B (0) <- RegA(0) % 8  (2,4)
RegB (1) <- RegB (0) XOR 1 (1,1)  # Always flip last bit of B
RegC( A//2^B) <- RegA / 2^^RegB(1) (7,5)  # C = A // 2^^B
RegB(0) <- RegB(1) XOR 5()  (1,5)  # Always xor B with 5
B(^A) <- B (0) ^ C (A) (4,0) # B = NOT(C)  , but C == A//2^^B
A <- A // 2^^3 > (0,3) # A = A//8  (shift right 3 bits)
Output B (A//2^^B % 8) (5,5)
Jump to zero (repeat)
"""


"""
This code proves that Only the last 10 bits influence the output for a given tick (after which its rshifted 3x).
for a in trange(pow(2, 20)):
    if (
        Computer(a, 0, 0, PROGRAM).run().output[0]
        != Computer(a % 1024, 0, 0, PROGRAM).run().output[0]
    ):
        print(f"For some reason, F(A) != F(A%1024) for {a=}")
"""
