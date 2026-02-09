"""
We have Devided Our Working Functions into 3 Different Modules:
    
    Base Level Functions: these are Functions that may be Used in Different Routes
    and Scenarios, are Written in a Universal Using Manner
    
    Mid Level Functions: these are Functions that are Specified to a Specific Task
    and might Give Varried Returns Depending on their Task
    
    Navigation Functions: these are Functions that are Specified to a Task,
    Handle the Return Part of the Mid Level Functions and Return log, route, stage
"""

import GlobalVariables as GV
import Messages as MSG
import BaseLevelFunctions as BLF
import MidLevelFunctions as MLF
import DFsSaveLoad as DFSL
from tqdm import tqdm

def navf_command_starting_phase(log, route, stage):
    route = MLF.command_starting_program(log)
    if not log:
        if route == "Q":
            return log, route, "quiting"
        if route == "N":
            return log, route, "get username"
        if route == "L":
            return log, route, "get username"
        if route == "C":
            return log, route, "credits"
        if route == "A":
            return log, route, "about"
    elif log:
        if route == "A":
            stage = "ask update"
            return log, route, stage
        if route == "G":
            stage = "ask update"
            return log, route, stage
        if route == "T":
            stage = "ask update"
            return log, route, stage
        if route == "L":
            stage = "ask update"
            return log, route, stage
        if route == "U":
            stage = "updating"
            return log, route, stage
        if route == "M":
            stage = "get and check and add to df"
            return log, route, stage
        if route == "W":
            stage = "get and check and add to df"
            return log, route, stage
        if route == "H":
            return log, route, "show help"
        if route == "F":
            return log, route, "show formats"
        if route == "Q":
            stage = "ask save"
            return log, route, stage
        if route == "V":
            stage = "ask update"
            return log, route, stage
        if route == "S":
            stage = "saving"
            return log, route, stage
        if route == "X":
            stage = "ask save"
            return log, route, stage
        return log, "Z", "starting"

def navf_get_username_check_exists_decide(log, route, stage):
    if route == "N":
        user, route = MLF.creating_profile_get_username()
    elif route == "L":
        user, route = MLF.loading_profile_get_username()
    if route =="Z":
        return log, route, "starting"
    elif route == "N":
        GV.CurrentUser.set_name(user)
        return log, route, "get profile info"
    elif route == "L":
        GV.CurrentUser.set_name(user)
        return log, route, "loading"
    
def navf_get_user_info(log, route, stage):
    cal_code = MLF.get_cal_from_user()
    year = MLF.get_first_year()
    month = MLF.get_first_month(cal_code)
    print("")
    cal_name = GV.supported_calendars_codetoname[cal_code]
    GV.CurrentUser.set_cal(cal_name)
    GV.CurrentUser.set_version(GV.software_version_GC)
    GV.CurrentUser.set_first_month (year*100 + month)
    GV.CurrentUser.set_cal_code(cal_code)
    #GV.CurrentUser.set_cal_code(GV.supported_calendars_codetoname[cal_code])#???GPTFIX
    print(f"Creating a Profile Named {GV.CurrentUser.Name} with the Calendar {GV.CurrentUser.Cal}.")
    print("")
    return False, "N", "creating profile"

def navf_under_construction(log, route, stage):
    MSG.module_under_construction_msgi()
    return log, "Z", "starting"

def navf_quiting_program(log, route, stage):
    MSG.exit_message_msgi()

def navf_create_DFs_new_profile(log, route, stage):
    GV.CurrentUser.fill_profile_secondary_attributes()
    MLF.create_DFs_new_profile()
    return False, "N", "saving"

def navf_save_profile(log, route, stage):
    GV.CurrentUser.save_profile()
    if route == "Q":
        GV.CurrentUser.reset_profile()
        return False, "Q", "quiting"
    elif route == "N":
        return True, "Z", "starting"
    elif route == "S":
        return True, "Z", "starting"
    elif route == "X":
        GV.CurrentUser.reset_profile()
        return False, "Z", "starting"
    
def navf_ask_save(log, route, stage):
    save = MLF.ask_if_want_to_save()
    if save:
        MLF.save_user_data_to_file()
    if route == "X":
        GV.CurrentUser.reset_profile()
        return False, "Z", "starting"
    elif route == "S":
        return True, "Z", "starting"
    elif route == "Q":
        GV.CurrentUser.reset_profile()
        return False, "Q", "quiting"

def navf_load_DFs(log, route, stage):
    GV.CurrentUser.load_DFs_from_name()
    GV.CurrentUser.load_basic_values_from_DF1()
    GV.CurrentUser.load_profile_values_from_basics()
    return True, "Z", "starting"    

def navf_show_formats(log, route, stage):
    MSG.show_formats_msgp()
    print("")
    return log, "Z", "starting"
    
def navf_help(log, route, stage):
    MSG.show_help_msgp()
    #input("Press Enter Key to Contunie.")
    print("")
    return log, "Z", "starting"

def navf_credits(log, route, stage):
    MSG.show_credits_msgp()
    #input("Press Enter Key to Contunie.")
    print("")
    return log, "Z", "starting"

def navf_about(log, route, stage):
    MSG.show_about_msgp()
    print("")
    return log, "Z", "starting"

def navf_get_entry(log, route, stage):
    if route == "M":
        is_monthly, entry = MLF.get_monthly_check_lines_validity()
        if is_monthly:
            has_correct_format, inputs_list_song_ID = MLF.give_songs_with_IDs_raw(entry)
            if not has_correct_format:
                MSG.wrong_format_look_help_msgi()
                return log, "Z", "starting"
            elif has_correct_format:
                write = not MLF.check_if_monthly_entry_exists_in_df(inputs_list_song_ID)
                if write:
                    MLF.get_monthly_entry_tuple_add_to_DF(inputs_list_song_ID)
                    print("Entry Added to Your Profile.\n")
                    #DFSL.assign_sequential_IDs(2, "SongFullName", "SongID", "SNG0001")#???GPTFIX
                    df2 = DFSL.assign_sequential_IDs(2, "SongFullName", "SongID", "SNG0001")
                    GV.CurrentUser.set_DF(df2, 2)
                    GV.CurrentUser.set_needs_update(True)
                    print("Updating Tables. \n")
                else:
                    return log, "Z", "starting"
        else:
            MSG.wrong_format_look_help_msgi()
        return log, "Z", "starting"
    elif route == "W":
        is_award, entry_type, entry = MLF.get_award_check_lines_validity()
        if is_award:
            entry_line_by_line = entry.split("\n")
            year = int(entry_line_by_line[0][-2:])
            year = BLF.calculate_modified_year(year)
            if entry_type == "song" or entry_type == "artist":
                award_with_IDs = MLF.give_award_IDs(entry)#???
                write = not MLF.check_if_award_entry_exists_in_df(award_with_IDs)
                if write:
                    DFSL.remove_repeated_awards_entry_and_update_rows_in_dataframe(award_with_IDs)
                    GV.CurrentUser.set_needs_update(True)
                    print("Entry Added to Your Profile.\n")       
                else:
                    return log, "Z", "starting"
            else:
                MSG.wrong_format_look_help_msgi()
            #print(award_with_IDs)#???
        else:   
            MSG.wrong_format_look_help_msgi()
    return log, "Z", "starting"

def navf_update_DF4_and_DF5(log, route, stage):
    DFSL.ensure_df45_schema()
    save = BLF.get_input_command_repeatedly_until_valid(GV.yes_or_no_dict, \
    "Due to a Relatively High Possibility of Crashing, We Highly Recommend Saving Your Progress Before Moving on. Would You Like to Save your Progress? ", \
        "Enter Your Choice Here: ", "", MSG.invalid_input_msg())
    if save == "Y":
        MLF.save_user_data_to_file()
    #00Clean Up DF4 and DF5
    MLF.clear_DF4_DF5()
    years_with_awards_list = GV.CurrentUser.get_award_year_list()
    
    fixed_steps = 6  # step1, step2, handle_artist_count, step3, step4, step5
    total_units = fixed_steps + len(years_with_awards_list) + 1 + len(years_with_awards_list)
    #                  ^loop1 years            ^step6         ^loop2 years
    
    with tqdm(total=total_units, desc="General Updates", unit="step") as pbar:
        DFSL.update_DF4_and_DF5_step1(); pbar.update(1)
        DFSL.update_DF4_and_DF5_step2(); pbar.update(1)
        DFSL.handle_artist_count_and_names_in_df4(); pbar.update(1)
        DFSL.update_DF4_and_DF5_step3(); pbar.update(1)
        DFSL.update_DF4_and_DF5_step4(); pbar.update(1)
        DFSL.update_DF4_and_DF5_step5(); pbar.update(1)
    
        # loop1 (NO tqdm here)
        for year in years_with_awards_list:
            awards_dict = MLF.group_songs_by_entry_match_count(year)
            awards_dict_ID = BLF.transform_dict_to_id_keyed(awards_dict, year, 1, "SAU")
            BLF.update_df_from_map(awards_dict_ID, 4, "SongID", "UnOpAwardIDs")
            pbar.update(1)
    
        DFSL.update_DF4_and_DF5_step6(); pbar.update(1)
    
        # loop2 (NO tqdm here)
        for year in years_with_awards_list:
            DFSL.update_DF4_and_DF5_step7(year)
            awards_dict1 = BLF.cascade_filter_dictionary(MLF.group_artists_by_entry_count(year))
            awards_dict1_ID = BLF.transform_dict_to_id_keyed(awards_dict1, year, 1, "AAU")
            BLF.update_df_from_map(awards_dict1_ID, 5, "ArtistID", "UnOpAwardIDs")
    
            awards_dict2 = BLF.cascade_filter_dictionary(MLF.group_artists_by_single_month_entries(year))
            awards_dict2_ID = BLF.transform_dict_to_id_keyed(awards_dict2, year, 3, "AAU")
            BLF.update_df_from_map(awards_dict2_ID, 5, "ArtistID", "UnOpAwardIDs")
    
            awards_dict3 = BLF.cascade_filter_dictionary(MLF.group_artists_by_unique_songs(year))
            awards_dict3_ID = BLF.transform_dict_to_id_keyed(awards_dict3, year, 2, "AAU")
            BLF.update_df_from_map(awards_dict3_ID, 5, "ArtistID", "UnOpAwardIDs")
    
            MLF.update_DF4_and_DF5_step8(year)
            DFSL.update_DF4_and_DF5_step9(year)
    
            pbar.update(1)

    print("Tables are Updated.\n")
    if route == "U":
        route = "Z"
        stage = "starting"
    else:
        stage = "get input"
    GV.CurrentUser.set_needs_update(False)
    return log, route, stage

def navf_leaderboard(log, route, stage):
    print("")
    MLF.print_leaderboard(25)
    print("")
    MSG.press_enter()
    return log, "Z", "starting"


def navf_ask_if_update_needed(log, route, stage):
    print("test1\n")
    if GV.CurrentUser.get_needs_update() == True:
        print("test2\n")
        print("\n")
        answer = BLF.get_input_command_repeatedly_until_valid(GV.yes_or_no_dict, "Would You Like to Update The Tables Before We Proceed? \nUpdating the Tables Takes a Long Time but for Accurate Results is Highly Recommended \nSpecifically if You Have Added Entries to Your Profile Since the Last Update. ", \
                                             "What Do You Wish to do? ", "", MSG.invalid_input_msg())
        if answer == "Y":
            return log, route, "updating"
        else:
            return log, route, "get input"
    else:
        print("test3")
        return log, route, "get input"

def navf_song_tag_viewer(log, route, stage):
    print(MLF.function_to_view_song_tags())
    return log, "Z", "starting"

def navf_show_awards(log, route, stage):
    MLF.see_awards()
    return True, "Z", "starting"#???

def navf_stats(log, route, stage):
    my_string = input("Enter the Song Name or Artist Name for which You would Like to See the Stats: ")
    DFSL.print_stats(my_string)
    print("")
    MSG.press_enter()
    return log, "Z", "starting"

def navf_suggestions(log, route, stage):
    year = BLF.get_year()
    year = year%100
    print(MLF.suggestions_top_songs(year))
    MSG.press_enter()
    print(MLF.suggestions_top_artists(year))
    MSG.press_enter()
    return log, "Z", "starting"

def navf_see_awards(log, route, stage):
    MLF.see_awards()
    MSG.press_enter()
    return log, "Z", "starting"
    
    

