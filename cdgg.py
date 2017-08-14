#!/usr/bin/python

import os
import sys
import argparse

import log
import analize
import cmplcmds
import graphs

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description="TODO",
            epilog="TODO")
    parser.add_argument("-c", "--compile-commands", dest="cmpl_cmds", type=str,
            required=True, help="compile commands file to parse")
    parser.add_argument("-s", "--source", dest="src_dirs", action="append",
            type=str, default=[], required=True, help="source directory to analize")
    parser.add_argument("-g", "--graph", dest="graph", type=str, required=True,
            choices=["dot", "json"], help="sets graph type")
    args = parser.parse_args()

    # initialize graph
    if args.graph == "dot":
        graph = graphs.DotGraph()
    elif args.graph == "json":
        graph = graphs.JsonGraph()

    log.info("load: " + str(args.cmpl_cmds))
    compile_commands = cmplcmds.CompileCommandsReader(args.cmpl_cmds)
    log.info("found: " + str(len(compile_commands.data)) + " commands")

    log.info("analize: " + str(args.src_dirs))
    analizer = analize.Analizer(args.src_dirs)
    for src_dir in args.src_dirs:
        analizer.extend(compile_commands.get_commands(src_dir))
    analizer.process()

    log.info("DONE")

    # build graph
    for src_from in analizer.dependencies:
        graph.add_node(src_from)
        for src_to in analizer.dependencies[src_from]:
            graph.add_edge(src_from, src_to)

    graph.dump()
