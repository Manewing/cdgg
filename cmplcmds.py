
import re
import json
import subprocess

import log

class CompileCommand(object):
    def __init__(self, sourcefile, cmplstr, header):
        self.sourcefile = sourcefile

        self.arglist= re.sub("[ ]+", " ", cmplstr).split(" ")

        if not self.arglist[-4] == "-o":
            raise ValueError("uncompatible compile command")

        self.arglist[-4] = "-H"
        self.arglist[-2] = "-MM"

        if header == False:
            self.arglist[-3] = ""
        else:
            self.arglist = self.arglist[:-2]
            self.arglist[:-2] = sourcefile

    def execute(self):
        try:
            ret = subprocess.check_output(self.arglist, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError, OSError:
            log.error("call failed: " + str(self.arglist))
        ret = re.sub("\033\[[0-9]+m", "", ret)
        return ret

class CompileCommandsReader(object):
    def __init__(self, filename):
        try:
            with open(filename, "r") as f:
                self.data = json.load(f)
        except IOError as e:
            log.error("while reading compile commands: " + e)

    def get_commands(self, src_dir):
        cmplcmds = list()

        for elem in self.data:
            if src_dir in elem["file"]:
                cmplcmds.append(CompileCommand(elem["file"],
                            elem["command"], False))

        return cmplcmds
