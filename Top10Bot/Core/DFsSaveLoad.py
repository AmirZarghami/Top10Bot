"""
Save and Load DFs
"""

import pandas as pd
import GlobalVariables as GV
import numpy as np
from typing import Tuple, List, Any
import BaseLevelFunctions as BLF
import re
from collections import defaultdict

def ensure_df45_schema():
    df4 = GV.CurrentUser.get_DF(4)
    df5 = GV.CurrentUser.get_DF(5)

    for col in ["SongFullName","SongID","EntryIDs","ArtistCount","Artists","ArtistIDs","OpAwardIDs","UnOpAwardIDs","TempAwardIDs","HighestAwardID"]:
        if col not in df4.columns:
            df4[col] = np.nan

    for col in ["ArtistName","ArtistID","SongIDs","EntryIDs","OpAwardIDs","UnOpAwardIDs","TempAwardIDs"]:
        if col not in df5.columns:
            df5[col] = np.nan

    GV.CurrentUser.set_DF(df4, 4)
    GV.CurrentUser.set_DF(df5, 5)




def create_first_DF(user):
    headers = GV.CSVFile_Headers_dict["RawUserInfo"]
    df1 = pd.DataFrame(columns=headers)
    row = {"UserName": user.Name, "FirstMonth": user.FM, "Version": user.V, "Calendar": user.Cal}
    df1.loc[len(df1)] = row
    return df1

def create_other_DFs():
    header1 = GV.CSVFile_Headers_dict["RawMonthlyEntries"]    
    header2 = GV.CSVFile_Headers_dict["RawAwardEntries"]
    header3 = GV.CSVFile_Headers_dict["SongList"]
    header4 = GV.CSVFile_Headers_dict["ArtistList"]
    df1 = pd.DataFrame(columns=header1)
    df2 = pd.DataFrame(columns=header2)
    df3 = pd.DataFrame(columns=header3)
    df4 = pd.DataFrame(columns=header4)
    return df1, df2, df3, df4
    
def DFsSet():
    user = GV.CurrentUser
    GV.CurrentUser.set_DF(create_first_DF(user), 1)
    count = 2
    for item in create_other_DFs():
        GV.CurrentUser.set_DF(item, count)
        count += 1

def TestSaveBeforeActualy():
    user = GV.CurrentUser
    df1 = user.DF1
    df2 = user.DF2
    df3 = user.DF3
    df4 = user.DF4
    df5 = user.DF5
    out_path = GV.profile_directory_path_GC / "TestFile.xlsx"
    # --- Write each dataframe to a different sheet ---
    try:
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            df1.to_excel(writer, sheet_name="RawUserInfo", index=False)
            df2.to_excel(writer, sheet_name="RawMonthlyEntries", index=False)
            df3.to_excel(writer, sheet_name="RawAwardEntries", index=False)
            df4.to_excel(writer, sheet_name="SongList", index=False)
            df5.to_excel(writer, sheet_name="ArtistList", index=False)
        print("Proceeding to Save Your Profile.\n")
        return True
    except:
        return False
    
def SaveUserDataToFile():
    if TestSaveBeforeActualy():
        user = GV.CurrentUser
        df1 = user.DF1
        df2 = user.DF2
        df3 = user.DF3
        df4 = user.DF4
        df5 = user.DF5
        out_path = GV.CurrentUser.get_file() #GV.CurrentUser.File
        try:
            with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
                df1.to_excel(writer, sheet_name="RawUserInfo", index=False)
                df2.to_excel(writer, sheet_name="RawMonthlyEntries", index=False)
                df3.to_excel(writer, sheet_name="RawAwardEntries", index=False)
                df4.to_excel(writer, sheet_name="SongList", index=False)
                df5.to_excel(writer, sheet_name="ArtistList", index=False)
            print(f"Data Has been Saved to: {out_path}\n")
        except:
            print("There was a Problem Saving Your Progress to Your Profile.\
In Order to Avoid Disrupting Your Existing Profile, Your Progress will Not be Saved at this Moment.\n")
    else:
        print("There was a Problem Saving Your Progress to Your Profile.\
In Order to Avoid Disrupting Your Existing Profile, Your Progress will Not be Saved at this Moment.\n")
    
    
def LoadUserDataToDFs(name):
    GV.CurrentUser.load_DFs_from_name()
    
def SetBasicUserValuesFromDF1():
    GV.CurrentUser.set_name(GV.CurrentUser.DF1.iloc[0, 0])
    GV.CurrentUser.set_first_month(GV.CurrentUser.DF1.iloc[0, 1])
    GV.CurrentUser.set_version(GV.CurrentUser.DF1.iloc[0, 2])
    GV.CurrentUser.set_cal(GV.CurrentUser.DF1.iloc[0, 3])
    #print("setting basic values.")
    #print(f"name is {GV.CurrentUser.get_name()} and ")#???


def give_me_list_from_DF(DF_no, DF_header):
    df = GV.CurrentUser.get_DF(DF_no)
    return list(df[DF_header])

def update_cell(df_no, row_num, column_name, value):
    df = GV.CurrentUser.get_DF(df_no)
    #GV.CurrentUser.set_DF(df, df_no)
    if 13000 >= len(df):
        missing_rows = 13000 + 1 - len(df)
        df = pd.concat([df, pd.DataFrame([{c: pd.NA for c in df.columns}] * missing_rows)], ignore_index=True)
    df.at[row_num, column_name] = value
    GV.CurrentUser.set_DF(df, df_no)



def assign_sequential_IDs(df_no, name_col, ID_col, start_id):
    df = GV.CurrentUser.get_DF(df_no)

    id_map = {}

    def get_next_id(current_id_str):
        prefix = current_id_str[:3]              # e.g., 'SNG'
        number = int(current_id_str[3:])         # e.g., 1
        return f"{prefix}{number + 1:04d}"

    def norm_key(x):
        # Handle non-strings safely
        s = str(x)
        # trim + collapse runs of whitespace to one space + lowercase
        s = re.sub(r"\s+", " ", s).strip().lower()
        return s

    current_id_str = start_id

    if ID_col not in df.columns:
        df[ID_col] = np.nan

    for index, value in df[name_col].items():
        if pd.isna(value):
            continue

        key = norm_key(value)

        if key not in id_map:
            id_map[key] = current_id_str
            df.loc[index, ID_col] = current_id_str
            current_id_str = get_next_id(current_id_str)
        else:
            df.loc[index, ID_col] = id_map[key]

    return df

def remove_repeated_awards_entry_and_update_rows_in_dataframe(tuples_list):
    df = GV.CurrentUser.get_DF(3)
    ENTRY_COL = "EntryID"
    AWARDEE_COL = "AwardeeName"
    input_entry_ids = {t[1] for t in tuples_list}
    mask = df[ENTRY_COL].isin(input_entry_ids)
    df.loc[mask, :] = None
    new_rows = pd.DataFrame(
        [(t[0], t[1]) for t in tuples_list],
        columns=[AWARDEE_COL, ENTRY_COL]
    )
    empty_row_idx = df.index[df.isna().all(axis=1)].tolist()
    n_fill = min(len(empty_row_idx), len(new_rows))
    if n_fill > 0:
        df.loc[empty_row_idx[:n_fill], [AWARDEE_COL, ENTRY_COL]] = new_rows.iloc[:n_fill].to_numpy()
    if n_fill < len(new_rows):
        df = pd.concat([df, new_rows.iloc[n_fill:]], ignore_index=True)
    GV.CurrentUser.set_DF(df, 3)

def clear_dataframe_values(df):
    fill_with=""
    return pd.DataFrame([[fill_with] * len(df.columns) for _ in range(len(df))],
                        columns=df.columns)

def update_DF4_and_DF5_step1():
    df2 = GV.CurrentUser.get_DF(2)
    df4 = GV.CurrentUser.get_DF(4).reset_index(drop=True)

    # Clean df4 of any NaN/empty SongIDs before proceeding
    df4 = df4.dropna(subset=["SongID"])
    df4 = df4[df4["SongID"].astype(str).str.strip().isin(["", "nan", "None"]) == False]
    df4 = df4.astype(str).reset_index(drop=True)

    # Clean and filter df2
    df2 = df2.astype(str)
    df2 = df2[
        df2["SongID"].notna()
        & df2["EntryID"].notna()
        & df2["SongFullName"].notna()
        & (df2["SongID"].str.strip() != "")
        & (df2["SongID"].str.lower() != "nan")
    ].reset_index(drop=True)

    # Merge logic
    for _, row in df2.iterrows():
        song_id = row["SongID"].strip()
        entry_id = row["EntryID"].strip()
        song_name = row["SongFullName"].strip()

        if not song_id or not entry_id:
            continue

        if song_id in df4["SongID"].values:
            df4.loc[df4["SongID"] == song_id, "EntryIDs"] = (
                df4.loc[df4["SongID"] == song_id, "EntryIDs"].apply(
                    lambda x: f"{x},{entry_id}" if x.strip() else entry_id
                )
            )
        else:
            new_row = {"SongFullName": song_name, "SongID": song_id, "EntryIDs": entry_id}
            df4 = pd.concat([df4, pd.DataFrame([new_row])], ignore_index=True)

    # Final cleanup: remove any all-empty rows and reset index
    df4 = df4[df4["SongID"].str.strip() != ""].reset_index(drop=True)
    GV.CurrentUser.set_DF(df4, 4)

def update_DF4_and_DF5_step2():
    df3 = GV.CurrentUser.get_DF(3)
    df4 = GV.CurrentUser.get_DF(4)
    df3 = df3.astype(str)
    df4 = df4.astype(str)
    df4 = df4.replace('nan', '', regex=False)
    df4 = df4.replace('None', '', regex=False)
    df4['NormalizedSongFullName'] = df4['SongFullName'].str.lower().str.replace(r'\s+', '', regex=True)
    for _, row in df3.iterrows():
        entry_id = row["EntryID"].strip()
        awardee_name = row["AwardeeName"].strip()
        if entry_id.startswith("SAW"):
            normalized_awardee_name = awardee_name.lower().replace(" ", "")
            matching_rows_in_df4 = df4[df4['NormalizedSongFullName'] == normalized_awardee_name]
            if not matching_rows_in_df4.empty:
                for index, row_df4 in matching_rows_in_df4.iterrows():
                    current_op_award_ids = row_df4["OpAwardIDs"]
                    if current_op_award_ids.strip() == "":
                        new_op_award_ids = entry_id
                    else:
                        new_op_award_ids = f"{current_op_award_ids},{entry_id}"
                    df4.loc[index, "OpAwardIDs"] = new_op_award_ids
            else:
                new_row_data = {
                    "SongFullName": awardee_name, 
                    "SongID": "", # Set to empty string to match the rest of the clean df4
                    "OpAwardIDs": entry_id,
                    "EntryIDs": "" # Set to empty string to match the rest of the clean df4
                }
                new_row_df = pd.DataFrame([new_row_data])
                for col in df4.columns:
                    if col not in new_row_df.columns:
                        new_row_df[col] = ""
                new_row_df = new_row_df[df4.columns]
                df4 = pd.concat([df4, new_row_df], ignore_index=True)
                df4.loc[df4.index[-1], 'NormalizedSongFullName'] = awardee_name.lower().replace(" ", "")
    df4 = df4.drop(columns=['NormalizedSongFullName'])
    GV.CurrentUser.set_DF(df4, 4)

def add_artist_count_and_names_to_df4(song_title: str) -> None:
    df = GV.CurrentUser.get_DF(4)
    match_index = df[df['SongFullName'] == song_title].index

    row_index = match_index[0]
    
    artist_count, artist_list = BLF.song_artists_give_artist_count_and_list(song_title)

    # --- Step 5: Update the DataFrame ---
    
    # Update ArtistCount
    df.loc[row_index, 'ArtistCount'] = artist_count
    
    # Update Artists column: join list with " - " if size > 1, otherwise use the single value
    if len(artist_list) == 1:
        artist_string = artist_list[0]
    elif len(artist_list) > 1:
        artist_string = " - ".join(artist_list)
    else:
        artist_string = None # If list is empty
        
    df.loc[row_index, 'Artists'] = artist_string
    GV.CurrentUser.set_DF(df, 4)

def handle_artist_count_and_names_in_df4():#???
    df = GV.CurrentUser.get_DF(4)
    song_names_series = df['SongFullName']
    
    # Filter out NaNs (using .notna()) AND filter out empty strings (using != '')
    cleaned_series = song_names_series[
        song_names_series.notna() & (song_names_series != '')
    ]
    
    # --- 3. Convert to List and Return ---
    song_list = cleaned_series.tolist()
    
    for item in song_list:
        add_artist_count_and_names_to_df4(item)

def update_DF4_and_DF5_step3():

    df3 = GV.CurrentUser.get_DF(3)
    df4 = GV.CurrentUser.get_DF(4)
    df5 = GV.CurrentUser.get_DF(5)

    all_artists = set()
    for val in df4['Artists']:
        if isinstance(val, str) and val.strip() != '':
            parts = [p.strip() for p in val.split(' - ') if p.strip()]
            all_artists.update(parts)
    for _, row in df3.iterrows():
        entry_id = str(row['EntryID']).strip() if pd.notna(row['EntryID']) else ''
        awardee = str(row['AwardeeName']).strip() if pd.notna(row['AwardeeName']) else ''
        if entry_id.startswith('AAW') and awardee != '':
            all_artists.add(awardee)
    unique_list = list(all_artists)  # optional: sort for consistency
    if len(df5) < len(unique_list):
        extra_rows = len(unique_list) - len(df5)
        df5 = pd.concat([df5, pd.DataFrame({'ArtistName': [''] * extra_rows})], ignore_index=True)
    df5['ArtistName'] = pd.Series(unique_list[:len(df5)])
    GV.CurrentUser.set_DF(df5, 5)   
    df5 = assign_sequential_IDs(5, "ArtistName", "ArtistID", "ART0001")
    GV.CurrentUser.set_DF(df5, 5)

def update_DF4_and_DF5_step4():
    df4 = GV.CurrentUser.get_DF(4)
    df5 = GV.CurrentUser.get_DF(5)
    def get_all_artist_names_from_df4(artists_series):
        """Creates a mapping from a single artist name to the list of its source rows in df4."""
        artist_to_df4_info = {}
        for index, row in artists_series.to_frame().iterrows():
            artists_str = str(row['Artists']).strip()
            if artists_str and artists_str != 'nan':
                # Split by " - "
                names = [p.strip() for p in artists_str.split(' - ') if p.strip() and p.strip() != 'nan']
                
                # Gather all necessary info from the current df4 row (using index for reference)
                df4_info = {
                    'SongID': str(df4.loc[index, 'SongID']).strip() if pd.notna(df4.loc[index, 'SongID']) else '',
                    'EntryIDs': str(df4.loc[index, 'EntryIDs']).strip() if pd.notna(df4.loc[index, 'EntryIDs']) else '',
                    'ArtistIDs': str(df4.loc[index, 'ArtistIDs']).strip() if pd.notna(df4.loc[index, 'ArtistIDs']) else ''
                }

                for name in names:
                    if name not in artist_to_df4_info:
                        artist_to_df4_info[name] = {
                            'df4_index_list': [],
                            'info': df4_info
                        }
                    # Store the index where this name was found in df4
                    artist_to_df4_info[name]['df4_index_list'].append(index)
        return artist_to_df4_info
    df4_artist_map = get_all_artist_names_from_df4(df4['Artists'])
    
    # --- Process df5 and update both DFs ---
    
    # Prepare lists to store the accumulated updates before assigning them back
    new_df4_artist_ids = df4['ArtistIDs'].astype(str).replace('nan', '')
    new_df5_song_ids = df5['SongIDs'].astype(str).replace('nan', '')
    new_df5_entry_ids = df5['EntryIDs'].astype(str).replace('nan', '')
    
    # Keep track of ArtistIDs added to df4 to ensure we don't duplicate across df5 rows
    # Maps df4_index -> set_of_added_df5_artist_ids
    df4_id_updates = {idx: set() for idx in df4.index}

    for df5_idx, df5_row in df5.iterrows():
        df5_artist_name = str(df5_row['ArtistName']).strip()
        df5_artist_id = str(df5_row['ArtistID']).strip() if pd.notna(df5_row['ArtistID']) else ''

        if not df5_artist_name or df5_artist_name == 'nan':
            continue

        # 1. Check if the df5 artist name matches any name found in df4
        if df5_artist_name in df4_artist_map:
            
            # Get all df4 records associated with this matching artist name
            matched_df4_data = df4_artist_map[df5_artist_name]
            
            # --- A. Update df4['ArtistIDs'] ---
            if df5_artist_id:
                # Iterate over all df4 rows where this artist name appeared
                for df4_idx in matched_df4_data['df4_index_list']:
                    
                    # Only add the ArtistID if it hasn't been added to this specific df4 row yet
                    if df5_artist_id not in df4_id_updates[df4_idx]:
                        
                        current_ids = new_df4_artist_ids.get(df4_idx, '')
                        
                        if current_ids:
                            # Add comma separator if existing IDs are present
                            new_ids_str = f"{current_ids},{df5_artist_id}"
                        else:
                            # Just add the ID if the field was empty/NaN
                            new_ids_str = df5_artist_id
                            
                        new_df4_artist_ids.loc[df4_idx] = new_ids_str
                        df4_id_updates[df4_idx].add(df5_artist_id)

            # --- B. Update df5['SongIDs'] and df5['EntryIDs'] ---
            # Collect SongIDs / EntryIDs from ALL df4 rows where this artist matched
            song_ids_to_add = []
            entry_ids_to_add = []

            for df4_idx in matched_df4_data['df4_index_list']:
                # SongID from df4 row
                s = df4.loc[df4_idx, 'SongID'] if 'SongID' in df4.columns else np.nan
                if pd.notna(s):
                    s = str(s).strip()
                    if s and s != 'nan':
                        song_ids_to_add.append(s)

                # EntryIDs from df4 row (may be comma-separated already)
                e = df4.loc[df4_idx, 'EntryIDs'] if 'EntryIDs' in df4.columns else np.nan
                if pd.notna(e):
                    e = str(e).strip()
                    if e and e != 'nan':
                        # split existing list so we can merge cleanly
                        entry_ids_to_add.extend([p.strip() for p in e.split(',') if p.strip() and p.strip() != 'nan'])

            # Deduplicate while preserving order (minimal, stable)
            def dedupe_preserve_order(seq):
                seen = set()
                out = []
                for x in seq:
                    if x not in seen:
                        seen.add(x)
                        out.append(x)
                return out

            song_ids_to_add = dedupe_preserve_order(song_ids_to_add)
            entry_ids_to_add = dedupe_preserve_order(entry_ids_to_add)

            # Append to df5 SongIDs
            if song_ids_to_add:
                current_song_ids = str(new_df5_song_ids.loc[df5_idx]).strip()
                if current_song_ids and current_song_ids != 'nan':
                    existing = [p.strip() for p in current_song_ids.split(',') if p.strip() and p.strip() != 'nan']
                    merged = dedupe_preserve_order(existing + song_ids_to_add)
                else:
                    merged = song_ids_to_add
                new_df5_song_ids.loc[df5_idx] = ",".join(merged)

            # Append to df5 EntryIDs
            if entry_ids_to_add:
                current_entry_ids = str(new_df5_entry_ids.loc[df5_idx]).strip()
                if current_entry_ids and current_entry_ids != 'nan':
                    existing = [p.strip() for p in current_entry_ids.split(',') if p.strip() and p.strip() != 'nan']
                    merged = dedupe_preserve_order(existing + entry_ids_to_add)
                else:
                    merged = entry_ids_to_add
                new_df5_entry_ids.loc[df5_idx] = ",".join(merged)
                
    # --- Final Assignment ---
    df4['ArtistIDs'] = new_df4_artist_ids.replace('nan', np.nan)
    df5['SongIDs'] = new_df5_song_ids.replace('nan', np.nan)
    df5['EntryIDs'] = new_df5_entry_ids.replace('nan', np.nan)
    GV.CurrentUser.set_DF(df4, 4)
    GV.CurrentUser.set_DF(df5, 5)

def update_DF4_and_DF5_step5():
    df3 = GV.CurrentUser.get_DF(3)
    df5 = GV.CurrentUser.get_DF(5)

    new_op_award_ids = df5['OpAwardIDs'].astype(str).replace('nan', '')

    for df3_idx, df3_row in df3.iterrows():
        
        entry_id = str(df3_row['EntryID']).strip() if pd.notna(df3_row['EntryID']) else ''
        awardee_name = str(df3_row['AwardeeName']).strip() if pd.notna(df3_row['AwardeeName']) else ''
        
        # 1. Check EntryID (case-insensitive startswith 'AAW')
        if entry_id.upper().startswith('AAW'):
            
            if not awardee_name:
                continue # Skip if AwardeeName is empty
            
            # 2. Find matching rows in df5
            # We use .str.strip() on the column for robust comparison
            
            # Create a boolean mask for matching rows
            mask = df5['ArtistName'].astype(str).str.strip() == awardee_name
            
            if mask.any():
                # 3. & 4. Update OpAwardIDs in df5 for all matching rows
                
                # Iterate only over the indices that matched
                for df5_idx in df5[mask].index:
                    
                    current_ids = new_op_award_ids.get(df5_idx, '')
                    
                    # Prepare the entry to append (it's the full EntryID from df3)
                    id_to_add = entry_id 
                    
                    if current_ids:
                        # Add comma separator if existing IDs are present
                        new_ids_str = f"{current_ids},{id_to_add}"
                    else:
                        new_ids_str = id_to_add
                    new_op_award_ids.loc[df5_idx] = new_ids_str
    df5['OpAwardIDs'] = new_op_award_ids.replace('', np.nan)
    GV.CurrentUser.set_DF(df5, 5)


def update_DF4_and_DF5_step6():
    # --- hardcoded dataframe ---
    df = GV.CurrentUser.get_DF(4)  # <-- change DF number if needed

    target_col = "HighestAwardID"   # change to "HighestAwarID" if that's your real column name
    op_col = "OpAwardIDs"
    unop_col = "UnOpAwardIDs"

    if target_col not in df.columns:
        df[target_col] = np.nan

    def is_nonempty(x) -> bool:
        if pd.isna(x):
            return False
        s = str(x).strip()
        return bool(s) and s.lower() != "nan"

    def extract_last_digits(cell) -> list[int]:
        if not is_nonempty(cell):
            return []
        tokens = [t.strip() for t in str(cell).split(",") if t.strip() and t.strip().lower() != "nan"]
        out = []
        for t in tokens:
            if t and t[-1].isdigit():
                out.append(int(t[-2:]))#??? changed, does it work?
        return out

    for idx, row in df.iterrows():
        digits = extract_last_digits(row.get(op_col, np.nan)) + extract_last_digits(row.get(unop_col, np.nan))

        if not digits:
            df.at[idx, target_col] = 4
            continue

        m = min(digits)
        df.at[idx, target_col] = 4 if m >= 4 else m

    GV.CurrentUser.set_DF(df, 4)  # <-- change DF number if needed
    return df

def update_DF4_and_DF5_step7(year: int):
    df = GV.CurrentUser.get_DF(4)  # <-- change DF number if needed

    entry_col = "EntryIDs"
    out_col = "TempAwardIDs"

    if out_col not in df.columns:
        df[out_col] = np.nan
    def is_nonempty(x) -> bool:
        if pd.isna(x):
            return False
        s = str(x).strip()
        return bool(s) and s.lower() != "nan"
    def parse_entry_tokens(cell) -> list[str]:
        if not is_nonempty(cell):
            return []
        return [t.strip() for t in str(cell).split(",") if t.strip() and t.strip().lower() != "nan"]

    def append_csv(cell, new_val: str) -> str:
        new_val = str(new_val).strip()
        if not new_val:
            return "" if pd.isna(cell) else str(cell)

        if pd.isna(cell) or str(cell).strip() == "" or str(cell).strip().lower() == "nan":
            return new_val

        parts = [p.strip() for p in str(cell).split(",") if p.strip() and p.strip().lower() != "nan"]
        if new_val not in parts:
            parts.append(new_val)
        return ",".join(parts)

    # ---- compute counters per row ----
    counters = pd.Series(0, index=df.index, dtype=int)

    for idx, val in df.get(entry_col, pd.Series(index=df.index, dtype=object)).items():
        c = 0
        for token in parse_entry_tokens(val):
            token = str(token).strip()
            if len(token) < 6:
                continue
            mid3 = token[3:6]
            if not mid3.isdigit():
                continue
            if int(mid3) <= int(year):
                c += 1
        counters.at[idx] = c

    # ---- select rows with highest counter ----
    max_counter = int(counters.max()) if len(counters) else 0
    selected_idx = counters.index[counters == max_counter].tolist()
    # If too many rows share the max, stop
    if len(selected_idx) > GV.MAX_OVERALL_AWARD_COUNT:
        return df
    # ---- generate ID (same for all selected rows) ----
    award_id = f"SAO{int(year):03d}1{max_counter:04d}"
    # ---- append to TempAwardIDs for selected rows ----
    for idx in selected_idx:
        df.at[idx, out_col] = append_csv(df.at[idx, out_col], award_id)

    GV.CurrentUser.set_DF(df, 4)  # <-- change DF number if needed
    return df


def update_DF4_and_DF5_step9(year: int):
    year = int(year)

    df4 = GV.CurrentUser.get_DF(4)
    df5 = GV.CurrentUser.get_DF(5)

    artist_ids_col = "ArtistIDs"
    entry_col = "EntryIDs"
    song_col = "SongID"

    df5_artist_col = "ArtistID"
    df5_out_col = "TempAwardIDs"

    if df5_out_col not in df5.columns:
        df5[df5_out_col] = np.nan

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

        parts = [p.strip() for p in str(cell).split(",") if p.strip() and p.strip().lower() != "nan"]
        if new_val not in parts:
            parts.append(new_val)
        return ",".join(parts)

    # ---- Step 1: dict1 keys from df4 ArtistIDs ----
    dict1 = {}
    for cell in df4.get(artist_ids_col, pd.Series(dtype=object)):
        for aid in split_csv(cell):
            if aid not in dict1:
                dict1[aid] = []

    # ---- Step 2: fill dict1[artist_id] with SongIDs where ANY EntryID mid3 <= year ----
    for aid in dict1.keys():
        for _, row in df4.iterrows():
            row_artist_ids = split_csv(row.get(artist_ids_col, None))
            if aid not in row_artist_ids:
                continue
            analysis_true = False  # IMPORTANT: empty EntryIDs does NOT auto-pass
            for token in split_csv(row.get(entry_col, None)):
                token = str(token).strip()
                if len(token) < 6:
                    continue
                mid3 = token[3:6]
                if mid3.isdigit() and int(mid3) <= year:
                    analysis_true = True
                    break
            if analysis_true:
                song_id = row.get(song_col, None)
                if is_nonempty(song_id):
                    dict1[aid].append(str(song_id).strip())
    # ---- Step 3: dict2 groups artists by number of collected SongIDs ----
    dict2 = defaultdict(list)
    for aid, songs in dict1.items():
        dict2[len(songs)].append(aid)
    if not dict2:
        # nothing to do
        GV.CurrentUser.set_DF(df5, 5)
        return df5
    # ---- Step 4: largest key K, proceed only if <= 5 artists ----
    K = max(dict2.keys())
    top_artists = dict2[K]
    if len(top_artists) > GV.MAX_OVERALL_AWARD_COUNT:
        # finish here (no change)
        GV.CurrentUser.set_DF(df5, 5)
        return df5
    award_id = f"AAO{year:03d}2{K:04d}"
    # ---- Step 5: add award_id to df5 TempAwardIDs for matching ArtistID rows ----
    # Build fast lookup artist_id -> df5 indices (handles duplicates)
    df5_index_map = defaultdict(list)
    for idx, val in df5.get(df5_artist_col, pd.Series(dtype=object)).items():
        if is_nonempty(val):
            df5_index_map[str(val).strip()].append(idx)

    for aid in top_artists:
        for idx in df5_index_map.get(str(aid).strip(), []):
            df5.at[idx, df5_out_col] = append_csv(df5.at[idx, df5_out_col], award_id)
    GV.CurrentUser.set_DF(df5, 5)
    return df5


def print_stats(query: str, *, similarity_threshold: float = GV.stats_similarity_theshold) -> None:

    from difflib import SequenceMatcher

    df4 = GV.CurrentUser.get_DF(4)  # SongList
    df5 = GV.CurrentUser.get_DF(5)  # ArtistList
    score_map = GV.rank_to_score_suggestion_dict

    # ---------------- Helpers ----------------

    def normalize(s) -> str:
        """Lowercase + remove ALL whitespace. Safe for NaN/None."""
        if s is None:
            return ""
        try:
            if pd.isna(s):
                return ""
        except Exception:
            pass
        return "".join(str(s).split()).lower()

    def split_csv(cell) -> list[str]:
        """Split comma-separated cell into tokens; empty/NaN -> []"""
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s or s.lower() == "nan":
            return []
        return [t.strip() for t in s.split(",") if t.strip() and t.strip().lower() != "nan"]

    def count_items(cell) -> int:
        return len(split_csv(cell))

    def score_from_entryids(cell) -> float:
        """Leaderboard-style score: sum score_map[rank] from last-2-digits of EntryIDs tokens."""
        total = 0.0
        for tok in split_csv(cell):
            if len(tok) >= 2 and tok[-2:].isdigit():
                rank = int(tok[-2:])
                total += float(score_map.get(rank, 0))
        return total

    def similarity(a: str, b: str) -> float:
        """Alignment similarity [0..1]."""
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a, b).ratio()

    def parse_songfullname(full: str) -> tuple[str, str, str]:

        if full is None:
            return "", "", ""
        s = str(full).strip()

        if " - " in s:
            artist_part, title_full = s.split(" - ", 1)
            title_full = title_full.strip()
        else:
            # fallback (shouldn't happen per your data rule)
            artist_part, title_full = s, ""

        title_base = title_full.split("(", 1)[0].strip() if title_full else ""
        return artist_part.strip(), title_full, title_base

    # ---------------- Find matches (df4) ----------------

    qn = normalize(query)
    if not qn:
        print("Empty query. Please type a song name or artist name.")
        return

    # df4 row dedupe happens here: dict keyed by df4 index
    song_matches_map = {}   # df4_idx -> best_similarity
    song_match_reason = {}  # df4_idx -> reason string

    if "SongFullName" in df4.columns:
        for idx, val in df4["SongFullName"].items():
            full = str(val) if val is not None else ""
            full_n = normalize(full)
            if not full_n:
                continue

            artist_part, title_full, title_base = parse_songfullname(full)
            artist_n = normalize(artist_part)
            title_full_n = normalize(title_full)
            title_base_n = normalize(title_base)

            # Compute similarities for multiple fields
            sims = []

            # 1) Full match (Artist - Song ...)
            sim_full = 1.0 if full_n == qn else similarity(qn, full_n)
            sims.append(("full", sim_full))

            # 2) Title-full match (after " - ", including "(...)" if any)
            if title_full_n:
                sim_title_full = 1.0 if title_full_n == qn else similarity(qn, title_full_n)
                sims.append(("title_full", sim_title_full))

            # 3) Title-base match (after " - ", cut at first "(")
            #    This is the new feature you requested.
            #    Example: "Rainbow in the Dark (Dio Cover)" -> "Rainbow in the Dark"
            if title_base_n:
                sim_title_base = 1.0 if title_base_n == qn else similarity(qn, title_base_n)
                sims.append(("title_base", sim_title_base))

            # 4) Artist-only match (before " - ")
            if artist_n:
                sim_artist = 1.0 if artist_n == qn else similarity(qn, artist_n)
                sims.append(("artist", sim_artist))

            # pick best scoring match reason
            best_reason, best_sim = max(sims, key=lambda t: t[1])

            if best_sim >= similarity_threshold:
                # keep only best similarity for that df4 row index (dedupe)
                if idx not in song_matches_map or best_sim > song_matches_map[idx]:
                    song_matches_map[idx] = best_sim
                    song_match_reason[idx] = best_reason

    song_matches = sorted(song_matches_map.items(), key=lambda t: (-t[1], t[0]))

    # ---------------- Find matches (df5 artists) ----------------

    artist_matches = []
    if "ArtistName" in df5.columns:
        for idx, val in df5["ArtistName"].items():
            vn = normalize(val)
            if not vn:
                continue
            sim = 1.0 if vn == qn else similarity(qn, vn)
            if sim >= similarity_threshold:
                artist_matches.append((idx, sim))
        artist_matches.sort(key=lambda t: (-t[1], t[0]))

    if not song_matches and not artist_matches:
        print("No Match Found in DataBase (even with near-match search).")
        return

    print(f"\nResults for: {query.strip()}\n")

    # ---------------- Print song matches (df4) ----------------

    if song_matches:
        print("=== Song matches ===")
        reason_label_map = {
            "full": "matched full name",
            "title_full": "matched song title (full)",
            "title_base": "matched song title (Before Appendages)",
            "artist": "matched artist"
        }

        for idx, sim in song_matches:
            row = df4.loc[idx]
            name = str(row.get("SongFullName", ""))

            appearances = count_items(row.get("EntryIDs"))
            awards = (
                count_items(row.get("OpAwardIDs")) +
                count_items(row.get("UnOpAwardIDs")) +
                count_items(row.get("TempAwardIDs"))
            )
            score = score_from_entryids(row.get("EntryIDs"))

            sim_pct = int(round(sim * 100))
            reason = song_match_reason.get(idx, "full")
            reason_label = reason_label_map.get(reason, reason)

            print(f"\n• {name}  (match: {sim_pct}% | {reason_label})")
            print(f"  Score: {score:.3f}")
            print(f"  Total Appearances: {appearances}")
            print(f"  Total Awards: {awards}")
        print("")

    # ---------------- Print artist matches (df5) ----------------

    if artist_matches:
        print("=== Artist matches ===")

        # Build SongID -> df4 index map for per-song scoring
        songid_to_df4idx = {}
        if "SongID" in df4.columns:
            for i, sid in df4["SongID"].items():
                try:
                    if pd.isna(sid):
                        continue
                except Exception:
                    pass
                s = str(sid).strip()
                if s and s.lower() != "nan":
                    songid_to_df4idx.setdefault(s, i)

        for idx, sim in artist_matches:
            row = df5.loc[idx]

            artist_name = str(row.get("ArtistName", ""))
            appearances = count_items(row.get("EntryIDs"))
            total_songs_count = count_items(row.get("SongIDs"))
            awards = (
                count_items(row.get("OpAwardIDs")) +
                count_items(row.get("UnOpAwardIDs")) +
                count_items(row.get("TempAwardIDs"))
            )

            # Leaderboard-style score directly from artist EntryIDs
            artist_score_direct = score_from_entryids(row.get("EntryIDs"))

            # Score per song of this artist (computed from df4)
            song_scores = []
            for sid in split_csv(row.get("SongIDs")):
                df4_idx = songid_to_df4idx.get(sid)
                if df4_idx is None:
                    continue
                srow = df4.loc[df4_idx]
                sname = str(srow.get("SongFullName", ""))
                sscore = score_from_entryids(srow.get("EntryIDs"))
                song_scores.append((sname, sscore))

            song_scores.sort(key=lambda t: (-t[1], t[0]))
            artist_score_sum_songs = sum(s for _, s in song_scores)

            sim_pct = int(round(sim * 100))
            print(f"\n• {artist_name}  (match: {sim_pct}%)")
            #print(f"  Score (from Artist EntryIDs): {artist_score_direct:.3f}")
            print(f"  Score (sum of Artist's Songs): {artist_score_sum_songs:.3f}")
            print(f"  Total Appearances: {appearances}")
            print(f"  Total Songs: {total_songs_count}")
            print(f"  Total Awards: {awards}")

            if song_scores:
                print("  Songs by Score:")
                top_n = len(song_scores)
                #top_n = min(10, len(song_scores))
                for i in range(top_n):
                    sname, sscore = song_scores[i]
                    print(f"    - {sname} -> {sscore:.3f}")
            else:
                print("  (No song-score breakdown available: missing SongIDs or SongID mapping.)")

        print("")







"""


def print_stats(query: str, *, similarity_threshold: float = GV.stats_similarity_theshold) -> None:

    from difflib import SequenceMatcher

    df4 = GV.CurrentUser.get_DF(4)  # SongList
    df5 = GV.CurrentUser.get_DF(5)  # ArtistList
    score_map = GV.rank_to_score_suggestion_dict

    # ---------------- Helpers ----------------

    def normalize(s) -> str:
        if s is None:
            return ""
        try:
            if pd.isna(s):
                return ""
        except Exception:
            pass
        return "".join(str(s).split()).lower()

    def split_csv(cell) -> list[str]:
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s or s.lower() == "nan":
            return []
        return [t.strip() for t in s.split(",") if t.strip() and t.strip().lower() != "nan"]

    def count_items(cell) -> int:
        return len(split_csv(cell))

    def score_from_entryids(cell) -> float:
        total = 0.0
        for tok in split_csv(cell):
            if len(tok) >= 2 and tok[-2:].isdigit():
                rank = int(tok[-2:])
                total += float(score_map.get(rank, 0))
        return total

    def similarity(a: str, b: str) -> float:
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a, b).ratio()

    def parse_songfullname(full: str) -> tuple[str, str]:

        if full is None:
            return "", ""
        s = str(full).strip()
        if " - " in s:
            a, t = s.split(" - ", 1)
            return a.strip(), t.strip()
        return s, ""

    # ---------------- Find matches (df4) ----------------

    qn = normalize(query)
    if not qn:
        print("Empty query. Please type a song name or artist name.")
        return

    song_matches_map = {}  # df4_idx -> best_similarity
    song_match_reason = {} # df4_idx -> reason string

    if "SongFullName" in df4.columns:
        for idx, val in df4["SongFullName"].items():
            full = str(val) if val is not None else ""
            full_n = normalize(full)
            if not full_n:
                continue

            artist_part, title_part = parse_songfullname(full)
            artist_n = normalize(artist_part)
            title_n = normalize(title_part)

            # Compute similarities for multiple fields
            sims = []

            # 1) Full match (Artist - Song)
            sim_full = 1.0 if full_n == qn else similarity(qn, full_n)
            sims.append(("full", sim_full))

            # 2) Song-title-only match
            if title_n:
                sim_title = 1.0 if title_n == qn else similarity(qn, title_n)
                sims.append(("title", sim_title))

            # 3) Artist-only match (from df4)
            if artist_n:
                sim_artist = 1.0 if artist_n == qn else similarity(qn, artist_n)
                sims.append(("artist", sim_artist))

            # pick best
            best_reason, best_sim = max(sims, key=lambda t: t[1])

            if best_sim >= similarity_threshold:
                # keep the best similarity per row (in case multiple reasons qualify)
                if idx not in song_matches_map or best_sim > song_matches_map[idx]:
                    song_matches_map[idx] = best_sim
                    song_match_reason[idx] = best_reason

    # Turn map into sorted list
    song_matches = sorted(song_matches_map.items(), key=lambda t: (-t[1], t[0]))

    # ---------------- Find matches (df5 artists) ----------------

    artist_matches = []
    if "ArtistName" in df5.columns:
        for idx, val in df5["ArtistName"].items():
            vn = normalize(val)
            if not vn:
                continue
            sim = 1.0 if vn == qn else similarity(qn, vn)
            if sim >= similarity_threshold:
                artist_matches.append((idx, sim))
        artist_matches.sort(key=lambda t: (-t[1], t[0]))

    if not song_matches and not artist_matches:
        print("No Match Found in DataBase (even with near-match search).")
        return

    print(f"\nResults for: {query.strip()}\n")

    # ---------------- Print song matches (df4) ----------------

    if song_matches:
        print("=== Song matches ===")
        for idx, sim in song_matches:
            row = df4.loc[idx]
            name = str(row.get("SongFullName", ""))

            appearances = count_items(row.get("EntryIDs"))
            awards = (
                count_items(row.get("OpAwardIDs")) +
                count_items(row.get("UnOpAwardIDs")) +
                count_items(row.get("TempAwardIDs"))
            )
            score = score_from_entryids(row.get("EntryIDs"))

            sim_pct = int(round(sim * 100))
            reason = song_match_reason.get(idx, "full")
            reason_label = {
                "full": "matched full name",
                "title": "matched song title",
                "artist": "matched artist part"
            }.get(reason, reason)

            print(f"\n• {name}  (match: {sim_pct}% | {reason_label})")
            print(f"  Score: {score:.3f}")
            print(f"  Total Appearances: {appearances}")
            print(f"  Total Awards: {awards}")
        print("")

    # ---------------- Print artist matches (df5) ----------------

    if artist_matches:
        print("=== Artist matches ===")

        # Build SongID -> df4 index map for per-song scoring
        songid_to_df4idx = {}
        if "SongID" in df4.columns:
            for i, sid in df4["SongID"].items():
                try:
                    if pd.isna(sid):
                        continue
                except Exception:
                    pass
                s = str(sid).strip()
                if s and s.lower() != "nan":
                    songid_to_df4idx.setdefault(s, i)

        for idx, sim in artist_matches:
            row = df5.loc[idx]

            artist_name = str(row.get("ArtistName", ""))
            appearances = count_items(row.get("EntryIDs"))
            total_songs_count = count_items(row.get("SongIDs"))
            awards = (
                count_items(row.get("OpAwardIDs")) +
                count_items(row.get("UnOpAwardIDs")) +
                count_items(row.get("TempAwardIDs"))
            )

            # Leaderboard-style score directly from artist EntryIDs
            artist_score_direct = score_from_entryids(row.get("EntryIDs"))

            # Score per song of this artist (computed from df4)
            song_scores = []
            for sid in split_csv(row.get("SongIDs")):
                df4_idx = songid_to_df4idx.get(sid)
                if df4_idx is None:
                    continue
                srow = df4.loc[df4_idx]
                sname = str(srow.get("SongFullName", ""))
                sscore = score_from_entryids(srow.get("EntryIDs"))
                song_scores.append((sname, sscore))

            song_scores.sort(key=lambda t: (-t[1], t[0]))
            artist_score_sum_songs = sum(s for _, s in song_scores)

            sim_pct = int(round(sim * 100))
            print(f"\n• {artist_name}  (match: {sim_pct}%)")
            print(f"  Score (from Artist EntryIDs): {artist_score_direct:.3f}")
            print(f"  Score (sum of Artist's Songs): {artist_score_sum_songs:.3f}")
            print(f"  Total Appearances: {appearances}")
            print(f"  Total Songs: {total_songs_count}")
            print(f"  Total Awards: {awards}")

            if song_scores:
                print("  Songs by Score:")
                #top_n = min(10, len(song_scores))
                top_n = len(song_scores)
                for i in range(top_n):
                    sname, sscore = song_scores[i]
                    print(f"    - {sname} -> {sscore:.3f}")
            else:
                print("  (No song-score breakdown available: missing SongIDs or SongID mapping.)")

        print("")









def print_stats(query: str, *, similarity_threshold: float = 0.82) -> None:


    from difflib import SequenceMatcher

    df4 = GV.CurrentUser.get_DF(4)  # SongList
    df5 = GV.CurrentUser.get_DF(5)  # ArtistList
    score_map = GV.rank_to_score_suggestion_dict

    # ---------------- Helpers ----------------

    def normalize(s) -> str:
        #Lowercase + remove ALL whitespace. Safe for NaN/None.
        if s is None:
            return ""
        try:
            if pd.isna(s):
                return ""
        except Exception:
            pass
        return "".join(str(s).split()).lower()

    def split_csv(cell) -> list[str]:
        #Split comma-separated cell into tokens; empty/NaN -> []
        if cell is None:
            return []
        try:
            if pd.isna(cell):
                return []
        except Exception:
            pass
        s = str(cell).strip()
        if not s or s.lower() == "nan":
            return []
        return [t.strip() for t in s.split(",") if t.strip() and t.strip().lower() != "nan"]

    def count_items(cell) -> int:
        return len(split_csv(cell))

    def score_from_entryids(cell) -> float:

        total = 0.0
        for tok in split_csv(cell):
            if len(tok) >= 2 and tok[-2:].isdigit():
                rank = int(tok[-2:])
                total += float(score_map.get(rank, 0))
        return total

    def similarity(a: str, b: str) -> float:
        #Alignment similarity [0..1]
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a, b).ratio()

    def find_matches(df: pd.DataFrame, col: str, q: str, threshold: float) -> list[tuple[int, float]]:

        qn = normalize(q)
        if not qn:
            return []

        matches = []
        for idx, val in df[col].items():
            vn = normalize(val)
            if not vn:
                continue
            sim = 1.0 if vn == qn else similarity(qn, vn)
            if sim >= threshold:
                matches.append((idx, sim))

        # Sort best similarity first, then stable by index
        matches.sort(key=lambda t: (-t[1], t[0]))
        return matches

    # ---------------- Find matches ----------------

    song_matches = find_matches(df4, "SongFullName", query, similarity_threshold) if "SongFullName" in df4.columns else []
    artist_matches = find_matches(df5, "ArtistName", query, similarity_threshold) if "ArtistName" in df5.columns else []

    if not song_matches and not artist_matches:
        print("No Match Found in DataBase (even with near-match search).")
        return

    q_show = query.strip() if query is not None else ""
    print(f"\nResults for: {q_show}\n")

    # ---------------- Print song matches (df4) ----------------

    if song_matches:
        print("=== Song matches ===")
        for idx, sim in song_matches:
            row = df4.loc[idx]

            name = str(row.get("SongFullName", ""))
            appearances = count_items(row.get("EntryIDs"))
            awards = (
                count_items(row.get("OpAwardIDs")) +
                count_items(row.get("UnOpAwardIDs")) +
                count_items(row.get("TempAwardIDs"))
            )
            score = score_from_entryids(row.get("EntryIDs"))

            sim_pct = int(round(sim * 100))
            print(f"\n• {name}  (match: {sim_pct}%)")
            print(f"  Score: {score:.3f}")
            print(f"  Total Appearances: {appearances}")
            print(f"  Total Awards: {awards}")
        print("")

    # ---------------- Print artist matches (df5) ----------------

    if artist_matches:
        print("=== Artist matches ===")
        # Build a quick lookup for df4 SongID -> df4 row index
        songid_to_df4idx = {}
        if "SongID" in df4.columns:
            for i, sid in df4["SongID"].items():
                s = str(sid).strip() if sid is not None and not (isinstance(sid, float) and pd.isna(sid)) else ""
                if s and s.lower() != "nan":
                    songid_to_df4idx.setdefault(s, i)

        for idx, sim in artist_matches:
            row = df5.loc[idx]

            artist_name = str(row.get("ArtistName", ""))
            appearances = count_items(row.get("EntryIDs"))
            total_songs_count = count_items(row.get("SongIDs"))
            awards = (
                count_items(row.get("OpAwardIDs")) +
                count_items(row.get("UnOpAwardIDs")) +
                count_items(row.get("TempAwardIDs"))
            )

            # "Leaderboard-style" score directly from the artist's EntryIDs (how your leaderboard does df5)
            artist_score_direct = score_from_entryids(row.get("EntryIDs"))

            # Requested: score per song of the artist (computed from df4 rows)
            song_scores = []
            for sid in split_csv(row.get("SongIDs")):
                df4_idx = songid_to_df4idx.get(sid)
                if df4_idx is None:
                    continue
                srow = df4.loc[df4_idx]
                sname = str(srow.get("SongFullName", ""))
                sscore = score_from_entryids(srow.get("EntryIDs"))
                song_scores.append((sname, sscore))

            # Sort songs by score desc then name
            song_scores.sort(key=lambda t: (-t[1], t[0]))
            artist_score_sum_songs = sum(s for _, s in song_scores)

            sim_pct = int(round(sim * 100))
            print(f"\n• {artist_name}  (match: {sim_pct}%)")
            print(f"  Score (from Artist EntryIDs): {artist_score_direct:.3f}")
            print(f"  Score (sum of Artist's Songs): {artist_score_sum_songs:.3f}")
            print(f"  Total Appearances: {appearances}")
            print(f"  Total Songs: {total_songs_count}")
            print(f"  Total Awards: {awards}")

            if song_scores:
                print("  Top songs by score:")
                top_n = min(10, len(song_scores))
                for i in range(top_n):
                    sname, sscore = song_scores[i]
                    print(f"    - {sname} -> {sscore:.3f}")
            else:
                print("  (No song-score breakdown available: missing SongIDs or SongID mapping.)")

        print("")


def print_stats(query: str) -> None:
    # --- Hardcoded dataframes (replace with your real data) ---
    df4 = GV.CurrentUser.get_DF(4)
    df5 = GV.CurrentUser.get_DF(5)
    
    def normalize(s: Any) -> str:
        #Lowercase and remove all whitespace.
        if s is None:
            return ""
        try:
            if pd.isna(s):
                return ""
        except Exception:
            pass
        return "".join(str(s).split()).lower()

    def count_items(cell: Any) -> int:
        #Count comma-separated values in a cell. Empty/NaN -> 0.
        if cell is None:
            return 0
        try:
            if pd.isna(cell):
                return 0
        except Exception:
            pass
        s = str(cell).strip()
        if not s:
            return 0
        return len([t.strip() for t in s.split(",") if t.strip()])

    q = normalize(query)

    # --- 1) Try match in df4 (SongFullName) ---
    match4 = df4[df4["SongFullName"].apply(normalize) == q]
    if not match4.empty:
        row = match4.iloc[0]
        count1 = count_items(row.get("EntryIDs"))

        count2 = (
            count_items(row.get("OpAwardIDs")) +
            count_items(row.get("UnOpAwardIDs")) +
            count_items(row.get("TempAwardIDs"))
        )

        name = str(row.get("SongFullName", ""))
        print(f"Song: {name}")
        print(f"Total Appearances: {count1}")
        print(f"Total Awards: {count2}")
        return

    # --- 2) Try match in df5 (ArtistName) ---
    match5 = df5[df5["ArtistName"].apply(normalize) == q]
    if not match5.empty:
        row = match5.iloc[0]
        count1 = count_items(row.get("EntryIDs"))

        count2 = (
            count_items(row.get("OpAwardIDs")) +
            count_items(row.get("UnOpAwardIDs")) +
            count_items(row.get("TempAwardIDs"))
        )
        
        count3 = count_items(row.get("SongIDs"))

        name = str(row.get("ArtistName", ""))
        print(f"Artist: {name}")
        print(f"Total Appearances: {count1}")
        print(f"Total Songs: {count3}")
        print(f"Total Awards: {count2}")
        return

    # --- 3) No match ---
    print("No Match Found in DataBase")
"""


