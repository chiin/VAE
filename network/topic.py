

EXCLUDE_TOPIC_LIST = [
   "AGAINST.",
   "NOES.",
   "REPORTS.",
   "DOCUMENTS.",

]


def is_topic(txt_str: str):
    return not (txt_str in EXCLUDE_TOPIC_LIST)

