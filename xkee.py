import random, time
import colorama, sys, os

if os.name == "nt":
    colorama.just_fix_windows_console()

result, i = [], {}
error_color = colorama.Fore.RED + colorama.Style.BRIGHT
dark_gray_color = colorama.Fore.BLACK + colorama.Style.BRIGHT

def is_hex(s):
    try:
        if len(s) > 2:
            return False
        int(s, 16)
        return True
    except ValueError:
        return False

def write(*argv):
    for arg in argv:
        result.append(bytes((arg,)))

def err(message, line=0, character=0):
    print(f"{error_color}Compilation Error: {message}{dark_gray_color} @ pos {line}:{character}{colorama.Style.RESET_ALL}")
    quit(1)



def i_tsp(request: bool, value=0x0, line=0):
    if not(request):
        err("TSP used as instruction!", line, 1)
    return int(time.time())%0x100

def i_rnd(request: bool, value=0x0, line=0):
    if not(request):
        err("RND used as instruction!", line, 1)
    return random.randrange(0x00, 0xff)

def i_lgd(request: bool, value=None, line=0):
    if request:
        err("LGD used as argument!", line, 5)
    elif value != None:
        err("Gave argument to LGD, when none are required.", line, 5)

    write(0x23, i["hx0"](True), i["hx1"](True))

def i_grd(request: bool, value=None, line=0):
    if request:
        err("GRD used as argument!", line, 5)
    elif value != None:
        err("Gave argument to GRD, when none are required.", line, 5)

    write(0x3f, i["hx0"](True), i["hx1"](True), i["hx2"](True), i["hx3"](True))

def i_add(request: bool, value=0x0, line=0):
    if request:
        err("ADD used as argument!", line, 5)
    write(0xe4, value)

def i_sub(request: bool, value=0x0, line=0):
    if request:
        err("SUB used as argument!", line, 5)
    write(0xe4, 0xff-value)

i = {
    "tsp": i_tsp,
    "rnd": i_rnd,
    "lgd": i_lgd,
    "grd": i_grd,
    "add": i_add,
    "sub": i_sub
}

values = []
def i_hx(request: bool, variable=0x0, value=0x0) -> hex:
    if request == False:
        values[variable] = value
    return values[variable]
def create_i_hx():
    for j in range(0,16):
        values.append(0x0)
        exec(f"""
def i_hx{hex(j)[2:]}(request: bool, value=0x0, line=0) -> hex:
    return i_hx(request, {hex(j)}, value)
""")
        i[f"hx{hex(j)[2:]}"] = locals()[f"i_hx{hex(j)[2:]}"]
create_i_hx()

def compile_instruction(instruction, line):
    length = len(instruction)
    if instruction[0] in i and length > 1 and is_hex(instruction[1]):
        i[instruction[0]](False, int("0x" + instruction[1], 0), line)
    elif length > 1:
        i[instruction[0]](False, i[instruction[1]](True, line=line), line)
    else:
        i[instruction[0]](False, None, line)

def read_xkee():
    with open(sys.argv[1]) as xkee:
        xkee_code = xkee.read()
    line = 0

    for instruction in xkee_code.split("\n"):
        line += 1

        if instruction == "" or instruction.startswith(";"):
            continue

        instruction = instruction.lower().split(";")[0].split(" ")
        compile_instruction(instruction, line)

if sys.argv[1].endswith(".xkee"):
    read_xkee()
    try:
        sys.argv[2]
        with open(sys.argv[2], "wb") as kee:
            for bytes in result:
                kee.write(bytes)
    except:
        with open(sys.argv[1].replace(".xkee",".kee"), "wb") as kee:
            for bytes in result:
                kee.write(bytes)
else:
    err("Not an XKEE file!")
