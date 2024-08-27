import random, time, colorama, sys, os
if os.name == "nt": colorama.just_fix_windows_console()

result, i = [], {}

def write(*argv):
    for arg in argv:
        result.append(bytes((arg,)))

def err(message):
    print(colorama.Fore.RED + colorama.Style.BRIGHT + "Compilation Error: " + message + colorama.Fore.BLACK + colorama.Style.BRIGHT + "\n-> Please make sure to get rid of garbage compilation leftovers before recompiling." + colorama.Style.RESET_ALL)
    quit()

def i_tsp(request: bool, value=0x0):
    if not(request): err("TSP used as instruction!")
    return int(time.time())%0x100
def i_rnd(request: bool, value=0x0):
    if not(request): err("RND used as instruction!")
    return random.randrange(0x00, 0xff)
def i_lgd(request: bool, value=0x0):
    if request: err("LGD used as argument!")
    write(0x23, i["hx0"](True), i["hx1"](True))
def i_grd(request: bool, value=0x0):
    if request: err("GRD used as argument!")
    write(0x3f, i["hx0"](True), i["hx1"](True), i["hx2"](True), i["hx3"](True))
def i_add(request: bool, value=0x0):
    if request: err("ADD used as argument!")
    write(0xe4, value)
def i_sub(request: bool, value=0x0):
    if request: err("SUB used as argument!")
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
def i_hx{hex(j)[2:]}(request: bool, value=0x0) -> hex:
    return i_hx(request, {hex(j)}, value)
""")
        i[f"hx{hex(j)[2:]}"] = locals()[f"i_hx{hex(j)[2:]}"]
create_i_hx()

with open(sys.argv[1], "r") as xkee:
    xkee_code = xkee.read()
    xkee.close()
    for instruction in xkee_code.split("\n"):
        if instruction == "" or instruction.startswith(";"): continue
        instruction = instruction.lower().split(" ")
        
        if len(instruction) > 1 and len(instruction[1]) == 2:
            i[instruction[0]](False, int("0x" + instruction[1], 0))
        elif len(instruction) > 1:
            i[instruction[0]](False, i[instruction[1]](True))
        else:
            i[instruction[0]](False)

if sys.argv[1].endswith(".xkee"):
    try:
        sys.argv[2]
        with open(sys.argv[2], "ab") as kee:
            for bytes in result:
                kee.write(bytes)
    except:
        with open(sys.argv[1].replace(".xkee",".kee"), "wb") as kee:
            for bytes in result:
                kee.write(bytes)
else:
    err("Not an XKEE file!")