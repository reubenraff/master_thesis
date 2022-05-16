#!/usr/bin/env python
import argparse
import re


def main(args: argparse.Namespace) -> None:
    with open(args.rst_file,"r") as segments, open(args.output_file,"w+") as sink:
        contents = segments.read()
        segs = contents.split("\n")
        segmented = " ".join(segs)
        sequence_segments = re.split('\d{2}', segmented)
        cleaner_segments = " ".join(sequence_segments)
        no_span = cleaner_segments.replace("span", "")
        print(no_span,file=sink)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rst_file")
    parser.add_argument("output_file")
    main(parser.parse_args())
