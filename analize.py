import re
import os
import subprocess

import log


# @class Analysis - TODO
class Analize(object):
    def __init__(self, config, filepath):
        self.config = config
        self.filepath = filepath
        self.dependencies = set()

        self.__process()

    def __build_call(self):
        args = list()

        args.append(self.config.cxx)
        args.append("-M")
        args.extend(self.config.inc_flags)
        args.extend(self.config.extra_flags)
        args.append(self.filepath)

        return args

    def __process(self):
        args = self.__build_call()
        log.info("call: " + str(args))

        try:
            ret = subprocess.check_output(args)
        except OSError:
            log.error("call failed: " + str(args))

        # remove newline, tab and escape
        ret = ret.replace("\\", "").replace("\n", "").replace("\t", "")

        # remove prefix
        ptrn = re.compile("(.*\..*:)(.*)")
        mtch = re.match(ptrn, ret)

        path_list = mtch.group(2)
        path_list = path_list.split(" ")

        for path in path_list:
            dirname = os.path.dirname(path)
            if dirname in self.config.inc_dirs \
              or dirname in self.config.src_dirs:
                self.dependencies.add(path)

