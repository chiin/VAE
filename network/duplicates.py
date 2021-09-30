import numpy as np
import pandas as pd

import recordlinkage


ALL_REMOVE_DICT = {
   "person_original": [
       'The title of the Ordinance was amended so as to read',
       'Re',
   ],
   "topic_original": [
       "PRESENT:-",
       "MINUTES.",
       "PAPERS.",
       "ADJOURNMENT.",
       "AGAINST.",
       "NOES.",
       "REPORTS.",
       "DOCUMENTS.",
   ]
}


DUPLICATE_DICT_BY_COL_NAME = {
   "topic_original": {
       "THE SANITARY BOARD'S BY-LAWS.": "THE SANITARY BOARD BY-LAWS.",
       "THE SANITARY BY-LAWS.": "THE SANITARY BOARD BY-LAWS.",

       "THE APPROPRIATION BILL FOR 1896.": "THE APPROPRIATION BILL.",
       "THE POSSESSION OF DEADLY WEAPONS.": "THE POSSESSION OF FIRE ARMS.",

       "THE WATERWORKS ORDINANCE.": "THE WATER ORDINANCE.",

       "THE REPEAL OF ORDINANCES.": "THE REPEALS ORDINANCE.",
   },
   "person_original": {
       "Hon. A. MCCONACHIE": "Hon. A. McCONACHIE",

       "Dr. HO KAI": "Hon. HO KAI",
       "Hon HO KAI": "Hon. HO KAI",

       "Hon C. P. CHATER": "Hon. C. P. CHATER",
       "The HON. C. P. CHATER": "Hon. C. P. CHATER",

       "His EXCELLENCY": "HIS EXCELLENCY",
       "Hon. E. R. BELILIOS": "HON. E. R. BELILIOS",

       "The ACTING ATTORNEY": "The ATTORNEY GENERAL",
       "The ATTORNEY": "The ATTORNEY GENERAL",

       "The ACTING COLONIAL SECRETARY": "The COLONIAL SECRETARY",
       "The ACTING COLONIAL TREASURER": "The COLONIAL TREASURER",


   }
}


def build_replace_dict(str_list: list):
   if len(str_list) == 1:
       return {}
   else:
       assert np.all(np.diff(np.array([len(x) for x in str_list])) >= 0)  # check the lengths are non-decreasing

       use_str = str_list[0]
       replace_dict = {
           raw_str: use_str for raw_str in str_list
           if (raw_str.find(use_str) == 0 and raw_str != use_str)  # look for entries starting with use_str
       }

       new_str_list = [x for x in str_list if (x != use_str and x not in replace_dict.keys())]

       return {
           **replace_dict,
           **(build_replace_dict(str_list=new_str_list))
       }


def build_replace_dict_column(dupes_column: str,
                             hansard_df: pd.DataFrame):
   replace_dict_list = []

   remove_dict = {
       x: None for x in ALL_REMOVE_DICT[dupes_column]
   }
   replace_dict_list.append(remove_dict)

   unique_column_list = sorted(set(hansard_df[dupes_column].values))

   column_length_series = pd.Series({
       col: len(col)
       for col in unique_column_list
   }).sort_values(ascending=True)

   replace_dict_initial = build_replace_dict(column_length_series.index)
   replace_dict_list.append(replace_dict_initial)

   duplicates_dict = DUPLICATE_DICT_BY_COL_NAME.get(dupes_column, {})
   replace_dict_list.append(duplicates_dict)

   return replace_dict_list


def add_clean_column(hansard_df: pd.DataFrame,
                    col_original: str
                   ):

   col_clean = col_original.replace("original", "clean")
   replace_dict_list = build_replace_dict_column(dupes_column=col_original, hansard_df=hansard_df)

   new_hansard_df = hansard_df.copy()
   new_hansard_df[col_clean] = new_hansard_df[col_original]

   for replace_dict in replace_dict_list:
       new_hansard_df[col_clean] = [replace_dict.get(x, x) for x in new_hansard_df[col_clean]]

   new_hansard_df = new_hansard_df[[x is not None for x in new_hansard_df[col_clean]]]

   return new_hansard_df

