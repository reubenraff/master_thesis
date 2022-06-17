#!/usr/bin/env python
import xmltodict
import datasets
from datasets import Dataset, concatenate_datasets
import glob
import pandas as pd
from functools import reduce


dataframe_list = []
for file in glob.glob("pubmed_xml/*.xml"):
    # Open the file and read the contents
    with open(file, 'r', encoding='utf-8') as file: #'pubmed_1_copy.xml'
        my_xml = file.read()

        # Use xmltodict to parse and conver the XML document
        xml_dict = xmltodict.parse(my_xml)
        df1 = pd.DataFrame(xml_dict, columns=xml_dict.keys())
        #<class 'collections.OrderedDict'>
        order_dict = df1["rst"].iloc[0]
        segments_list_of_dicts = order_dict["segment"]
        xml_dataframe = pd.DataFrame.from_dict(segments_list_of_dicts, orient='columns')
        selected_df = xml_dataframe[~xml_dataframe.isnull().any(axis=1)]
        # Sort by date
        selected_df.sort_values(by='@id',ascending=True)
        df_formatted = selected_df.assign(parent_text=selected_df["#text"].shift(1))

        df_formatted["parent_text"].fillna(value="Introduction",inplace=True) #fillna parent

        #dataframe_list.append(df_formatted)
        dataframe_list.append(df_formatted)


all_pubmed_df = pd.concat(dataframe_list)

dataset = Dataset.from_pandas(all_pubmed_df,split="train")
dataset = dataset.rename_column("@parent", "parent")
dataset = dataset.rename_column("#text", "text")
dataset = dataset.rename_column("@id", "id")
dataset = dataset.rename_column("@relname", "relname")
print(dataset)
