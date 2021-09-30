import numpy as np
import pandas as pd
import itertools


import duplicates


NUM_INITIAL_SPACES = 2


def get_hansard_date(line_list: list):
   # f_is_blank_line = lambda x: not(len(x.replace(" ", "")))
   # first_non_blank_index = min([i for i, x in enumerate(line_list) if not f_is_blank_line(x)])
   # return pd.to_datetime(line_list[first_non_blank_index]).date()

   i = 0
   use_date = None
   max_line = 20

   while i < max_line and pd.isnull(use_date):
       try:
           use_date = pd.to_datetime(line_list[i]).date()
       except:
           0
       if pd.isnull(use_date):
           i += 1

   assert use_date is not None, line_list[:max_line]
   return use_date


def is_topic(line_str: str) -> bool:
   is_topic_bool_list = [
       line_str == line_str.upper(),  # all capital
       (len(line_str) and line_str[0] != " ")  # not empty AND does not start with a space
   ]
   return all(is_topic_bool_list)


def get_person_any(line_str: str) -> bool:
   get_person_2 = get_person(line_str=line_str, n=2)
   get_person_3 = get_person(line_str=line_str, n=3)

   is_2 = (get_person_2 is not None)
   is_3 = (get_person_3 is not None)

   assert not (is_2 and is_3)

   if is_2:
       return get_person_2
   elif is_3:
       return get_person_3
   else:
       return None


def get_person(line_str: str, n: int) -> bool:
   substr_list = line_str.split("-")
   initial_substr = substr_list[0]
   is_person_bool_list = [
       len(substr_list) >= 2,  # XXX-YYY
       (len(initial_substr) > n and initial_substr[0:n] == " " * n),  # starts with n blank spaces
       (len(initial_substr) > n and initial_substr[n] != " "),  # (n+1)th position is NOT blank
   ]
   if all(is_person_bool_list):
       return initial_substr[n:]
   else:
       return None


def get_topic_person_edges(topic_series: pd.Series,
                          line_list: list,
                          i: int,
                          num_initial_spaces: int,
                          ) -> (str, list):
   assert i < len(topic_series) - 1

   start_line = topic_series.index[i]
   end_line = topic_series.index[i + 1]

   topic = topic_series[start_line]
   person_list = [get_person_any(x) for x in line_list[start_line + 1:end_line]]
   person_list = [x for x in person_list if x is not None]

   return topic, person_list


def get_hansard_df(hansard_dict: dict) -> pd.DataFrame:
   edge_list = [
       [
           {"topic_original": topic, "person_original": person}
           for person in person_list
       ]
       for topic, person_list in hansard_dict.items()
   ]
   edge_list = list(itertools.chain.from_iterable(edge_list))

   hansard_df = pd.DataFrame(edge_list)
   return hansard_df


def get_hansard_edge_df(txt_str: str,
                       config_dict: dict = {}
                       ) -> pd.DataFrame:
   line_list = txt_str.split("\n")

   hansard_date = get_hansard_date(line_list=line_list)

   topic_dict = {i: x for i, x in enumerate(line_list) if is_topic(x)}
   topic_series = pd.Series(topic_dict).sort_index(ascending=True)

   num_initial_spaces = config_dict.get("num_initial_spaces", NUM_INITIAL_SPACES)

   edge_dict = {}
   for i in range(len(topic_series) - 1):
       topic, person_list = get_topic_person_edges(topic_series=topic_series,
                                                   line_list=line_list,
                                                   i=i,
                                                   num_initial_spaces=num_initial_spaces
                                                   )
       if len(person_list):
           edge_dict[topic] = person_list

   hansard_df = get_hansard_df(hansard_dict=edge_dict)
   hansard_df["date"] = hansard_date

   return hansard_df


def clean_hansard_edge_df(hansard_df: pd.DataFrame) -> pd.DataFrame:
   for col_original in [
       "topic_original",
       "person_original",
   ]:
       hansard_df = duplicates.add_clean_column(hansard_df=hansard_df, col_original=col_original)

   return hansard_df

