import re
import os

import log

class Analizer(object):
    DEPTH_PTRN = re.compile("([.]+) (.*)")

    def __init__(self, src_dirs):
        self.dependencies = dict()
        self.cmplcmds = list()

        if type(src_dirs) != list:
            raise TypeError("expected list of source directories")

        self.src_dirs = src_dirs

    def filter(self, filter_expr):
        pass

    def add(self, cmplcmd):
        self.cmplcmds.append(cmplcmd)

    def extend(self, cmplcmds):
        self.cmplcmds.extend(cmplcmds)

    def __is_source(self, src_file):
        for src_dir in self.src_dirs:
            if src_dir in src_file:
                return True
        return False

    def __add_dependency(self, src_from, src_to):
        if not src_from in self.dependencies:
            self.dependencies[src_from] = set([src_to])
        else:
            self.dependencies[src_from].add(src_to)

    def __process_result(self, src_file, result):
        result = result.split("\n")

        last_src = src_file
        for line in result:
            mtch = re.match(Analizer.DEPTH_PTRN, line)
            if mtch == None:
                continue

            # are we at "depth 0"?
            if len(mtch.group(1)) == 1:
                last_src = src_file

            # last source file was not in source directory
            # ignore following sources
            if last_src == None:
                continue

            if self.__is_source(mtch.group(2)):
                self.__add_dependency(last_src, mtch.group(2))
                last_src = mtch.group(2)
            else:
                last_src = None

    def process(self):
        for cmplcmd in self.cmplcmds:
            log.info("analizing: " + cmplcmd.sourcefile)

            result = cmplcmd.execute()
            self.__process_result(cmplcmd.sourcefile, result)

    def dump(self):
        for src_from in self.dependencies:
            print os.path.basename(src_from)
            for src_to in self.dependencies[src_from]:
                print "  -", os.path.basename(src_to)
