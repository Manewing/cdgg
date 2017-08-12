import sys

TC_NC = "\033[0m"
TC_RE = "\033[31m"
TC_GR = "\033[32m"
TC_YE = "\033[33m"
TC_BL = "\033[34m"

def info(what):
    sys.stderr.write(TC_BL + "[INFO]: " + what + "\n" + TC_NC)

def warn(what):
    sys.stderr.write(TC_YE + "[WARN]: " + what + "\n" + TC_NC)

def error(what):
    sys.stderr.write(TC_RE + "[ERROR]: " + what + "\n" + TC_NC)
    sys.exit(-1)
