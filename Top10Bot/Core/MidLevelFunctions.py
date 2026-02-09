"""
We have Devided Our Working Functions into 3 Different Modules:
    
    Base Level Functions: these are Functions that may be Used in Different Routes
    and Scenarios, are Written in a Universal Using Manner
    
    Mid Level Functions: these are Functions that are Specified to a Specific Task
    and might Give Varried Returns Depending on their Task
    
    Navigation Functions: these are Functions that are Specified to a Task,
    Handle the Return Part of the Mid Level Functions and Return log, route, stage
"""

import BaseLevelFunctions as BLF
import GlobalVariables as GV
import Messages as MSG
import Formatting as FORM
import DFsSaveLoad as DFSL
from collections import Counter
from collections import defaultdict
from typing import Optional
from typing import Any, Dict, List, Tuple

def command_starting_program(log):
    if log == False:    
        return BLF.get_input_command_repeatedly_until_valid(GV.not_logged_in_route_codetoname_dict,\
                MSG.what_action_msg(), MSG.choose_an_action_msg(), " was Selected. ", MSG.invalid_input_msg())
    elif log == True:
        return BLF.get_input_command_repeatedly_until_valid(GV.logged_in_route_codetoname_dict, \
                        MSG.what_action_msg(), MSG.choose_an_action_msg(), " was Selected. ", MSG.invalid_input_msg())

def creating_profile_get_username():
    print("")
    username, exists = BLF.get_username_check_exists()
    if exists:
        print("")
        yes_no = BLF.get_input_command_repeatedly_until_valid(GV.yes_or_no_dict, \
                 f"A Profile Named {username} Exists, Do You Wish to Load this Profile? ",\
                 MSG.choose_an_action_msg(), "", MSG.invalid_input_msg())
        if yes_no == "Y":
            return username, "L"
        else:
            return username, "Z"
    else:
        return username, "N"

def loading_profile_get_username():
    print("")
    username, exists = BLF.get_username_check_exists()
    if not exists:
        yes_no = BLF.get_input_command_repeatedly_until_valid(GV.yes_or_no_dict, \
                 f"No Profile Named {username} Exists, Do You Wish to Create a Profile with this Name? ",\
                 MSG.choose_an_action_msg(), "", MSG.invalid_input_msg())
        if yes_no == "Y":
            return username, "N"
        else:
            return username, "Z"
    else:
        return username, "L"

def get_cal_from_user():
    print("")
    calcode = BLF.get_input_command_repeatedly_until_valid(GV.supported_calendars_codetoname, \
        "Choose a Calendar for Your Profile.", MSG.choose_an_action_msg(), " was Selected", MSG.invalid_input_msg())
    return calcode

def get_first_year():
    print("")
    while True:
        year = input("Enter the First Year of Your TOP10 Journey: ")
        try:
            year = int(year)%100
            print(f"You Have Chosen the year {year} as the First Year in Your Top10 Journey.\n")
            return year%100
        except:
            print(MSG.invalid_input_msg(), " The First Year Must be a Number. ")
        
def get_first_month(cal):
    while True:
        month = FORM.format_first_upper_rest_lower(input("Enter the First Month of Your Top10 Journey: "))
        try:
            month = int(month)
            if 0<month<=GV.month_count(GV.calendar_code_to_dict[cal]):
                month_horuf = GV.calendar_code_to_dict[cal]['NtM'][month]
                print("")
                print(f"{month_horuf} Has been Chosen as the First Month of Your Top10 Journey. ")
                return month
        except:
            month = FORM.format_first_upper_rest_lower(month)
            for item in GV.calendar_code_to_dict[cal]["MtN"].keys():
                if month == item:
                    print("")
                    print(f"{item} is Chosen as the First Month of Your Top10 Journey. ")
                    return GV.calendar_code_to_dict[cal]["MtN"][item]
        print(MSG.invalid_input_msg())
        print("")

def create_DFs_new_profile():
    DFSL.DFsSet()

def save_user_data_to_file():
    DFSL.SaveUserDataToFile()
    print("Your Profile Has been Saved.\n")
    
def load_user_data_to_DFs(name):
    DFSL.LoadUserDataToDFs(name)
    
def ask_if_want_to_save():
    save = BLF.get_input_command_repeatedly_until_valid(GV.yes_or_no_dict, "Do You Want to Save Changes to Your Profile? ", \
                                    MSG.choose_an_action_msg(), "", MSG.invalid_input_msg())
    if save == "Y":
        return True
    elif save == "N":
        return False
    
def get_monthly_entry():
    entry = FORM.strip_only_empty_or_whitespace_lines(BLF.read_multiline("Enter Your Entry Here:\n"))
    first_line = entry.split("\n")[0]
    is_monthly = FORM.check_if_is_monthly_entry(first_line, GV.CurrentUser.get_name(), GV.CurrentUser.get_cal_dict()["MtN"].keys())
    return is_monthly, entry

def get_monthly_check_lines_validity():
    correct, entry = get_monthly_entry()
    if correct:
        line_count = 0
        lines = entry.split("\n")[1:]
        for line in lines:
            if " - " in line:
                line_count+=1
            elif line == "":
                continue
            else:
                return False, entry
        if line_count == 10:
            return True, entry
        else:
            return False, entry
    else:
        return False, entry
    
def give_songs_with_IDs_raw(entry):
    mod_month_ID = BLF.calculate_month_ID_for_monthly_entry(entry)
    lines = entry.split("\n")
    lines = lines[1:]
    line_count = 0
    out_list = []
    for line in lines:
        if(line != ""):
            line_count += 1
            ID = FORM.pad_number(mod_month_ID * 100 + line_count, 7)
            ID = FORM.add_string_to_num(ID, "MNT")
            out_list.append((FORM.demojify(line), ID))
    if line_count == 10:
        return True, out_list
    else:
        print(MSG.invalid_input_msg())
        return False, out_list
    
def check_if_monthly_entry_exists_in_df(entry_tuple):
    song_list=[]
    ID_list = []
    for item in entry_tuple:
        song, song_ID = item
        song_list.append(song)
        ID_list.append(song_ID)
    tekrari_check = BLF.cross_check_list_with_list(ID_list, DFSL.give_me_list_from_DF(2, "EntryID"))
    if tekrari_check:
        rewrite = BLF.get_input_command_repeatedly_until_valid(GV.yes_or_no_dict, \
                "Entries for this Month and Year Already Exist in the DataBase.\nWould You Like to Write Over the Existing Data?\n ", \
                "Enter Choise here: ", " was Chosen.", \
                MSG.invalid_input_msg())
        if rewrite == "Y":
            return False
        else:
            return True
        return not tekrari_check
    else:
        return False
        
def get_monthly_entry_tuple_add_to_DF(entry_list_of_tuples):
    for item in entry_list_of_tuples:
        song_name, song_ID = item
        song_ID_code = FORM.take_ID_give_number(song_ID)
        first_month = GV.CurrentUser.get_first_month()
        song_line = BLF.map_entry_code_to_DFLine(song_ID_code, first_month)
        DFSL.update_cell(2, song_line, "SongFullName", song_name)
        DFSL.update_cell(2, song_line, "EntryID", song_ID)
        DFSL.update_cell(2, song_line, "SongID", "")
        
def get_award_entry():
    entry = FORM.strip_only_empty_or_whitespace_lines(BLF.read_multiline("Enter Your Entry Here:\n"))
    first_line = entry.split("\n")[0]
    is_song_award = FORM.check_if_is_song_award_entry_first_line(first_line, GV.CurrentUser.get_name())
    if is_song_award:
        return is_song_award, 'song', entry
    is_artist_award = FORM.check_if_is_artist_award_entry_first_line(first_line, GV.CurrentUser.get_name())
    if is_artist_award:
        return is_artist_award, "artist", entry
    else:
        return False, "none", entry

def get_award_check_lines_validity():
    is_award, entry_type, entry = get_award_entry()
    if len(entry.split("\n"))>1:
        first_line = entry.split("\n")[1]
        if is_award:
            if entry_type == "song":
                is_song_op = FORM.check_if_is_song_op_award(first_line)
                if is_song_op:
                    line_count = 0
                    lines = lines = entry.split("\n")[2:]
                    for line in lines:
                        if " - " in line:
                            line_count+=1
                        elif line == "":
                            continue
                        else:
                            return False, entry_type, entry
                    if line_count == 10:
                        return True, "song", entry
                    else:
                        return False, "song", entry
                else:
                    return False, "song", entry
            elif entry_type == "artist":
                split_entry = entry.split("\n")
                total_length = len(split_entry)
                count_lines = 0
                list_of_entries = []
                has_op = False
                has_mor = False
                has_new = False
                for line in split_entry:
                    is_artist_op = FORM.check_if_is_artist_op_award(line)
                    is_morricone = FORM.check_if_is_morricone_award(line)
                    is_newcomer = FORM.check_if_is_newcomer_award(line)
                    if is_artist_op:
                        if not has_op:
                            has_op = True
                            my_tuple = ("artist op", count_lines)
                            list_of_entries.append(my_tuple)
                        else:
                            print("Multiple Instances of One Award was Spotted.")
                            return False, "artist", entry
                    if is_morricone:
                        if not has_mor:
                            has_mor = True
                            my_tuple = ("morricone", count_lines)
                            list_of_entries.append(my_tuple)
                        else:
                            print("Multiple Instances of One Award was Spotted.")
                            return False, "artist", entry
                    if is_newcomer:
                        if not has_new:
                            has_new = True
                            my_tuple = ("newcomer", count_lines)
                            list_of_entries.append(my_tuple)
                        else:
                            print("Multiple Instances of One Award was Spotted.")
                            return False, "artist", entry
                    count_lines +=1
                if list_of_entries != []:
                    my_tuple = ("finish", total_length+1)
                    list_of_entries.append(my_tuple)
                    lines_num_list = []
                    for item in list_of_entries:
                        award, num = item
                        lines_num_list.append(num)
                        #print(lines_num_list)#???
                    for count in range(len(lines_num_list)):
                        award, num = list_of_entries[count]
                        if award == "artist op":
                            next_a, next_n = list_of_entries[count+1]
                            if num + 10 < next_n:
                                continue
                            else:
                                return False, "artist", entry
                        if award == "morricone":
                            next_a, next_n = list_of_entries[count+1]
                            if num + 1 < next_n:
                                continue
                            else:
                                return False, "artist", entry
                        if award == "newcomer":
                            next_a, next_n = list_of_entries[count+1]
                            if num + 1 < next_n:
                                continue
                            else:
                                return False, "artist", entry
                    return True, "artist", entry
                
                else:
                    return False, "not important", entry
            else:
                return False, "not important", entry
    else:
        return False, "not important", entry

def give_award_IDs(entry):
    entry = FORM.strip_only_empty_or_whitespace_lines(entry)
    entry = FORM.demojify_multilines(entry)
    entry_line_by_line = entry.split("\n")
    year = int(entry_line_by_line[0][-2:])
    year = BLF.calculate_modified_year(year)
    definition_line = entry_line_by_line[0]
    first_line = entry_line_by_line[1]
    is_song_award = FORM.check_if_is_song_op_award(first_line)
    is_artist_award = FORM.check_if_is_artist_award_entry_first_line(definition_line, GV.CurrentUser.get_name())
    award_with_ID_tuple_list = []
    if is_song_award:
        line_count = 0
        lines = lines = entry.split("\n")[2:]
        for line in lines:
            if line == "":
                continue
            if line_count == 0:#???
                ID = "SAW" + FORM.pad_number(year*100+line_count, 5)
                my_tuple = (line, ID)
                award_with_ID_tuple_list.append(my_tuple)
            line = FORM.demojify(line)
            line_count += 1
            ID = "SAW" + FORM.pad_number(year*100+line_count, 5)
            my_tuple = (line, ID)
            award_with_ID_tuple_list.append(my_tuple)
        return award_with_ID_tuple_list
    if is_artist_award:
        total_length = len(entry_line_by_line)
        count_lines = 0
        list_of_entries = []
        for line in entry_line_by_line:
            is_artist_op = FORM.check_if_is_artist_op_award(line)
            is_morricone = FORM.check_if_is_morricone_award(line)
            is_newcomer = FORM.check_if_is_newcomer_award(line)
            if is_artist_op:
                my_tuple = ("artist op", count_lines)
                list_of_entries.append(my_tuple)
            if is_morricone:
                my_tuple = ("morricone", count_lines)
                list_of_entries.append(my_tuple)
            if is_newcomer:
                my_tuple = ("newcomer", count_lines)
                list_of_entries.append(my_tuple)
            count_lines +=1
        my_tuple = ("finish", total_length+1)
        list_of_entries.append(my_tuple)
        for tup in list_of_entries:
            entry_type, line_start = tup
            if entry_type == "artist op":
                for counter in range(0,10):
                    if counter == 0:#???
                        ID = "AAW" + str(FORM.pad_number(year*100 + counter, 5))
                        line = entry_line_by_line[line_start+1]
                        my_tuple = (line, ID)
                        #print("my tuple is", my_tuple)#???
                        award_with_ID_tuple_list.append(my_tuple)
                    counter += 1
                    line_count = counter + line_start
                    line = entry_line_by_line[line_count]
                    ID = "AAW" + str(FORM.pad_number(year*100 + counter, 5))
                    my_tuple = (line, ID)
                    award_with_ID_tuple_list.append(my_tuple)
            elif entry_type == "morricone":
                line_count = 1 + line_start
                line = entry_line_by_line[line_count]
                ID = "AAW" + FORM.pad_number(year*100+11, 5) 
                my_tuple = (line, ID)
                award_with_ID_tuple_list.append(my_tuple)
            elif entry_type == "newcomer":
                line_count = 1 + line_start
                line = entry_line_by_line[line_count]
                ID = "AAW" + FORM.pad_number(year*100+12, 5) 
                my_tuple = (line, ID)
                award_with_ID_tuple_list.append(my_tuple)
        return award_with_ID_tuple_list
    
def check_if_award_entry_exists_in_df(entry_tuple):
    awardee_list=[]
    ID_list = []
    for item in entry_tuple:
        awardee, award_ID = item
        awardee_list.append(awardee)
        ID_list.append(award_ID)
    tekrari_check = BLF.cross_check_list_with_list(ID_list, DFSL.give_me_list_from_DF(3, "EntryID"))
    if tekrari_check:
        rewrite = BLF.get_input_command_repeatedly_until_valid(GV.yes_or_no_dict, \
                "Entries for Awards of this Year Already Exist in the DataBase.\n ", \
                "Would You Like to Write Over the Existing Data? ", " was Chosen.", \
                MSG.invalid_input_msg())
        if rewrite == "Y":
            return False
        else:
            return True
        return not tekrari_check
    else:
        return False    

def clear_DF4_DF5():
    GV.CurrentUser.set_DF(DFSL.clear_dataframe_values(GV.CurrentUser.get_DF(4)), 4)
    GV.CurrentUser.set_DF(DFSL.clear_dataframe_values(GV.CurrentUser.get_DF(5)), 5)
    
import pandas as pd
import numpy as np
from typing import Dict, List, Any

def group_songs_by_entry_match_count(num: int) -> Dict[int, List[str]]:
    df = GV.CurrentUser.get_DF(4)
    target_num_str = str(num).zfill(3) # Ensure the input number is a 3-digit string (e.g., 5 -> '005')
    result_dict: Dict[int, List[str]] = {}
    for index, row in df.iterrows():
        song_id = row['SongID']
        entry_ids_str = row['EntryIDs']
        match_counter = 0
        if pd.isna(entry_ids_str) or not isinstance(entry_ids_str, str):
            pass
        else:
            individual_ids = [e.strip() for e in entry_ids_str.split(',')]
            for entry_id in individual_ids:
                if isinstance(entry_id, str) and len(entry_id) >= 6:
                    try:
                        extracted_digits = entry_id[3:6]
                        if extracted_digits == target_num_str:
                            match_counter += 1
                    except Exception:
                        continue
        if match_counter not in result_dict:
            result_dict[match_counter] = [song_id]
        else:
            result_dict[match_counter].append(song_id)
    result_dict = BLF.cascade_filter_dictionary(result_dict)
    return result_dict

def group_artists_by_entry_count(year: int):
    """
    Hardcoded df5.
    Returns dictionary1 where:
      - key   = counter (how many EntryIDs in that row have mid-3-digits == year)
      - value = list of ArtistID values from rows with that counter
    """
    # --- hardcoded dataframe ---
    df5 = GV.CurrentUser.get_DF(5)

    dictionary1: dict[int, list[str]] = {}

    def is_nonempty(x) -> bool:
        if pd.isna(x):
            return False
        s = str(x).strip()
        return bool(s) and s.lower() != "nan"

    def parse_tokens(cell) -> list[str]:
        if not is_nonempty(cell):
            return []
        return [t.strip() for t in str(cell).split(",") if t.strip() and t.strip().lower() != "nan"]

    year = int(year)

    for _, row in df5.iterrows():
        counter = 0

        # Count matches in EntryIDs
        for token in parse_tokens(row.get("EntryIDs", None)):
            token = str(token).strip()
            if len(token) < 6:
                continue

            mid3 = token[3:6]  # the 3 digits after the first 3 chars
            if not mid3.isdigit():
                continue

            if int(mid3) == year:
                counter += 1

        # Add ArtistID to dictionary under that counter
        artist_id = row.get("ArtistID", None)
        if not is_nonempty(artist_id):
            continue

        artist_id_str = str(artist_id).strip()
        dictionary1.setdefault(counter, []).append(artist_id_str)

    return dictionary1



def group_artists_by_single_month_entries(year: int):
    df5 = GV.CurrentUser.get_DF(5)  # hardcoded
    result: dict[int, list[str]] = {}
    year = int(year)

    def is_nonempty(x) -> bool:
        if pd.isna(x):
            return False
        s = str(x).strip()
        return bool(s) and s.lower() != "nan"

    def parse_tokens(cell) -> list[str]:
        if not is_nonempty(cell):
            return []
        return [t.strip() for t in str(cell).split(",") if t.strip() and t.strip().lower() != "nan"]

    for _, row in df5.iterrows():
        # Count M values for tokens matching the year
        m_counts = Counter()

        for token in parse_tokens(row.get("EntryIDs", None)):
            token = str(token).strip()
            if len(token) < 8:   # need at least 3 prefix + 5 digits
                continue

            block5 = token[3:8]  # next 5 chars after the first 3
            if not block5.isdigit():
                continue

            y_str = block5[:3]   # first 3 digits
            m_str = block5[3:5]  # last 2 digits

            if int(y_str) != year:
                continue

            m_counts[m_str] += 1

        score = max(m_counts.values()) if m_counts else 0

        artist_id = row.get("ArtistID", None)
        if not is_nonempty(artist_id):
            continue
        result.setdefault(score, []).append(str(artist_id).strip())
    return result


def group_artists_by_unique_songs(year: int):
    df4 = GV.CurrentUser.get_DF(4)

    year = int(year)

    def is_nonempty(x) -> bool:
        if pd.isna(x):
            return False
        s = str(x).strip()
        return bool(s) and s.lower() != "nan"

    def split_csv(cell) -> list[str]:
        if not is_nonempty(cell):
            return []
        return [t.strip() for t in str(cell).split(",") if t.strip() and t.strip().lower() != "nan"]

    # ---- Step 1: collect unique ArtistIDs as dict1 keys ----
    dict1 = {}
    for cell in df4.get("ArtistIDs", pd.Series(dtype=object)):
        for artist_id in split_csv(cell):
            if artist_id not in dict1:
                dict1[artist_id] = []

    # ---- Step 2: for each artist_id, scan all rows and collect SongID where analysis is true ----
    # (Not massively changing structure; still follows your "for each key -> scan all rows" description)
    for artist_id in dict1.keys():
        for _, row in df4.iterrows():
            row_artist_ids = split_csv(row.get("ArtistIDs", None))
            if artist_id not in row_artist_ids:
                continue

            entry_cell = row.get("EntryIDs", None)

            # analysis TRUE if EntryIDs empty/NaN
            analysis_true = False

            # if not empty, analysis TRUE if ANY EntryID token has token[3:6] == year
            if not analysis_true:
                for token in split_csv(entry_cell):
                    token = str(token).strip()
                    if len(token) < 6:
                        continue
                    mid3 = token[3:6]
                    if mid3.isdigit() and int(mid3) == year:
                        analysis_true = True
                        break

            if analysis_true:
                song_id = row.get("SongID", None)
                if is_nonempty(song_id):
                    dict1[artist_id].append(str(song_id).strip())

    # ---- Step 3: build dict2 by grouping artists by number of songs collected ----
    dict2 = defaultdict(list)
    for artist_id, songs in dict1.items():
        dict2[len(songs)].append(artist_id)

    return dict(dict2)

def update_DF4_and_DF5_step8(year: int):
    df5 = GV.CurrentUser.get_DF(5)  # hardcoded

    entry_col = "EntryIDs"
    out_col = "TempAwardIDs"

    year = int(year)

    # ensure output column exists
    if out_col not in df5.columns:
        df5[out_col] = np.nan

    def is_nonempty(x) -> bool:
        if pd.isna(x):
            return False
        s = str(x).strip()
        return bool(s) and s.lower() != "nan"

    def split_csv(cell) -> list[str]:
        if not is_nonempty(cell):
            return []
        return [t.strip() for t in str(cell).split(",") if t.strip() and t.strip().lower() != "nan"]

    def append_csv(cell, new_val: str) -> str:
        new_val = str(new_val).strip()
        if not new_val:
            return "" if pd.isna(cell) else str(cell)

        if pd.isna(cell) or str(cell).strip() == "" or str(cell).strip().lower() == "nan":
            return new_val

        # you asked specifically: "if not empty add a comma before it"
        # (this version also avoids duplicates; remove the duplicate check if you truly want repeats)
        parts = [p.strip() for p in str(cell).split(",") if p.strip() and p.strip().lower() != "nan"]
        if new_val not in parts:
            parts.append(new_val)
        return ",".join(parts)

    # ---- compute per-row scores ----
    scores = pd.Series(0, index=df5.index, dtype=int)

    for idx, row in df5.iterrows():
        counter = 0
        for token in split_csv(row.get(entry_col, None)):
            token = str(token).strip()
            if len(token) < 6:
                continue
            mid3 = token[3:6]  # next three chars after first 3
            if not mid3.isdigit():
                continue
            if int(mid3) <= year:
                counter += 1
        scores.at[idx] = counter
    # ---- select rows with highest score ----
    max_score = int(scores.max()) if len(scores) else 0
    selected_idx = scores.index[scores == max_score].tolist()
    if len(selected_idx) > GV.MAX_OVERALL_AWARD_COUNT:
        return df5  # do nothing
    # ---- build ID using the max score ----
    award_id = f"AAO{year:03d}1{max_score:04d}"
    # ---- append award_id to TempAwardIDs for selected rows ----
    for idx in selected_idx:
        df5.at[idx, out_col] = append_csv(df5.at[idx, out_col], award_id)
    GV.CurrentUser.set_DF(df5, 5)
    return df5

def song_to_tag(line: str, month: int) -> int:
    df = GV.CurrentUser.get_DF(4)
    int2 = month // 100

    # ---- helpers ----
    def normalize_name(s: object) -> str:
        """Lowercase and remove all whitespace."""
        if s is None:
            return ""
        try:
            if pd.isna(s):
                return ""
        except Exception:
            pass
        return "".join(str(s).split()).lower()

    def split_tokens(cell: Optional[object]) -> List[str]:
        """Split comma-separated cell into stripped tokens."""
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    # --- Step 1: match SongFullName (case-insensitive, ignore spaces) ---
    target = normalize_name(line)
    matches = df.index[df["SongFullName"].apply(normalize_name) == target].tolist()
    if not matches:
        return 5

    row = df.loc[matches[0]]

    # --- Step 2: TempAwardIDs logic ---
    for tok in split_tokens(row.get("TempAwardIDs")):
        # skip first 3 chars, next 3 digits
        if len(tok) >= 6 and tok[3:6].isdigit():
            int1 = int(tok[3:6])
            if (int2 - int1) == 1:
                return -1

    # --- Step 3: OpAwardIDs / UnOpAwardIDs / EntryIDs ---
    # 3a) OpAwardIDs score
    op_scores = []
    for tok in split_tokens(row.get("OpAwardIDs")):
        # digits after first 3 chars (3 digits)
        if len(tok) >= 6 and tok[3:6].isdigit():
            intA = int(tok[3:6])
            if intA < int2:
                # last two digits are score
                if len(tok) >= 2 and tok[-2:].isdigit():
                    op_scores.append(int(tok[-2:]))

    op_score = min(op_scores) if op_scores else None

    # 3b) UnOpAwardIDs score
    unop_scores = []
    for tok in split_tokens(row.get("UnOpAwardIDs")):
        if len(tok) >= 6 and tok[3:6].isdigit():
            intA = int(tok[3:6])
            if intA < int2:
                # last one digit is score
                if tok[-1:].isdigit():
                    unop_scores.append(int(tok[-1:]))
    unop_score = min(unop_scores) if unop_scores else None
    # If the minimum of available (op_score, unop_score) is < 4, return it
    candidates = [s for s in [op_score, unop_score] if s is not None]
    if candidates:
        m = min(candidates)
        if m < 4:
            return m

    # 3c) EntryIDs final analysis
    for tok in split_tokens(row.get("EntryIDs")):
        # skip first 3 chars, next 5 digits
        if len(tok) >= 8 and tok[3:8].isdigit():
            intB = int(tok[3:8])
            if intB < month:
                return 4
    return 5

def function_to_view_song_tags():
    defult_month_code = GV.CurrentUser.get_probable_current_month()
    defult_month_code = BLF.calculate_modified_month_ID(defult_month_code)
    year = int(defult_month_code)//100
    month = int(defult_month_code)%100
    my_dict = GV.CurrentUser.get_cal_dict()
    cal_code = GV.CurrentUser.get_cal_code()
    defult_month_name = my_dict["NtM"][month]
    message = f"The Tags will be Given for the Month of {defult_month_name} of the year {FORM.pad_number(year%100, 2)}. Is that OK with You? "
    answer = BLF.get_input_command_repeatedly_until_valid(GV.yes_or_no_dict,\
    message, "Enter Response Here: ", " was Chosen", MSG.invalid_input_msg())
    if answer == "N":
        year = BLF.get_year()
        month = BLF.get_month(cal_code)
    code = BLF.calculate_modified_month_ID(year*100 + month)
    entry = BLF.read_multiline("Enter Songs to Get Corresponding Tags (Hit Enter Multiple Times to Finish): ")
    line_by_line = entry.split("\n")
    output = []
    """🆕🎖🤘🏻(🏆🥇🥈🥉)"""
    for line in line_by_line:
        if BLF.line_is_song(line):
            score = song_to_tag(line, code)
            emoji = GV.score_to_emoji_dict[score]
            new_line = emoji + line
            output.append(new_line)
    return "\n".join(tuple(output))
    

def print_leaderboard(top_n: int = 10) -> None:
    # --- Hardcoded dictionary (example; replace with yours) ---
    score_map = GV.rank_to_score_suggestion_dict
    # --- Hardcoded dataframes (examples; replace with yours) ---
    df4 = GV.CurrentUser.get_DF(4)
    df5 = GV.CurrentUser.get_DF(5)

    def split_tokens(cell: Any) -> List[str]:
        """Split comma-separated cell into trimmed tokens."""
        if cell is None:
            return []
        try:
            # handles pandas NaN
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    def score_from_entryids(cell: Any) -> int:
        """Sum mapped scores using last two chars of each token as the key."""
        total = 0
        for tok in split_tokens(cell):
            # Need at least 2 chars at the end to parse
            if len(tok) >= 2 and tok[-2:].isdigit():
                k = int(tok[-2:])
                total += score_map.get(k, 0)  # if key missing, add 0
        return total

    def compute_top(df: pd.DataFrame, name_col: str) -> List[Tuple[str, int]]:
        scored: List[Tuple[str, int]] = []
        for _, row in df.iterrows():
            name = row.get(name_col, "")
            score = score_from_entryids(row.get("EntryIDs"))
            scored.append((str(name), score))
        # sort by score desc, then name asc for stable ordering
        scored.sort(key=lambda x: (-x[1], x[0]))
        return scored[:top_n]

    # --- Print df4 results ---
    top_df4 = compute_top(df4, "SongFullName")
    print("Top Songs:")
    for rank, (name, score) in enumerate(top_df4, start=1):
        print(f"{rank:>2}. {name} -> {score: .3f}")
    print()

    # --- Print df5 results ---
    top_df5 = compute_top(df5, "ArtistName")
    print("Top Artists:")
    for rank, (name, score) in enumerate(top_df5, start=1):
        print(f"{rank:>2}. {name} -> {score: .3f}")

def build_song_op_awards_output(year: int) -> str:
    Name = GV.CurrentUser.get_name()
    df4 = GV.CurrentUser.get_DF(4)
    rank_to_emoji_dict = GV.rank_to_emoji_dict
    yearstr = FORM.pad_number(year, 2)
    output = f"#{Name}'s Awards for Songs in the Year {yearstr}\n\n"

    dictionary1: Dict[int, str] = {}

    # If caller passes 4-digit year (e.g., 2024), match against last two digits (24),
    # since your IDs store year in 2 digits after the first four characters.
    target_yy = year if year < 100 else (year % 100)

    def split_tokens(cell: Any) -> list[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    for _, row in df4.iterrows():
        song_name = str(row.get("SongFullName", ""))
        for token in split_tokens(row.get("OpAwardIDs")):
            # Need at least 6 chars to read token[4:6], and 2 chars for last two digits
            if len(token) < 6:
                continue

            yy = token[4:6]
            if not yy.isdigit():
                continue

            if int(yy) != target_yy:
                continue

            last2 = token[-2:]
            if not last2.isdigit():
                continue

            rank = int(last2)
            dictionary1[rank] = song_name  # map rank -> song

    if not dictionary1:
        output += f"No Opinionated Awards for Songs were Found for the year {yearstr}\n\n"
        return output

    output += f"Opinionated Award for the Song of the Year {yearstr}\n"
    if 0 in dictionary1:
        output += f"{rank_to_emoji_dict[0]}{dictionary1[0]}\n\n"
    else:
        # In case rank 0 is missing but others exist
        output += f"{rank_to_emoji_dict[0]}(not found)\n\n"

    output += f"Opinionated Top 10 Songs of the Year {yearstr}\n"
    for idx in range(1, 11):
        if idx in dictionary1:
            output += f"{rank_to_emoji_dict[idx]}{dictionary1[idx]}\n"
        else:
            # If a rank is missing, still keep the line for consistent formatting
            output += f"{rank_to_emoji_dict[idx]}(not found)\n"

    return output




def suggestions_top_songs(year: int) -> None:
    # --- hardcoded inputs (replace with your real ones) ---
    Name = GV.CurrentUser.get_name()

    rank_to_score_dict = GV.rank_to_score_suggestion_dict

    rank_to_emoji_dict = GV.rank_to_emoji_dict

    df4 = GV.CurrentUser.get_DF(4)

    #df5 = GV.CurrentUser.get_DF(5)
    target_yy = year if year < 100 else year % 100

    def split_tokens(cell: Any) -> List[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    def entry_year_yy(entry: str) -> int | None:
        # set aside first 4 chars, next 2 must be digits
        if len(entry) < 6:
            return None
        yy = entry[4:6]
        return int(yy) if yy.isdigit() else None

    def entry_rank(entry: str) -> int | None:
        # last two chars must be digits
        if len(entry) < 2:
            return None
        rr = entry[-2:]
        return int(rr) if rr.isdigit() else None

    # --- Phase 1: compute score per df4 row for the given year ---
    scored_rows: List[Tuple[int, int]] = []  # (row_index, score)

    for idx, row in df4.iterrows():
        score = 0
        for entry in split_tokens(row.get("EntryIDs")):
            yy = entry_year_yy(entry)
            if yy is None or yy != target_yy:
                continue

            rr = entry_rank(entry)
            if rr is None:
                continue

            score += rank_to_score_dict.get(rr, 0)

        scored_rows.append((idx, score))

    # Sort by score desc, then by song name asc (stable tie-break)
    scored_rows.sort(
        key=lambda t: (
            -t[1],
            str(df4.loc[t[0], "SongFullName"]) if t[0] in df4.index else ""
        )
    )

    top20 = scored_rows[:20]
    # --- Build output string ---
    output = ""
    output += f"Suggestions for {Name}'s Top 10 Songs of the year {FORM.pad_number(year, 2)}\n"

    top10 = top20[:10]
    for rank, (idx, score) in enumerate(top10, start=1):
        emoji = rank_to_emoji_dict.get(rank, "")
        song_name = str(df4.loc[idx, "SongFullName"])
        # Format requested: emoji + SongFullName
        output += f"{emoji}{song_name}\n"

    if len(top20) > 10:
        output += "\nOther Possible Nominees: \n"
        for idx, score in top20[10:]:
            song_name = str(df4.loc[idx, "SongFullName"])
            output += f"{song_name}\n"

    return output

def suggestions_top_artists(year: int) -> str:
    # --- hardcoded inputs (replace with your real ones) ---
    Name = GV.CurrentUser.get_name()
    rank_to_score_dict = GV.rank_to_score_suggestion_dict
    rank_to_emoji_dict = GV.rank_to_emoji_dict
    df5 = GV.CurrentUser.get_DF(5)
    # If caller passes 4-digit year (e.g., 2024), match against the last two digits (24).
    target_yy = year if year < 100 else (year % 100)
    def split_tokens(cell: Any) -> List[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    def entry_year_yy(entry: str) -> int | None:
        # set aside first 4 chars, next 2 must be digits
        if len(entry) < 6:
            return None
        yy = entry[4:6]
        return int(yy) if yy.isdigit() else None

    def entry_rank(entry: str) -> int | None:
        # last two chars must be digits
        if len(entry) < 2:
            return None
        rr = entry[-2:]
        return int(rr) if rr.isdigit() else None

    # --- compute score per df5 row for the given year ---
    scored_rows: List[Tuple[int, int]] = []  # (row_index, score)

    for idx, row in df5.iterrows():
        score = 0
        for entry in split_tokens(row.get("EntryIDs")):
            yy = entry_year_yy(entry)
            if yy is None or yy != target_yy:
                continue

            rr = entry_rank(entry)
            if rr is None:
                continue

            score += rank_to_score_dict.get(rr, 0)

        scored_rows.append((idx, score))

    # Sort by score desc, then by artist name asc (tie-break)
    scored_rows.sort(
        key=lambda t: (
            -t[1],
            str(df5.loc[t[0], "ArtistName"]) if t[0] in df5.index else ""
        )
    )
    top20 = scored_rows[:20]
    # --- Build output string ---
    output = ""
    output += f"Suggestions for {Name}'s Top 10 Bands or Artists of the year {FORM.pad_number(year, 2)}\n"

    top10 = top20[:10]
    for rank, (idx, score) in enumerate(top10, start=1):
        emoji = rank_to_emoji_dict.get(rank, "")
        artist_name = str(df5.loc[idx, "ArtistName"])
        output += f"{emoji}{artist_name}\n"

    if len(top20) > 10:
        output += "\nOther Possible Nominees:\n\n"
        for idx, score in top20[10:]:
            artist_name = str(df5.loc[idx, "ArtistName"])
            output += f"{artist_name}\n"

    return output

def build_song_most_apps_output(year: int) -> str:
    rank_to_emoji_dict = GV.rank_to_emoji_dict
    yearstr = FORM.pad_number(year, 2)
    df4 = GV.CurrentUser.get_DF(4)
    # -----------------------------------------------
    output = ""
    output += f"Award for the Song with the Most Appearance in the Top 10 List in the Year {yearstr}\n"

    dictionary1: Dict[int, List[str]] = {}

    # Support both 2-digit and 4-digit inputs for year:
    target_yy = year if year < 100 else (year % 100)

    def split_tokens(cell: Any) -> List[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    for _, row in df4.iterrows():
        song_name = str(row.get("SongFullName", ""))
        for token in split_tokens(row.get("UnOpAwardIDs")):
            # Need at least 6 chars for token[4:6], and at least 3 chars for last 3 digits
            if len(token) < 7:
                continue
            yy = token[4:6]
            if not yy.isdigit() or int(yy) != target_yy:
                continue
            last3 = token[-3:]
            if not last3.isdigit():
                continue
            key = int(last3)
            dictionary1.setdefault(key, []).append(song_name)
    if not dictionary1:
        output += f"No Awards for Songs with the Most Appearance were Found for the year {yearstr}\n\n"
        return output
    # pick the largest key
    #key_set = set()
    key_list = []
    for item in dictionary1.keys():
        #key_set.add(item)
        key_list.append(item)
    #key_set.sort(reverse=True)
    key_list.sort(reverse=True)
    for key in key_list:
        # for each member in that key's list
        for song_name in dictionary1[key]:
            # emoji based on key % 10 (as requested)
            emoji = rank_to_emoji_dict.get(key % 10, "")
            output += f"{emoji}{song_name}\n"
        output += f"with {int(key // 10)} Appearances\n"
    output += "\n"
    return output


def build_song_overall_awards(year: int) -> str:
    # --- hardcoded inputs (replace with your real ones) ---
    rank_to_emoji_dict = GV.rank_to_emoji_dict
    yearstr = FORM.pad_number(year, 2)
    df4 = GV.CurrentUser.get_DF(4)
    # -----------------------------------------------

    output = ""
    output += f"Award for the Song with the Most Overall Appearance in the Top 10 List as of the End of the Year {yearstr}\n"

    dictionary1: Dict[int, List[str]] = {}

    # Support both 2-digit (24) and 4-digit (2024) year input
    target_yy = year if year < 100 else (year % 100)

    def split_tokens(cell: Any) -> List[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    for _, row in df4.iterrows():
        song_name = str(row.get("SongFullName", ""))
        for token in split_tokens(row.get("TempAwardIDs")):
            # Need at least 6 chars for token[4:6], and at least 4 digits for last4
            if len(token) < 8:
                continue

            yy = token[4:6]
            if not yy.isdigit() or int(yy) != target_yy:
                continue

            last4 = token[-4:]
            if not last4.isdigit():
                continue

            key = int(last4)
            dictionary1.setdefault(key, []).append(song_name)

    if not dictionary1:
        output += f"No Awards for Songs with the Most Appearance were Found for the year {yearstr}\n\n"
        return output

    # Sort keys in decreasing order and print groups
    trophy = rank_to_emoji_dict.get(-1, "")
    for key in sorted(dictionary1.keys(), reverse=True):
        for member in dictionary1[key]:
            output += f"{trophy}{member}\n"
        output += f"with {int(key)} Appearances\n"

    output += "\n"
    return output


def build_artist_op_awards(year: int) -> str:
    # --- Hardcoded inputs (replace with your real ones) ---
    Name = GV.CurrentUser.get_name()
    rank_to_emoji_dict = GV.rank_to_emoji_dict
    yearstr = FORM.pad_number(year, 2)
    df5 = GV.CurrentUser.get_DF(5)
    # -----------------------------------------------

    # output starts empty, then we add the header
    output = ""
    output += f"#{Name}'s Awards for Bands and Artists in the Year {yearstr}\n\n"

    dictionary1: Dict[int, str] = {}

    # Support both 2-digit and 4-digit year input:
    target_yy = year if year < 100 else (year % 100)

    def split_tokens(cell: Any) -> list[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    for _, row in df5.iterrows():
        artist_name = str(row.get("ArtistName", ""))
        for token in split_tokens(row.get("OpAwardIDs")):
            if len(token) < 6:
                continue

            yy = token[4:6]
            if not yy.isdigit() or int(yy) != target_yy:
                continue

            last2 = token[-2:]
            if not last2.isdigit():
                continue

            rank = int(last2)
            dictionary1[rank] = artist_name  # rank -> artist

    if not dictionary1:
        output += f"No Opinionated Awards for Songs were Found for the year {yearstr}\n\n"
        return output

    output += f"Opinionated Award for the Band or Artist of the Year {yearstr}\n"
    if 0 in dictionary1:
        output += f"{rank_to_emoji_dict[0]}{dictionary1[0]}\n\n"
    else:
        output += f"{rank_to_emoji_dict[0]}(not found)\n\n"

    output += f"Opinionated Top 10 Bands and Artists of the Year {yearstr}\n"
    for idx in range(1, 11):
        if idx in dictionary1:
            output += f"{rank_to_emoji_dict[idx]}{dictionary1[idx]}\n"
        else:
            output += f"{rank_to_emoji_dict[idx]}(not found)\n"

    return output

def build_unop_artist_awards(year: int) -> str:
    # --- Hardcoded inputs (replace with your real ones) ---
    Name = GV.CurrentUser.get_name()
    rank_to_emoji_dict = GV.rank_to_emoji_dict
    yearstr = FORM.pad_number(year, 2)
    df5 = GV.CurrentUser.get_DF(5)
    # -----------------------------------------------

    output = ""  # starts empty (as requested)

    # Three category dictionaries: key -> [artist names...]
    dictionary1: Dict[int, List[str]] = {}
    dictionary2: Dict[int, List[str]] = {}
    dictionary3: Dict[int, List[str]] = {}

    # Support both 2-digit and 4-digit year input:
    target_yy = year if year < 100 else (year % 100)

    def split_tokens(cell: Any) -> List[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    def add_to_dict(d: Dict[int, List[str]], k: int, name: str) -> None:
        if k in d:
            d[k].append(name)
        else:
            d[k] = [name]

    # --- Build dictionary1/2/3 from df5.UnOpAwardIDs ---
    for _, row in df5.iterrows():
        artist_name = str(row.get("ArtistName", ""))

        for token in split_tokens(row.get("UnOpAwardIDs")):
            # Need at least:
            # - positions [4:6] for yy
            # - index 6 for category (7th character)
            # - last 3 for key
            if len(token) < 10:
                continue

            yy = token[4:6]
            if not yy.isdigit() or int(yy) != target_yy:
                continue

            category = token[6]  # 7th character
            last3 = token[-3:]
            if not last3.isdigit():
                continue
            key = int(last3)

            if category == "1":
                add_to_dict(dictionary1, key, artist_name)
            elif category == "2":
                add_to_dict(dictionary2, key, artist_name)
            elif category == "3":
                add_to_dict(dictionary3, key, artist_name)
            # else: ignore unknown category

    # If all three are empty
    if not dictionary1 and not dictionary2 and not dictionary3:
        output += f"No UnOpinionated Awards for Bands and Artists were Found for the year {yearstr}\n\n"
        return output

    def append_ranked_block(d: Dict[int, List[str]], suffix_line: str) -> None:
        nonlocal output
        for k in sorted(d.keys(), reverse=True):
            for name in d[k]:
                emoji = rank_to_emoji_dict.get(k % 10, "")
                output += f"{emoji}{name}\n"
            output += suffix_line.format(value=int(k // 10))

    # --- dictionary1 section ---
    output += f"Award for the Band or Artist with the Most Appearance in the Top 10 List in the Year {yearstr}\n"
    if not dictionary1:
        output += f"No Data on Bands or Artists with the Most Appearance was Found for the Year {yearstr}\n\n"
    else:
        append_ranked_block(dictionary1, "with {value} Appearances\n")

    # --- dictionary2 section ---
    output += f"Award for the Band or Artist with the Most Number of Unique Songs in the Top 10 List in the Year {yearstr}\n"
    if not dictionary2:
        output += f"No Data on Bands or Artists with the Most Number of Unique Songs was Found for the Year {yearstr}\n\n"
    else:
        append_ranked_block(dictionary2, "with {value} Unique Songs\n")
    output += f"Award for the Band or Artist with the Most Number of Songs in a Single Month in the Top 10 List in the Year {yearstr}\n"
    # --- dictionary3 section ---
    if not dictionary3:
        output += f"No Data on Bands or Artists with the Most Number of Songs in a Single Month was Found for the Year {yearstr}\n\n"
    else:
        append_ranked_block(dictionary3, "with {value} Songs in a Single Month\n")

    output += "\n\n"
    return output

def build_artist_overall_awards(year: int) -> str:
    # --- Hardcoded inputs (replace with your real ones) ---
    Name = GV.CurrentUser.get_name()
    rank_to_emoji_dict = GV.rank_to_emoji_dict
    yearstr = FORM.pad_number(year, 2)
    df5 = GV.CurrentUser.get_DF(5)
    # -----------------------------------------------

    output = ""  # starts empty (as requested)

    dictionary1: Dict[int, List[str]] = {}
    dictionary2: Dict[int, List[str]] = {}

    # Support both 2-digit and 4-digit year input:
    target_yy = year if year < 100 else (year % 100)

    def split_tokens(cell: Any) -> List[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    def add_to_dict(d: Dict[int, List[str]], k: int, name: str) -> None:
        if k in d:
            d[k].append(name)
        else:
            d[k] = [name]

    # --- Build dictionaries from df5.TempAwardIDs ---
    for _, row in df5.iterrows():
        artist_name = str(row.get("ArtistName", ""))

        for token in split_tokens(row.get("TempAwardIDs")):
            # Need at least:
            # - positions [4:6] for yy
            # - index 6 for category (7th character)
            # - last 4 for key
            if len(token) < 10:
                continue

            yy = token[4:6]
            if not yy.isdigit() or int(yy) != target_yy:
                continue

            category = token[6]  # 7th character
            last4 = token[-4:]
            if not last4.isdigit():
                continue
            key = int(last4)

            if category == "1":
                add_to_dict(dictionary1, key, artist_name)
            elif category == "2":
                add_to_dict(dictionary2, key, artist_name)
            # else: ignore unknown category

    if not dictionary1 and not dictionary2:
        output += f"No Awards for Bands or Artists Overall Awards was Found for the year {yearstr}\n\n"
        return output

    trophy = rank_to_emoji_dict.get(-1, "")

    # --- dictionary1 section ---
    output += (
        f"Award for the Band or Artist with the Most Overall Appearance in the Top 10 List "
        f"as of the End of the Year {yearstr}"
    )
    output += "\n"
    if not dictionary1:
        output += "No Input Found in DataBase\n"
    else:
        for key in sorted(dictionary1.keys(), reverse=True):
            for member in dictionary1[key]:
                output += f"{trophy}{member}\n"
            output += f"with {int(key)} Appearances\n"
    output += "\n"

    # --- dictionary2 section ---
    output += (
        f"Award for the Band or Artist with the Most Overall Number of Unique Songs in the Top 10 List "
        f"as of the End of the Year {yearstr}"
    )
    output += "\n"
    if not dictionary2:
        output += "No Input Found in DataBase\n"
    else:
        for key in sorted(dictionary2.keys(), reverse=True):
            for member in dictionary2[key]:
                output += f"{trophy}{member}\n"
            output += f"with {int(key)} Unique Songs\n"
    output += "\n"

    return output




def build_honorary_opinionated_artist_awards(year: int) -> str:
    # --- Hardcoded inputs (replace with your real ones) ---
    Name = GV.CurrentUser.get_name()
    rank_to_emoji_dict = GV.rank_to_emoji_dict
    yearstr = FORM.pad_number(year, 2)
    df5 = GV.CurrentUser.get_DF(5)
    # -----------------------------------------------

    output = ""  # starts empty, as requested
    dictionary1: Dict[int, str] = {}

    # Support both 2-digit and 4-digit year input
    target_yy = year if year < 100 else (year % 100)

    def split_tokens(cell: Any) -> list[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return []
        return [t.strip() for t in s.split(",") if t.strip()]

    for _, row in df5.iterrows():
        artist_name = str(row.get("ArtistName", ""))
        for token in split_tokens(row.get("OpAwardIDs")):
            if len(token) < 6:
                continue

            yy = token[4:6]
            if not yy.isdigit() or int(yy) != target_yy:
                continue

            last2 = token[-2:]
            if not last2.isdigit():
                continue

            code = int(last2)
            if code in (11, 12):
                dictionary1[code] = artist_name

    if not dictionary1:
        output += f"No Honarary Opinionated Awards for Bands or Artists were Found for the year {yearstr}\n\n"
        return output

    # Morricone award (11)
    output += f"#MorriconeAward of the Year {yearstr} for Lifetime Achievements of a Band or Artist\n"
    if 11 in dictionary1:
        output += f"{rank_to_emoji_dict.get(11, '')}{dictionary1[11]}\n"
    else:
        output += "No Input Found in DataBase\n"
    output += "\n"

    # New-comer award (12)
    output += f"Award for the New-Comer Band or Artist of the Year {yearstr}\n"
    if 12 in dictionary1:
        output += f"{rank_to_emoji_dict.get(12, '')}{dictionary1[12]}\n"
    else:
        output += "No Input Found in DataBase\n"

    return output



def see_awards():
    year = BLF.get_year()
    yearstr = FORM.pad_number(year, 2)
    mod_year = BLF.calculate_modified_year(year)
    year_list = GV.CurrentUser.get_award_year_list()
    if mod_year not in year_list:
        print(f"There was No Awards Found for the year {yearstr}. This Might Happen for the Following Reasons:\
-You Haven't Entered any Entries for the year {yearstr} \
-You Haven't Entered the Opinionated Awards for the year {yearstr} \
-Your Tables Have not been Properly Updated Before Checking for Awards \
              ")
        return False
    else:
        print(build_song_op_awards_output(year))
        print(build_song_most_apps_output(year))
        print(build_song_overall_awards(year))
        MSG.press_enter()
        print(build_artist_op_awards(year))
        print(build_unop_artist_awards(year))
        print(build_artist_overall_awards(year))
        print(build_honorary_opinionated_artist_awards(year))
        
        #???
        return True



