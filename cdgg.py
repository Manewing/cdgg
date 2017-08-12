#!/usr/bin/python

import os
import sys
import argparse

import log
import config
import analize
import graphs

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description="TODO",
            epilog="TODO")
    parser.add_argument("--cxx", dest="cxx", type=str, required=True,
            help="sets compiler to call")
    parser.add_argument("--graph", dest="graph", type=str, required=True,
            choices=["dot", "json"], help="sets graph type")
    parser.add_argument("--ext", dest="exts", type=str, default=[], action="append",
            help="add file extension to be parsed")
    parser.add_argument("--inc", dest="inc", type=str, default=[], action="append",
            help="add include directory")
    parser.add_argument("--src", dest="src", type=str, default=[], action="append",
            help="add source directory")
    args = parser.parse_args()

    # normalize directory names
    for l in range(0, len(args.inc)):
        args.inc[l] = os.path.dirname(args.inc[l])
    for l in range(0, len(args.src)):
        args.src[l] = os.path.dirname(args.src[l])

    # initialize configuration
    cfg = config.Config(args.cxx, args.inc, args.src, [])

    # initialize graph
    if args.graph == "dot":
        graph = graphs.DotGraph()
    elif args.graph == "json":
        graph = graphs.JsonGraph()

    # build list of all source file directories
    source_dirs = list()
    source_dirs.extend(args.inc)
    source_dirs.extend(args.src)

    # create list of a paths to all files with matching extensions
    path_list = list()
    for source_dir in source_dirs:
        content = os.listdir(source_dir)
        for filename in content:
            if os.path.splitext(filename)[1] in args.exts:
                path_list.append(os.path.join(source_dir, filename))


    log.info("analize: " + str(path_list))

    # analize all files
    analysis = list()
    for path in path_list:
        analysis.append(analize.Analize(cfg, path))

    log.info("DONE")

    # build graph
    for elem in analysis:
        graph.add_node(elem.filepath)
        for dep in elem.dependencies:
            graph.add_edge(elem.filepath, dep)

    graph.dump()
