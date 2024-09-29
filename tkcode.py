
def header(file):
    file.write("#############################################\n")
    file.write("#                                           #\n")
    file.write("#   The Innovative Kitty Kompiler Interface #\n")
    file.write("#                2024                       #\n")
    file.write("#                                           #\n")
    file.write("#  This assembly program contains a variety #\n")
    file.write("#     of bugs, use it at your own risk.     #\n")
    file.write("#                                           #\n")
    file.write("#############################################\n\n")


def stater(file):
    file.write("JMP .main\n\n.end\nHLT\n\n.main\n")
