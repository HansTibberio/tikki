
def left_shift(self, left_register, right_register):
    counter_register = self.registers.counter()

    self.instructions.append(
        f"MOV {right_register} {counter_register}")
    self.instructions.append(f"\n.lsh_loop\t; Left Shift Loop")
    self.instructions.append(f"CMP {counter_register} r0")
    self.instructions.append(f"BRH EQ .end_lsh")
    self.instructions.append(
        f"LSH {left_register} {left_register}")
    self.instructions.append(f"DEC {counter_register}")
    self.instructions.append(f"JMP .lsh_loop")
    self.instructions.append(f".end_lsh")


def right_shift(self, left_register, right_register):
    counter_register = self.registers.counter()

    self.instructions.append(
        f"MOV {right_register} {counter_register}")
    self.instructions.append(f"\n.rsh_loop\t; Right Shift Loop")
    self.instructions.append(f"CMP {counter_register} r0")
    self.instructions.append(f"BRH EQ .end_rsh")
    self.instructions.append(
        f"RSH {left_register} {left_register}")
    self.instructions.append(f"DEC {counter_register}")
    self.instructions.append(f"JMP .rsh_loop")
    self.instructions.append(f".end_rsh")


def or_function(self, left_register, right_register):
    self.instructions.append(
        f"NOR {left_register} {right_register} {left_register}")
    self.instructions.append(f"NOT {left_register} {left_register}")


def multiply_function(self, left_register, right_register):
    result_register = self.registers.temporal()
    counter_register = self.registers.counter()

    self.instructions.append(f"\nLDI {result_register} 0")
    self.instructions.append(f"CMP {left_register} r0")
    self.instructions.append(f"BRH EQ .end_mul")
    self.instructions.append(f"MOV {right_register} {counter_register}")
    self.instructions.append(f".mul_loop\t; Multiplication Loop")
    self.instructions.append(f"CMP {counter_register} r0")
    self.instructions.append(f"BRH EQ .end_mul")
    self.instructions.append(
        f"ADD {result_register} {left_register} {result_register}")
    self.instructions.append(f"DEC {counter_register}")
    self.instructions.append(f"JMP .mul_loop")
    self.instructions.append(f".end_mul")
    self.instructions.append(f"MOV {result_register} {left_register}")


def greater_than_or_equal_function(self, left_register, right_register):
    result_register = self.registers.flags()

    self.instructions.append(f"\nCMP {left_register} {right_register}")
    self.instructions.append(f"BRH GE .set_true")
    self.instructions.append(f"LDI {result_register} 0")
    self.instructions.append(f"JMP .end_ge")
    self.instructions.append(f".set_true")
    self.instructions.append(f"LDI {result_register} 1")
    self.instructions.append(f".end_ge")


def greater_than_function(self, left_register, right_register):
    result_register = self.registers.flags()

    self.instructions.append(f"CMP {left_register} {right_register}")
    self.instructions.append(f"BRH LT .set_false")
    self.instructions.append(f"BRH EQ .set_false")
    self.instructions.append(f"LDI {result_register} 1")
    self.instructions.append(f"JMP .end_gt")
    self.instructions.append(f".set_false")
    self.instructions.append(f"LDI {result_register} 0")
    self.instructions.append(f".end_gt")
