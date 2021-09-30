
MAX_SUBSTRINGS = 5


PERSON_INITIAL_STR_LIST = [
   "THE HON. ",
   "The HON. ",
   "The Hon. ",
   "The Hon ",
   "HON. ",
   "Hon. ",
   "Hon ",
   "Hon, ",
   "Dr. ",
   "Mr. ",

   "H.E. ",
   "H. E. ",

   "The ACTING ",
   "The ATTORNEY",
   "The Acting ATTORNEY",

   "The COLONIAL ",
   "The DIRECTOR ",
   "The HARBOUR MASTER",
   "The CHAIRMAN",
   "CHAIRMAN",

   "HIS EXCELLENCY",
   "His EXCELLENCY",
   "His Excellency",


   "CAPT. ",
   "CAPTAIN ",
   "Colonel ",
   "General ",

   "COLONIAL SECRETARY",
   "Honourable COLONIAL SECRETARY",


   "Mr. FRANCIS",
   "The CLERK OF COUNCILS",
   "The Director of Public Works",
   "DIRECTOR OF PUBLIC WORKS",
   "ACTING DIRECTOR OF PUBLIC WORKS",
   "ACTING DIRECTOR of PUBLIC WORKS",


]


UNOFFICIAL_MEMBER_LIST = [
   'HON. E. R. BELILIOS',
    'Hon. A. McCONACHIE',
    'Hon. C. P. CHATER',
    'Hon. HO KAI',
    'Hon. J. J. KESWICK',
    'Hon. T. H. WHITEHEAD',
    'Mr. J. J. Bell',
]



def is_speech(txt_str: str, max_substrings: int = MAX_SUBSTRINGS):
   substr_list = txt_str.split(" ")
   return len(substr_list) > max_substrings


def is_person(txt_str: str):
   is_person_bool_list = [
       txt_str.find(x) == 0
       for x in PERSON_INITIAL_STR_LIST
   ]
   return any(is_person_bool_list)


def get_official_unofficial_member_list(person_list: list):
   unofficial_member_list = [x for x in person_list if x in UNOFFICIAL_MEMBER_LIST]
   official_member_list = [x for x in person_list if x not in UNOFFICIAL_MEMBER_LIST]
   return {
       "official": official_member_list,
       "unofficial": unofficial_member_list
   }


