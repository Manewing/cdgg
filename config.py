
# @class Config - todo
class Config(object):
    def __init__(self, cxx, inc_dirs, src_dirs,  extra_flags):
        self.cxx = cxx

        if type(inc_dirs) != list:
            raise TypeError("expected list of inc directories")
        self.inc_dirs = inc_dirs

        self.inc_flags = list()
        for inc_dir in inc_dirs:
            self.inc_flags.append("-I" + inc_dir)

        if type(src_dirs) != list:
            raise TypeError("expected list of src directories")
        self.src_dirs = src_dirs

        if type(extra_flags) != list:
            raise TypeError("expected list of extra flags")
        self.extra_flags = extra_flags

