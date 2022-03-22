#!/usr/bin/env/python
from collections import Counter
import torch
from transformers import AutoModel, AutoTokenizer, RobertaTokenizer
import logging
import matplotlib.pyplot as plt

"""
Token indices sequence length is longer than the specified maximum sequence length for this model (517 > 512). Running this sequence through the model will result in indexing errors
"""

MAX_SEQUENCE_LENGTH = 512
##MODEL_NAME_OR_PATH = "markussagen/xlm-roberta-longformer-base-4096"

#tokenizer = AutoTokenizer.from_pretrained(
#    MODEL_NAME_OR_PATH,
#    max_length=MAX_SEQUENCE_LENGTH,
#    padding="max_length",
#    truncation=True,
#)

tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

with open("abnb_10k.doc", "r") as source, open("wordpiece_subsets.doc","w+") as sink:
    lengths = [] # 62650
    for line in source:
        input_ids = tokenizer(line)["input_ids"]
        logging.info("%d wordpieces found", len(input_ids))
        wordpieces = [tokenizer.decode([input_id]) for input_id in input_ids]

        #counts[len(wordpieces)]
        #counts = [len(wordpiece) for wordpiece in wordpieces]
        #average_line_length =
        #counts = Counter([len(wordpiece) for wordpiece in wordpieces])
        lengths.append(len(wordpieces)) # 62650

        print(len(wordpieces), wordpieces,file=sink)
        length_counts = Counter(lengths)

plt.bar(length_counts.keys(), length_counts.values())
plt.show()



"""
sentence = "Правда, от окон дуло."
input_ids = tokenizer(sentence)["input_ids"]
logging.info("%d wordpieces found", len(input_ids))
wordpieces = [tokenizer.decode([input_id]) for input_id in input_ids]
"""
