# Tested with transformers==3.3.1 from conda-forge.
import argparse
import transformers
import torch
import logging


def main(args):
# Testing tokenizer.
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        "bert-base-uncased"
    )
    with open(args.input_section, "r") as source, open(args.toked_doc,"w+") as sink:
        for line in source:
            input_ids = tokenizer(line,truncation=True)["input_ids"]
            logging.info("%d wordpieces found", len(input_ids))
            wordpieces = [tokenizer.decode([input_id]) for input_id in input_ids]
            print(" ".join(wordpieces),file=sink)


if "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_section")
    parser.add_argument("toked_doc")
    args = parser.parse_args()
    main(args)





"""
warning was better:
Token indices sequence length is longer than the specified maximum sequence length for this model (554 > 512)"""
