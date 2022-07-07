import nltk
from nltk.tree import *
import pandas as pd




tree_dict = {}
rel_list = []
text_list = []
with open("file1.lisp.name","r") as source_tree,open("df_tree.tok","w") as sink:
    content = source_tree.read()

    tree = Tree.fromstring(content)
    for thing in tree.subtrees():
        if isinstance(thing, nltk.tree.Tree):
            if thing.label() == "rel2par":
                rel_list.append(" ".join([i for i in thing.leaves()]))

            elif thing.label() == "text":
                text_list.append(" ".join([i for i in thing.leaves()]))

data_tuples = list(zip(rel_list,text_list))

df = pd.DataFrame(data_tuples, columns=["relation","text"])
df_formatted = df.assign(parent_text=df["text"].shift(1))
df_formatted["parent_text"].fillna(value=df["text"].iloc[0],inplace=True) #fillna parent

print(df_formatted.head(5))
