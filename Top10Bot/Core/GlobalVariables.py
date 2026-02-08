# -*- coding: utf-8 -*-
"""
This Module Contains Global Variables Such as Constants, Dicts and Lists

"""

from pathlib import Path
import pandas as pd
from typing import List
#------------------------------------------------------------------------------

### GLOBAL CONSTANTS #####

software_version_GC = 1.01 #as you update this value keep in mind to update prog to prof compatability dict in the DictsListsStuff Module
MAX_AWARD_COUNT = 20
MAX_OVERALL_AWARD_COUNT = 5
program_directory_path_GC = Path(__file__).resolve().parent
program_directory_string_GC = str(program_directory_path_GC)
profile_directory_path_GC = program_directory_path_GC.parent / "Profiles"
profile_directory_string_GC = str(profile_directory_path_GC)
#defult_directory_string_GC = "D://Important Stuff//Top10Bot" ### WILL CHANGE IN THE FINAL VERSION TO DIRECTORY OF PROGRAM
developer_email_string_GC = "Amir.Zarghami.13@Gmail.Com"

#------------------------------------------------------------------------------

##### CALENDARS #####

supported_calendars_codetoname = { "H": "Hejri Shamsi" , "G": "Gregorian"}
supported_calendars_nametocode = {"Hejri Shamsi": "H", "Gregorian": "G"}

################### Intra Modular

HejriShamsi_MtN = {"Farvardin":1, "Ordibehesht": 2, "Khordad": 3,
                   "Tir": 4, "Mordad": 5, "Shahrivar":6,
                   "Mehr": 7, "Aban":8, "Azar": 9,
                   "Dey": 10, "Bahman":11, "Esfand":12}

HejriShamsi_NtM = {1:"Farvardin", 2:"Ordibehesht", 3:"Khordad",
                   4:"Tir", 5:"Mordad", 6:"Shahrivar",
                   7:"Mehr", 8:"Aban", 9:"Azar",
                   10:"Dey", 11:"Bahman", 12:"Esfand"}

Miladi_MtN = {"January":1, "February": 2, "March": 3,
                   "April": 4, "May": 5, "June":6,
                   "July": 7, "Agust":8, "September": 9,
                   "October": 10, "November":11, "December":12}

Miladi_NtM = {1:"January", 2:"February", 3:"March",
                   4:"April", 5:"May", 6:"June",
                   7:"July", 8:"Agust", 9:"September",
                   10:"October", 11:"November", 12:"December"}

HejriShamsi_dict = { "MtN": HejriShamsi_MtN, "NtM": HejriShamsi_NtM }

Miladi_dict = { "MtN": Miladi_MtN, "NtM": Miladi_NtM }

################### Inter Modular *********************************************

#each key is a dict which has two keys MtN and NtM, the value of each is a dict itself
calendar_code_to_dict = {"H": HejriShamsi_dict, "G": Miladi_dict}

def month_count(cal):
    return max(cal["NtM"].keys())

##### GENERAL COMMANDS #####

yes_or_no_dict = {"Y": "Yes", "N": "No"}

song_or_artist_dict = {"S": "Song", "A": "Band and Artist"}

##### STAGE COMMANDS #####
"""
routing_log_to_route_to_stage_dict = \
        {False:{"N": ["starting", "get username", "get profile info", "creating profile", "saving"], \
        "L": ["get username", "loading"],\
        "Q": ["quiting"], \
        "Z": ["starting"]}, \
        True: {"M":[], \
        "W":[], \
        "H":[], \
        "V":[], \
        "A":[], \
        "S":[], \
        "X":[], \
        "Q":["quiting"], \
        "Z": ["starting"]}}
"""
not_logged_in_route_codetoname_dict = {"N": "Create a New Profile", "L": "Load an Existing Profile", \
                                       "A": "Read About this Program", "C": "Show Credits", "Q": "Quit the Program"}
logged_in_route_codetoname_dict = {"M": "Add Monthly Entry to Profile", "W": "Add Award Entry to Profile",\
                                   "L": "See LeaderBoard", "T": "Show Stats",\
                                   "V": "View Tag for a Song", "A": "Show Awards List", "G": "Suggest Opinionated Awards", \
                                   "H": "Help", "F": "See Input Format", \
                                   "U": "Update Tables", "S": "Save Progress to Profile", "X": "Exit Current Profile", "Q": "Quit the Program" }

routing_log_to_route_to_name_dict = {False: not_logged_in_route_codetoname_dict, True: logged_in_route_codetoname_dict}

#####CSV Headers#####

CSVFile_Headers_dict = {"RawUserInfo": ["UserName", "FirstMonth", "Version", "Calendar"],
                "RawMonthlyEntries": ["SongFullName", "EntryID", "SongID"],
                "RawAwardEntries": ["AwardeeName", "EntryID"],
                "SongList": ["SongFullName", "SongID", "EntryIDs", "ArtistCount", "Artists", "ArtistIDs", "OpAwardIDs", "UnOpAwardIDs", "TempAwardIDs", "HighestAwardID"],
                "ArtistList": ["ArtistName", "ArtistID", "SongIDs", "EntryIDs", "OpAwardIDs", "UnOpAwardIDs", "TempAwardIDs"]}




##### EMOJIZ DICT #####

emojiz_list = ["4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", \
    "🥉", "🤘🏻", "🤘🏼", "🤘🏽", "🤘🏾", "🤘🏿", "🆕", "✅", "🎖", "🥇", "🥈", "🏅", "🏆"]
    
score_to_emoji_dict ={-1: "🎖", 0: "🏆", 1: "🥇", 2: "🥈", 3: "🥉", 4: "🤘🏻", 5: "🆕",6: "🏅"}

rank_to_emoji_dict = {-1: "🎖", 0: "🏆", 1: "🥇", 2: "🥈", 3: "🥉", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟",\
                      11: "🏅", 12: "🏅"}
 
    
#------------------

def extract_unique_entry_numbers(df, col_name, output_chars) -> List[str]: 
    unique_numbers = set()
    for entry_id in df[col_name].dropna():
        entry_str = str(entry_id).strip()
        # Check if the string is long enough to contain the 3-char prefix + 3-digit number (at least 6 chars)
        if len(entry_str) >= 3+output_chars:
            # Slice: Start at index 3 (the 4th character), take 3 characters (indices 3, 4, 5)
            # Check if the extracted part is purely numeric (as requested)
            extracted_part = entry_str[3:3+output_chars]
            if extracted_part.isdigit():
                extracted_part = int(extracted_part)
                unique_numbers.add(extracted_part)
    result_list = sorted(list(unique_numbers))
    return result_list


class User:
    def __init__(self, name, calendar, first_month, version):
        self.Name = name
        self.Cal = calendar
        self.FM = first_month
        self.V = version
        self.CalCode = None
        self.CalDict = None
        self.AwardYearList = None
        self.ProbableCurrentMonth = None
        self.Dir = None
        self.File = None
        self.DF1 = None
        self.DF2 = None
        self.DF3 = None
        self.DF4 = None
        self.DF5 = None
    
    # --- getters ---
    def get_name(self):
        return self.Name

    def get_cal(self):
        return self.Cal

    def get_version(self):
        return self.V
    
    def get_first_month(self):
        return self.FM
    
    def get_cal_code(self):
        return self.CalCode
    
    def get_cal_dict(self):
        return self.CalDict
            
    def set_award_year_list(self):
        self.AwardYearList = extract_unique_entry_numbers(self.get_DF(3), "EntryID", 3)
    
    def get_award_year_list(self):
        self.set_award_year_list()
        return self.AwardYearList
    
    def set_probable_current_month(self):
        df2 = self.get_DF(2)
        df3 = self.get_DF(3)
        output = 0
        def is_valid_entryid(x):
            if pd.isna(x):
                return False
            s = str(x).strip()
            return bool(s) and s.lower() != "nan"
        highest_3 = None
        if "EntryID" in df3.columns:
            for x in df3["EntryID"]:
                if not is_valid_entryid(x):
                    continue
                s = str(x).strip()
                if len(s) < 6:
                    continue
                mid3 = s[3:6]  # next three characters after the first 3
                if not mid3.isdigit():
                    continue
                n = int(mid3)
                highest_3 = n if highest_3 is None else max(highest_3, n)
        if highest_3 is not None:
            output = 100 * highest_3 + 1  # as you requested
        if "EntryID" in df2.columns:
            valid_series = df2["EntryID"].apply(is_valid_entryid)
            if valid_series.any():
                last_val = df2.loc[valid_series, "EntryID"].iloc[-1]
                s = str(last_val).strip()
                if len(s) >= 8:
                    next5 = s[3:8]
                    if next5.isdigit():
                        n2 = int(next5)
                        output = max(output, n2)
        if output%100 == 12:
            output+=89
        else:
            output +=1
        self.ProbableCurrentMonth = output
        return output
    
    def get_probable_current_month(self):
        self.set_probable_current_month()
        return self.ProbableCurrentMonth
    
    def get_dir(self):
        return self.Dir
    
    def get_file(self):
        return self.File
    
    def get_DF(self, num):
        if num == 1:
            return self.DF1
        if num == 2:
            return self.DF2
        if num == 3:
            return self.DF3
        if num == 4:
            return self.DF4
        if num == 5:
            return self.DF5
        
    def get_DFs(self):
        return (self.DF1, self.DF2, self.DF3, self.DF4, self.DF5)
    
    # --- getters ---
    
    def set_name(self, new_name):
        self.Name = new_name
    
    def set_cal(self, cal_name):
        self.Cal = cal_name
        
    def set_version(self, version):
        self.V = version
        
    def set_first_month(self, first_month):
        self.FM = first_month
        
    def set_cal_code(self, cal_code):
        self.CalCode = cal_code
        
    def set_cal_dict(self, cal_dict):
        self.CalDict = cal_dict    

    def set_dir(self):
        self.Dir = program_directory_string_GC
        return self.Dir
        
    def set_file(self):
        self.File = profile_directory_string_GC +"//" + self.Name + "_TOP10BOT.xlsx"
        return self.File
        
    def set_DF(self, df, num):
        if num == 1:
            self.DF1 = df
        if num == 2:
            self.DF2 = df
        if num == 3:
            self.DF3 = df
        if num == 4:
            self.DF4 = df
        if num == 5:
            self.DF5 = df
    
    def set_DFs(self, df_list):
        self.DF1, self.DF2, self.DF3, self.DF4, self.DF5 = df_list
    
    # --- other functions
    
    def fill_profile_secondary_attributes(self):
        self.set_file()
        self.set_dir()
        self.set_cal_code(supported_calendars_nametocode[self.get_cal()])
        self.set_cal_dict(calendar_code_to_dict[self.get_cal_code()])
        
    def reset_profile(self):
        self.set_name("")
        self.set_cal(None)
        self.set_version(None)
        self.set_first_month(None)
        self.set_cal_code(None)
        self.set_cal_dict(None)
        self.set_dir()
        self.set_file()

    def load_DFs_from_name(self):
        self.set_file()
        file_path = self.get_file()
        # Reads every sheet into a dict of DataFrames
        dfs_dict = pd.read_excel(file_path, sheet_name=None)
        self.set_DFs(list(dfs_dict.values()))
        """
        print ("DF1: ", self.DF1) #???
        print ("DF2: ", self.DF2) #???
        print ("DF3: ", self.DF3) #???
        print ("DF4: ", self.DF4) #???
        print ("DF5: ", self.DF5) #???
        """
        
    def load_basic_values_from_DF1(self):
        self.set_first_month(self.DF1.iloc[0, 1])
        self.set_version(self.DF1.iloc[0, 2])
        self.set_cal(self.DF1.iloc[0, 3])
        
    def load_profile_values_from_basics(self):
        self.set_cal_code(supported_calendars_nametocode[self.Cal])
        self.set_cal_dict(calendar_code_to_dict[self.CalCode])
        self.set_dir()
        self.set_file()
            
    def load_profile(self):
        self.load_DFs_from_name()
        self.load_basic_values_from_DF1()
        self.load_profile_values_from_basics()
    
    def save_profile(self):
        df1 = self.DF1
        df2 = self.DF2
        df3 = self.DF3
        df4 = self.DF4
        df5 = self.DF5
        # --- Choose your output directory (example: a folder next to this .py file) ---
        out_path = self.get_file() #GV.CurrentUser.File
        # --- Write each dataframe to a different sheet ---
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            df1.to_excel(writer, sheet_name="RawUserInfo", index=False)
            df2.to_excel(writer, sheet_name="RawMonthlyEntries", index=False)
            df3.to_excel(writer, sheet_name="RawAwardEntries", index=False)
            df4.to_excel(writer, sheet_name="SongList", index=False)
            df5.to_excel(writer, sheet_name="ArtistList", index=False)
        print(f"Data Has been Saved to: {out_path}\n")
    
CurrentUser = User (None, None, None, None) #???   
    
def get_available_profile_names(directory):
    suffix = "_TOP10BOT"
    base_dir = Path(directory)
    return sorted(
        p.stem[:-len(suffix)]
        for p in base_dir.glob(f"*{suffix}.xlsx")
        if p.is_file() and p.stem.endswith(suffix)
    )


rank_to_score_suggestion_dict = {1: 10, 2:9.113, 3: 8.366, 4: 7.764, 5:7.246, 6: 6.816, 7: 6.428, 8: 6.079, 9: 5.777, 10: 5.505}






"""
Reminder to Self:
    
    
SongID                                                          SNG + generated code (4)
ArtistID                                                        ART + generated code (4)
Monthly Entry ID                                                MNT + modified year (3) + Month (2) + Rank (2)
Song of the Year Award Entry ID                                 SAW + modified year (3) + 00
Song Award Entry ID                                             SAW + modified year (3) + rank (2)
Artist of the year Award Entry ID                               AAW + modified year (3) + 00
Artist Award Entry ID                                           AAW + modified year (3) + rank (2)
Artist Morricone Award Entry ID                                 AAW + modified year (3) + 11
Artist NewComer Award Entry ID                                  AAW + modified year (3) + 12
Song Most App Award ID (UnOp type=1)                            SAU + modified year (3) + type (1) + score (2) + rank (1)
Artist Most App Award ID (UnOp type=1)                          AAU + modified year (3) + type (1) + score (2) + rank (1)
Artist Unique Songs Award ID (UnOp type=2)                      AAU + modified year (3) + type (1) + score (2) + rank (1)
Artist Most Songs in Single Month Award ID (UnOp type=3)        AAU + modified year (3) + type (1) + score (2) + rank (1)
Song Overall Most Apps Award (Overall type=1)                   SAO + modified year granted (3) + type (1) + score (4)
Artist Overall Most Apps Award (Overall type=1)                 AAO + modified year granted (3) + type (1) + score (4)
Artist Overall Unique Songs Award ID (Overall type=2)           AAO + modified year granted (3) + type (1) + score (4)

"""
