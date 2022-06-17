#!/usr/bin/env python
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


df1 = pd.DataFrame(xml_dict, columns=xml_dict.keys())

df2 = df1.copy(deep=True)
#<class 'collections.OrderedDict'>
order_dict = df1["rst"].iloc[0]
segments_list_of_dicts = order_dict["segment"]
xml_dataframe = pd.DataFrame.from_dict(segments_list_of_dicts, orient='columns')
copy_xml_dataframe = xml_dataframe.copy(deep=True)


selected_df1 = xml_dataframe[~xml_dataframe.isnull().any(axis=1)]

# Sort by date
selected_df1.sort_values(by='@id',ascending=True)
df2 =selected_df1.assign(parent_text=selected_df1["#text"].shift(1))
print(df2[["@relname","#text", "parent_text"]])




# Create a column comparing previous Adj Close with current Adj Close
#import numpy as np
#selected_df1['i'] = np.where(df['@relname #text'].shift(1) < df['@relname #text'],1,0)




"""
selected_df2 = xml_copy[~xml_copy.isnull().any(axis=1)]
required_cols = selected_rows.get(["@id","@parent","@relname","#text"])

#convert parent and id col values to int
required_cols["@parent"] = required_cols["@parent"].astype(int)
required_cols["@id"] = required_cols["@id"].astype(int)

required_cols.pivot(index="@id",columns="@parent",values="#text")
"""
