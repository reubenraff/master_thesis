import lxml
import xmltodict
import datasets
import pandas as pd
from datasets import Dataset

# Open the file and read the contents
with open('pubmed_1_copy.xml', 'r', encoding='utf-8') as file:
    my_xml = file.read()

# Use xmltodict to parse and convert
# the XML document
xml_dict = xmltodict.parse(my_xml)


df = pd.DataFrame(xml_dict, columns=xml_dict.keys())

#print(df)
#ordered_dict = df["rst"].iloc[0] #<class 'collections.OrderedDict'>
order_dict = df["rst"].iloc[0]
segments_list_of_dicts = order_dict["segment"]
xml_dataframe = pd.DataFrame.from_dict(segments_list_of_dicts, orient='columns')


selected_rows = xml_dataframe[~xml_dataframe.isnull().any(axis=1)]
selected_rows.sort_values(by=["@parent"])
first_row = selected_rows[selected_rows["@id"]=="31"]["#text"]

#print(type(selected_rows))
dataset = Dataset.from_pandas(selected_rows,split="train")

#print(dataset["@id"])
print(dataset["@parent"][2])

parent_for_2 = dataset[dataset["@parent"] == 2]

id = dataset[dataset["@id"] == 2]

text_of_parent_for_2 = dataset[dataset["@parent"] == 2]["#text"]

parent_of_desired_id = dataset[dataset["@parent"] == id]["#text"]

print(text_of_parent_for_2)

from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")


encoding = tokenizer(text_of_parent_for_2, parent_of_desired_id, padding = "max_length", truncation=True)


#print(parent_for_2["#text"])
#text for the id of parent of row
#text for the id of current row
#relname between them

"""
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
sentence_a = "this is a sentence"
sentence_b = "this is another sentence"
encoding = tokenizer(sentence_a, sentence_b, padding="max_length", truncation=True)
"""


#relname, sentence1, sentence2

""" TODO make tuples, relname, sentence1, sentence2
    or tsv? then feed them to biobert
"""

"""
with open("pubmed1_sent_pair.txt", "w+") as sink:
    for i, j in selected_rows.iterrows():
    #print(j.values) # each j is a series with text, id parent and relname
        print(j.values[0])
    #print(j.values[1])
        parent_text = selected_rows.loc[selected_rows["@parent"] == j.values[0], "#text"]
        child_text = selected_rows.loc[selected_rows["@id"] == j.values[0], "#text"]
        relname = selected_rows.loc[selected_rows["@id"] == j.values[0], "@relname"]
        stuff = ("\t".join(relname.values), "\t".join(parent_text.values), "\t".join(child_text))
        print(" ".join(stuff),file=sink)
#clean this up and add as three columns to subset dataframe -> to dataset
"""




"""
x = selected_rows.loc[selected_rows["@parent"] == "4", "#text"]
y = selected_rows.loc[selected_rows["@id"] == "4", "#text"]
z = selected_rows.loc[selected_rows["@id"] == "4", "@relname"]
print(x)
print(y)
print(z)


add these to a dictionary? then turn that dict to dataset
"""




linked_parent = selected_rows[selected_rows["@id"]=="1"]["@parent"]

"""
print(xml_dataframe)
for column in xml_dataframe:
    if "@parent" != "NaN":
        print(column)
"""

"""
print(xml_dataframe.iloc[2]["@id"])
print(xml_dataframe.iloc[2]["#text"])
print(xml_dataframe.iloc[2]["@parent"])
"""
