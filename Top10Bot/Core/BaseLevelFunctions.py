"""
We have Devided Our Working Functions into Different Modules:
    
    Base Level Functions: these are Functions that may be Used in Different Routes
    and Scenarios, are Written in a Universal Using Manner
    
    Mid Level Functions: these are Functions that are Specified to a Specific Task
    and might Give Varried Returns Depending on their Task
    
    Navigation Functions: these are Functions that are Specified to a Task,
    Handle the Return Part of the Mid Level Functions and Return log, route, stage
"""

import Messages as MSG
import Formatting as FORM
import GlobalVariables as GV
import pandas as pd
import numpy as np
from typing import Callable, Optional

def do_nothing_func():
    pass

def get_input_command_repeatedly_until_valid (valid_choices_dict, \
                                             welcome_msg, wanting_input_msg, \
                                             valid_choice_msg, invalid_choice_msg):
    print(welcome_msg)
    print("")
    while(True):
        MSG.print_message_showing_valid_inputs_using_dicts(valid_choices_dict)
        user_input = FORM.refine_user_input_to_single_capital_letter(input(wanting_input_msg))
        print("")
        if FORM.check_input_validity_in_list(user_input, valid_choices_dict.keys()):
            print(valid_choices_dict[user_input] + valid_choice_msg)
            return user_input
            break
        else:
            print("!!!" + invalid_choice_msg + "!!!")
            print("")
            
def get_username_check_exists():
    existing_profiles_list = GV.get_available_profile_names(GV.profile_directory_path_GC)
    #print(existing_profiles_list)#???
    username = FORM.remove_space_keep_first_part(FORM.format_first_upper_rest_lower(input("Enter UserName: ")))
    check = FORM.check_input_validity_in_list(username, existing_profiles_list)
    return username, check
    
def read_multiline(input_message, end_blanks = 2):
    """
    Read multi-line user input from the terminal.
    Stops when the user enters `end_blanks` consecutive blank lines.
    Blank lines inside the text are preserved (unless they contribute to the final terminator).
    """
    lines = []
    blank_streak = 0
    print(f"{input_message}")
    while True:
        line = input()
        if line == "":
            blank_streak += 1
            if blank_streak >= end_blanks:
                return "\n".join(lines)
            lines.append("")
        else:
            blank_streak = 0
            lines.append(line)

def calculate_modified_month_ID(month_ID):
    if month_ID >= GV.CurrentUser.get_first_month():
        return month_ID
    else:
        return 10000+month_ID

def calculate_modified_year(year):
    if year >= GV.CurrentUser.get_first_month()//100:
        return year
    else:
        return 100+year

def calculate_unmodified_month_ID(month_ID):
    if month_ID>9999:
        return month_ID-10000
    else:
        return month_ID
    
def calculate_month_ID_for_monthly_entry(entry):
    first_line = entry.split("\n")[0].strip()
    first_line_split = first_line.split(" ")
    year = int(first_line_split[-1])
    month_in_entry = FORM.format_first_upper_rest_lower(first_line_split[-3])
    cal_dict = GV.CurrentUser.get_cal_dict()["MtN"]
    for dict_month_name, dict_month_num in cal_dict.items():
        if month_in_entry == dict_month_name:
            month = dict_month_num
    output_month = year*100 + month
    output_month = calculate_modified_month_ID(output_month)
    return output_month

def cross_check_list_with_list(list1, list2):
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                return True
    return False

def map_entry_code_to_DFLine(entry_code, first_month):
    fm_month = first_month%100
    fm_year = first_month//100
    ent_line = entry_code%100
    ent_month = (entry_code%10000)//100
    ent_year = entry_code//10000
    first_year_lines = (13-fm_month)*10
    return ((ent_month-1)*10 + (ent_year-fm_year-1)*120 + first_year_lines + ent_line - 1)

def song_artists_give_artist_count_and_list(song_string: str) -> tuple[int, list[str]]:
    try:
        artist_block, _ = song_string.split(" - ", 1)
    except ValueError:
        artist_block = song_string
    all_artists = []
    if " Feat. " in artist_block:
        main_part, feat_part = artist_block.split(" Feat. ", 1)
        all_artists.append(main_part.strip())
        featured_artists_list = feat_part.split(',')
        for artist in featured_artists_list:
            all_artists.append(artist.strip())
    else:
        all_artists.append(artist_block.strip())
    final_artists = [artist for artist in all_artists if artist]
    return len(final_artists), final_artists


from typing import Dict, List, Any

def cascade_filter_dictionary(input_dict: Dict[int, List[Any]]) -> Dict[int, List[Any]]:
    MAX_LIST_SIZE = GV.MAX_AWARD_COUNT

    if not input_dict:
        return {}

    # 1. Sort keys in descending order: [(200, List_200), (100, List_100), (50, List_50)] for sample input
    sorted_items = sorted(input_dict.items(), key=lambda item: item[0], reverse=True)
    
    # We only care about the top 3 items
    top_items = sorted_items[:3]
    
    final_dict: Dict[int, List[Any]] = {}
    
    # --- Cascade Execution ---
    
    # 1. Check the highest key (Key 1)
    if not top_items:
        return {}
        
    key1, list1 = top_items[0]
    if len(list1) <= MAX_LIST_SIZE:
        final_dict[key1] = list1
    else:
        # If Key 1 fails, the entire process stops, and the result is empty/null
        return {}

    # 2. Check the second highest key (Key 2)
    if len(top_items) > 1:
        key2, list2 = top_items[1]
        if len(list2) <= MAX_LIST_SIZE:
            final_dict[key2] = list2
        else:
            # If Key 2 fails, we keep Key 1's result and stop (no further checks)
            return final_dict

    # 3. Check the third highest key (Key 3)
    if len(top_items) > 2:
        key3, list3 = top_items[2]
        if len(list3) <= MAX_LIST_SIZE:
            final_dict[key3] = list3
        else:
            # If Key 3 fails, we keep the results from Key 1 and Key 2 and stop
            return final_dict
            
    return final_dict


from typing import Dict, List, Any

#???
def transform_dict_to_id_keyed(
    input_dict: Dict[int, List[Any]], 
    year: int, 
    award_type: int, 
    suffix: str
) -> Dict[str, List[Any]]:
    """
    Transforms an input dictionary by creating a new ID for each key based on 
    its rank, year, award type, and suffix, and then uses this new ID as the key 
    in the output dictionary.

    Args:
        input_dict: Dictionary where keys are numbers (up to 3) and values are lists.
        year: An integer used to format a 3-digit string for the ID.
        award_type: An integer used to format a 1-digit string for the ID.
        suffix: A string prefix for the ID.

    Returns:
        A new dictionary where keys are the generated IDs (str) and values are 
        the original list values.
    """
    
    if not input_dict:
        return {}

    # 1. Sort the keys in descending order to determine rank
    # sorted_items will be [(highest_key, value), (next_key, value), ...]
    sorted_items = sorted(input_dict.items(), key=lambda item: item[0], reverse=True)
    
    output_dict: Dict[str, List[Any]] = {}
    
    # Prepare the fixed string components with required zero-padding
    # Format the year as a three-digit string (e.g., 2024 -> "024" or "2024" depending on context, 
    # using the instruction 'three digit string')
    # Note: If year is 2026, it will become "026" if f-string padding is used, 
    # but typically years > 999 are truncated or handled specifically. 
    # Based on standard formatting for numbers < 1000, we use ':03d'. 
    # For years like 2026, we will take the last three digits as a safe interpretation for a 3-digit format.
    
    # Safe handling for Year: Format to 3 digits, assuming context implies only the last 3 digits matter 
    # if the year is > 999, or zero-padding if it is < 100.
    year_str = f"{year % 1000:03d}" 
    
    # Format award_type as a one-digit string
    award_type_str = f"{award_type:01d}" 
    
    # 2. Iterate through the top items (max 3) to assign rank and build the ID
    for index, (key_num, value_list) in enumerate(sorted_items):
        # Rank is 1-based (index 0 -> rank 1)
        rank = index + 1
        
        # Format key_value as a two-digit string (e.g., 5 -> "05", 100 -> "00" or "00" if key > 99)
        # For keys > 99, the format will likely truncate or result in unexpected behavior 
        # based on the strict two-digit requirement. We will take the last two digits.
        key_str = f"{key_num % 100:02d}"
        
        # Format rank as a one-digit string
        rank_str = f"{rank:01d}"
        
        # Construct the final ID: suffix, year(3), award_type(1), key(2), rank(1)
        new_id = f"{suffix}{year_str}{award_type_str}{key_str}{rank_str}"
        
        # 3. Create the output dictionary entry
        output_dict[new_id] = value_list
        
        # Stop after processing the first 3 keys (if the input dict had more)
        if rank == 3:
            break
            
    return output_dict

# --- Example Usage Simulation ---
# Define inputs based on the requirements
test_year = 2026
test_award_type = 5
test_suffix = "ABC"

# Sample Input (testing 3 keys, with one being small to test key formatting)
test_input_dict = {
    105: ["SongA", "SongB"],  # Will be rank 1 (if highest key is 105)
    2: ["SongC"],             # Will be rank 3 (if it's the lowest)
    50: ["SongD", "SongE", "SongF"] # Will be rank 2
}




def update_df_from_map(id_to_ids_dict, df_no, check_col_name, put_col_name): 
    df = GV.CurrentUser.get_DF(df_no)  # <-- change this to wherever your df lives
    def norm(x):
        if pd.isna(x):
            return ""
        return str(x).strip()
    # Build a lookup: SongID -> list of row indices (handles duplicates)
    song_to_indices = {}
    for idx, songid in df[check_col_name].items():
        k = norm(songid)
        if k:
            song_to_indices.setdefault(k, []).append(idx)
    # Helper: append a value to a comma-separated cell (no duplicates)
    def append_csv(cell, new_val: str) -> str:
        new_val = norm(new_val)
        if not new_val:
            return cell if not pd.isna(cell) else ""
        if pd.isna(cell) or norm(cell) == "" or norm(cell).lower() == "nan":
            return new_val
        parts = [p.strip() for p in str(cell).split(",") if p.strip()]
        if new_val not in parts:
            parts.append(new_val)
        return ",".join(parts)
    for award_id, songid_list in (id_to_ids_dict or {}).items():
        award_id_str = norm(award_id)
        if not award_id_str:
            continue
        for songid in songid_list or []:
            songid_str = norm(songid)
            if not songid_str:
                continue
            for idx in song_to_indices.get(songid_str, []):
                df.at[idx, put_col_name] = append_csv(df.at[idx, put_col_name], award_id_str)
    GV.CurrentUser.set_DF(df, df_no)  # <-- change index if needed
    return df


def get_year():
    print("")
    while True:
        year = input("Enter Year: ")
        try:
            year = int(year)%100
            print(f"You Have Chosen the year {year}.\n")
            return year%100
        except:
            print(MSG.invalid_input_msg(), "Year Must be a Number. ")
            
def get_month(cal):
    while True:
        month = FORM.format_first_upper_rest_lower(input("Enter Month: "))
        try:
            month = int(month)
            if 0<month<=GV.month_count(GV.calendar_code_to_dict[cal]):
                month_horuf = GV.calendar_code_to_dict[cal]['NtM'][month]
                print("")
                print(f"{month_horuf} Has been Chosen. ")
                return month
        except:
            month = FORM.format_first_upper_rest_lower(month)
            for item in GV.calendar_code_to_dict[cal]["MtN"].keys():
                if month == item:
                    print("")
                    print(f"{item} is Chosen. ")
                    return GV.calendar_code_to_dict[cal]["MtN"][item]
        print(MSG.invalid_input_msg())
        print("")            

def clean_lines(
    text: str,
    *,
    drop_empty: bool = False,
    join_with: str = "\n",
) -> str:
    """
    Split text into lines, strip each line, optionally transform each line,
    optionally drop empty lines, then join and return.
    """
    lines = text.splitlines()  # handles \n, \r\n, \r without keeping line endings
    out = []
    for line in lines:
        line = line.strip()
        line = FORM.demojify(line)
        if drop_empty and line == "":
            continue
        out.append(line)
    return join_with.join(out)

def line_is_song(text):
    if " - " in text:
        return True
    else:
        return False


