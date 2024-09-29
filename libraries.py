
def cclls(self, left_register, right_register, tag):
    """Logical Left Shift"""
    counter_register = self.registers.counter()

    lsh_loop_tag = f".lsh_loop{tag}"
    lsh_end_tag = f".end_lsh{tag}"

    self.instructions.append(
        f"MOV {right_register} {counter_register}")
    self.instructions.append(f"\n{lsh_loop_tag}\t; Left Shift Loop")
    self.instructions.append(f"CMP {counter_register} r0")
    self.instructions.append(f"BRH EQ {lsh_end_tag}")
    self.instructions.append(
        f"LSH {left_register} {left_register}")
    self.instructions.append(f"DEC {counter_register}")
    self.instructions.append(f"JMP {lsh_loop_tag}")
    self.instructions.append(f"{lsh_end_tag}")


def cclrs(self, left_register, right_register, tag):
    """Logical Right Shift"""
    counter_register = self.registers.counter()

    rsh_loop_tag = f".rsh_loop{tag}"
    rsh_end_tag = f".end_rsh{tag}"

    self.instructions.append(
        f"MOV {right_register} {counter_register}")
    self.instructions.append(f"\n{rsh_loop_tag}\t; Right Shift Loop")
    self.instructions.append(f"CMP {counter_register} r0")
    self.instructions.append(f"BRH EQ {rsh_end_tag}")
    self.instructions.append(
        f"RSH {left_register} {left_register}")
    self.instructions.append(f"DEC {counter_register}")
    self.instructions.append(f"JMP {rsh_loop_tag}")
    self.instructions.append(f"{rsh_end_tag}")


def ccor(self, left_register, right_register):
    """Bitwise Or Operation"""
    self.instructions.append(
        f"NOR {left_register} {right_register} {left_register}")
    self.instructions.append(f"NOT {left_register} {left_register}")


def ccumul(self, left_register, right_register, tag):
    """Unsigned Multiplication"""
    result_register = self.registers.temporal()
    counter_register = self.registers.counter()

    mul_loop_tag = f".mul_loop_{tag}"
    end_mul_tag = f".end_mul_{tag}"

    self.instructions.append(f"\nLDI {result_register} 0")
    self.instructions.append(f"CMP {left_register} r0")
    self.instructions.append(f"BRH EQ {end_mul_tag}")
    self.instructions.append(f"MOV {right_register} {counter_register}")
    self.instructions.append(f"{mul_loop_tag}\t; Multiplication Loop")
    self.instructions.append(f"CMP {counter_register} r0")
    self.instructions.append(f"BRH EQ {end_mul_tag}")
    self.instructions.append(
        f"ADD {result_register} {left_register} {result_register}")
    self.instructions.append(f"DEC {counter_register}")
    self.instructions.append(f"JMP {mul_loop_tag}")
    self.instructions.append(f"{end_mul_tag}")
    self.instructions.append(f"MOV {result_register} {left_register}")


def ccuge(self, left_register, right_register, tag):
    """Comparator Greater or Equal than"""
    result_register = self.registers.flags()

    set_true_tag = f".set_true{tag}"
    end_ge_tag = f".end_ge{tag}"

    self.instructions.append(f"\nCMP {left_register} {right_register}")
    self.instructions.append(f"BRH GE {set_true_tag}")
    self.instructions.append(f"LDI {result_register} 0")
    self.instructions.append(f"JMP {end_ge_tag}")
    self.instructions.append(f"{set_true_tag}")
    self.instructions.append(f"LDI {result_register} 1")
    self.instructions.append(f"{end_ge_tag}")


def ccugt(self, left_register, right_register, tag):
    """Comparator Greater than"""
    result_register = self.registers.flags()

    set_false_tag = f".set_false{tag}"
    end_gt_tag = f".end_gt{tag}"

    self.instructions.append(f"CMP {left_register} {right_register}")
    self.instructions.append(f"BRH LT {set_false_tag}")
    self.instructions.append(f"BRH EQ {set_false_tag}")
    self.instructions.append(f"LDI {result_register} 1")
    self.instructions.append(f"JMP {end_gt_tag}")
    self.instructions.append(f"{set_false_tag}")
    self.instructions.append(f"LDI {result_register} 0")
    self.instructions.append(f"{end_gt_tag}")
