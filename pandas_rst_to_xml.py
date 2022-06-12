import lxml
import xmltodict
import xmltodict
import pprint
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


#text for the id of parent of row
#text for the id of current row
#relname between them

#relname, sentence1, sentence2

""" TODO make tuples, relname, sentence1, sentence2
    or tsv? then feed them to biobert
"""
with open("pubmed1_sent_pair.txt", "w+") as sink:
    for i, j in selected_rows.iterrows():
    #print(j.values) # each j is a series with text, id parent and relname
        print(j.values[0])
    #print(j.values[1])
        parent_text = selected_rows.loc[selected_rows["@parent"] == j.values[0], "#text"]
        child_text = selected_rows.loc[selected_rows["@id"] == j.values[0], "#text"]
        relname = selected_rows.loc[selected_rows["@id"] == j.values[0], "@relname"]
        stuff = (" ".join(relname.values), " ".join(parent_text.values), " ".join(child_text))
        print(stuff,file=sink)
#clean this up and add as three columns to subset dataframe -> to dataset

"""
x = selected_rows.loc[selected_rows["@parent"] == "4", "#text"]
y = selected_rows.loc[selected_rows["@id"] == "4", "#text"]
z = selected_rows.loc[selected_rows["@id"] == "4", "@relname"]
print(x)
print(y)
print(z)
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
