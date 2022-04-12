#!/usr/bin/env python
import argparse
import os
from typing import Any, str

def main(files: Any) -> Any:
    file_dir = os.listdir(args.input_dir)
    with open(args.output_file, 'w+') as sink:
    # Iterate through list
        for names in filenames:
        # Open each file in read mode
            with open(names,"r") as source:
                # read the data from file1 and
                # file2 and write it in file3
                print(source.read(),file=outfile)


if __main__():
    parser = ArgumentParser()
    parser.add_argument("input_dir", help="path to input directory")
    parser.add_argument("output_file",help="output file with combined docs")
    args = parser.parse_args()
    main(args)
