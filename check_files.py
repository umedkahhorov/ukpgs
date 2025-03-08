#!/usr/bin/env python3

import os, fnmatch, argparse

def common_prefix(strings):
    return os.path.commonprefix(strings)

def main():
    parser = argparse.ArgumentParser(description="List files matching a given pattern.")
    parser.add_argument("-d","--dir", default=".", help='Directory to search in (default: current directory)')
    parser.add_argument("-p","--pattern",required=True,help='File pattern to match (e.g., "kr0917_A3obs_s0*-1*")')

    args = parser.parse_args()

    directory = args.dir
    pattern = args.pattern

    matching_files = [f for f in os.listdir(directory) if fnmatch.fnmatch(f,pattern)]
    #print(directory,pattern,matching_files)

    #print ("matching files:")
    #for f in matching_files:
    #    print(f)

    prefix = common_prefix(matching_files)
    print (f"\nCommon part: {prefix}")
    for f in matching_files:
        print(f"-{f[len(prefix):]}")

    print (f"\nTotal matching files: {len(matching_files)}")

if __name__ == '__main__':
    main()
