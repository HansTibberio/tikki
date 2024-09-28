
class Registers():

    def __init__(self) -> None:
        self.registers = ['r8', 'r7', 'r6', 'r5', 'r4', 'r3', 'r2', 'r1']
        self.reg_counter = ['r9']
        self.temp_register = ['r10']
        self.flags_register = ['r15']

    def push(self, register):
        if register in self.registers:
            raise ValueError(f"Register {register} in the stack!.")
        self.registers.append(register)

    def pop(self):
        if len(self.registers) == 0:
            raise ValueError("No more registers available!.")
        return self.registers.pop()

    def counter(self):
        return self.reg_counter[0]

    def temporal(self):
        return self.temp_register[0]

    def flags(self):
        return self.flags_register[0]
