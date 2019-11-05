#!/usr/bin/env python3

import argparse, re, sys

# the per instruction formats: 0, 1, or 2
FORMATS = {
    'add': 0, 'sub': 0, 'mult': 0, 'div': 0,
    'mod': 0, 'and': 0, 'or': 0, 'xor': 0,
    'beq': 0, 'bne': 0, 'blt': 0, 'ble': 0,
    'addi': 1, 'subi': 1, 'multi': 1, 'divi': 1,
    'modi': 1, 'shli': 1, 'shri': 1,
    'ld': 1, 'sd': 1, 'jalr': 1,
    'jal': 2, 'bz': 2, 'bnz': 2,
}

# the per instruction opcodes
OPCODES = {
    'add': (0, 0), 'sub': (0, 1), 'mult': (0, 2), 'div': (0, 3),
    'mod': (1, 0), 'and': (1, 1), 'or': (1,2), 'xor': (1,3),
    'beq': (2,0), 'bne': (2,1), 'blt': (2,2), 'ble': (2,3),
    'addi': 3, 'subi': 4, 'multi': 5, 'divi': 6,
    'modi': 7, 'shli': 8, 'shri': 9,
    'ld': 10, 'sd': 11, 'jalr': 12,
    'jal': 13, 'bz': 14, 'bnz': 15,
}

# the architecture register names
REGISTERS = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3,
}


def compile(source):
    """
    Compile an R12 source code

    :param source: the list of source code lines.
    :raises: nothing.

    :returns: the list of binary string instructions.
    """
    code = []

    # process all statements
    for i, line in enumerate(source, start=1):

        if line.strip() == '':
            continue

        # separate opcode from arguments
        op, args = line.split(maxsplit=1)

        if FORMATS.get(op) == 0:
            code.append(parse_format0(op, args.split(','), i))
        elif FORMATS.get(op) == 1:
            code.append(parse_format1(op, args.split(','), i))
        elif FORMATS.get(op) == 2:
            code.append(parse_format2(op, args.split(','), i))
        else:
            print(f"erreur ligne {i+1}: opcode invalide {op}", file=sys.stderr)

    return code


def parse_format0(op, args, line):
    """Parse the first instruction format: 'op rd, rs1, rs2'."""
    rd, rs1, rs2 = map(str.strip, map(str.upper, args))

    if not rd in REGISTERS:
        return f"erreur ligne {line}: registre invalide rd={rd}"
    if not rs1 in REGISTERS:
        return f"erreur ligne {line}: registre invalide rs1={rs1}"
    if not rs2 in REGISTERS:
        return f"erreur ligne {line}: registre invalide rs2={rs2}"

    # return binary instruction string
    return (
        f'{REGISTERS[rd]:02b}{REGISTERS[rs1]:02b}{REGISTERS[rs2]:02b}{OPCODES[op][1]:02b}'
        f'{OPCODES[op][0]:04b}'
    )


def parse_format1(op, args, line):
    """Parse the second instruction format: 'op rd, rs1, imm'."""
    rd, rs, imm = map(str.strip, map(str.upper, args))

    if not rd in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rd}", file=sys.stderr)
    if not rs in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rs}", file=sys.stderr)

    try:
        value = int(imm)
        if not 0 <= value <= 15:
            print(f"erreur ligne {line}: valeur invalide {value}", file=sys.stderr)

    except:
        print(f"erreur ligne {line}: valeur invalide {imm}", file=sys.stderr)

    # return binary instruction string
    return (
        f'{REGISTERS[rd]:02b}{REGISTERS[rs]:02b}{value:04b}{OPCODES[op]:04b}'
    )


def parse_format2(op, args, line):
    """Parse the third instruction format: 'op rd, imm'."""
    rd, imm = map(str.strip, map(str.upper, args))

    if not rd in REGISTERS:
        print(f"erreur ligne {line}: registre invalide {rd}", file=sys.stderr)

    try:
        value = int(imm)
        if not -32 <= value <= 31:
            print(f"erreur ligne {line}: valeur invalide {value}", file=sys.stderr)

    except:
        print(f"erreur ligne {line}: valeur invalide {imm}", file=sys.stderr)

    # return binary instruction string
    return (
        f'{REGISTERS[rd]:02b}{value:06b}{OPCODES[op]:04b}'
    )


if __name__ == '__main__':
    # define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    args = parser.parse_args()

    # read source file
    with open(args.source, 'r') as file:
        source = file.readlines()

    # compile source
    code = compile(source)
    print('\n'.join(code))
