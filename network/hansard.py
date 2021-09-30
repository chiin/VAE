import numpy as np
import pandas as pd

import os

import person
import duplicates
import utils


MAX_I = 1172
PATH_BASE = "txt//NNN.txt"




def build_edge_df(target_year: int) -> pd.DataFrame:
   hansard_df_list = []

   for i in range(1, MAX_I + 1):
       path_i = PATH_BASE.replace("NNN", str(i))
       if os.path.isfile(path_i):
           #         try:
           txt_str = open(path_i, encoding="ISO-8859-1").read()

           line_list = txt_str.split("\n")

           hansard_date = utils.get_hansard_date(line_list=line_list)
           if hansard_date.year == target_year:
               hansard_df = utils.get_hansard_edge_df(txt_str=txt_str)

               assert len(hansard_df), i

               hansard_df["index"] = i
               hansard_df_list.append(hansard_df)

   all_hansard_df = pd.concat(hansard_df_list)

   all_hansard_df = duplicates.add_clean_column(hansard_df=all_hansard_df, col_original="person_original")

   all_person_list = sorted(set(all_hansard_df["person_clean"]))
   all_person_list = [x for x in all_person_list if not person.is_speech(x)]

   all_person_list = [x for x in all_person_list if person.is_person(x)]

   all_hansard_df = all_hansard_df[
       [x in all_person_list for x in all_hansard_df["person_clean"]]
   ]

   all_hansard_df = duplicates.add_clean_column(hansard_df=all_hansard_df, col_original="topic_original")

   return all_hansard_df


def get_node_dict(edge_df: pd.DataFrame,
                 node_column: str,
                 count_node_column: str,
                 restrict_count_node_list: list = []
                 ):
   assert node_column in edge_df.columns, (edge_df.columns, node_column)
   assert count_node_column in edge_df.columns, (edge_df.columns, count_node_column)

   node_dict = {}
   node_list = sorted(set(edge_df[node_column]))
   count_node_list = sorted(set(edge_df[count_node_column]))

   for node in node_list:
       use_count_node_list = sorted(set(edge_df[edge_df[node_column] == node][count_node_column]))
       if len(restrict_count_node_list):
           use_count_node_list = [x for x in use_count_node_list if x in restrict_count_node_list]
       if len(use_count_node_list):
           node_dict[node] = use_count_node_list

   return node_dict

