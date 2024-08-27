# kee.py file.txt basic_encryption.kee en/de
import sys, os, numpy

instructions_left = True
decrypt = False

if sys.argv[3] == "de":
    decrypt = True

with open(sys.argv[1], "rb") as file:
    file_content = file.read()
    file.close()
# file = open(sys.argv[1], "wb")

with open(sys.argv[2], "rb") as key:
    key = key.read()
    key_instructions = []
    for instruction in key:
        key_instructions.append(instruction)

def modify_file(list: bool, value):
    global file_content
    new = []
    if list and not(decrypt):
        for i in range(0, len(file_content)):
            new.append((int(file_content[i]) + value[i]) % 0x100)
    elif list and decrypt:
        for i in range(0, len(file_content)):
            new.append((int(file_content[i]) - value[i]) % 0x100)
    elif not(list) and not(decrypt):
        for i in range(0, len(file_content)):
            new.append((int(file_content[i]) + value) % 0x100)
    elif not(list) and decrypt:
        for i in range(0, len(file_content)):
            new.append((int(file_content[i]) - value) % 0x100)
    file_content = bytearray(new)

def linear_gradient():
    # i fucking love math
    a, b = key_instructions[1], key_instructions[2]
    total_steps = len(file_content)

    steps_ab = int(round(total_steps))

    if steps_ab <= 0:
        steps_ab = 1

    gradient_ab = numpy.linspace(a, b, steps_ab, dtype=int)
    modify_file(True, gradient_ab)

def gradient():
    # i fucking love math
    a, b, c, d = key_instructions[1], key_instructions[2], key_instructions[3], key_instructions[4]
    total_steps = len(file_content)

    diff_ab = b - a
    diff_bc = c - b
    diff_cd = d - c
    total_diff = diff_ab + diff_bc + diff_cd

    if total_diff <= 0:
        total_diff = 1
    exact_steps_ab = total_steps * diff_ab / total_diff
    exact_steps_bc = total_steps * diff_bc / total_diff
    exact_steps_cd = total_steps * diff_cd / total_diff

    steps_ab = int(round(exact_steps_ab))
    steps_bc = int(round(exact_steps_bc))
    steps_cd = total_steps - steps_ab - steps_bc

    if steps_ab <= 0:
        steps_ab = 1
        steps_bc = max(0, total_steps - steps_ab - steps_cd)
    if steps_bc <= 0:
        steps_bc = 1
        steps_cd = max(0, total_steps - steps_ab - steps_bc)
    if steps_cd <= 0:
        steps_cd = 1
        steps_bc = max(0, total_steps - steps_ab - steps_cd)

    gradient_ab = numpy.linspace(a, b, steps_ab, endpoint=False, dtype=int)
    gradient_bc = numpy.linspace(b, c, steps_bc, endpoint=False, dtype=int)
    gradient_cd = numpy.linspace(c, d, steps_cd, dtype=int)

    full_gradient = numpy.concatenate((gradient_ab, gradient_bc, gradient_cd))
    modify_file(True, full_gradient)

def add():
    modify_file(False, key_instructions[1])

length = {
    0x23: 3,
    0x3f: 5,
    0xe4: 2
}
instructions = {
    0x23: linear_gradient,
    0x3f: gradient,
    0xe4: add
}

while instructions_left:
    instructions[key_instructions[0]]()
    for instruction in range(0,length[key_instructions[0]]):
        key_instructions.pop(0)
    if not(len(key_instructions) > 0):
        instructions_left = False

with open(sys.argv[1], "wb") as file:
    file.write(file_content)
    file.close()

file.close()