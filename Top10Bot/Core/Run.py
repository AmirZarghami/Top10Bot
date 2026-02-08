# -*- coling: utf-8 -*-
"""
This Module is the Main Module to Run the Program.
"""

import GlobalVariables as GV
import Messages as MSG
import NavFunctions as NF
import logging
import traceback

logger = logging.getLogger("alpha_test_logger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = logging.FileHandler("error_log.txt", mode="a", encoding="utf-8")
    logger.addHandler(fh)

class StateOfProgram:
    def __init__(self, log, route, stage):
        self.log = log
        self.route = route
        self.stage = stage

state = StateOfProgram(False, "Z", "starting") #???

#??? under  parts
map_nav_input_to_functions_dict = {(False, "Z", "starting"): NF.navf_command_starting_phase, \
                                   (False, "N", "get username"): NF.navf_get_username_check_exists_decide, \
                                   (False, "N", "get profile info"): NF.navf_get_user_info, \
                                   (False, "N", "creating profile"): NF.navf_create_DFs_new_profile, \
                                   (False, "N", "saving"): NF.navf_save_profile, \
                                   (False, "L", "get username"): NF.navf_get_username_check_exists_decide, \
                                   (False, "L", "loading"): NF.navf_load_DFs, \
                                   (False, "A", "about"): NF.navf_about, \
                                   (False, "C", "credits"): NF.navf_credits, \
                                   (False, "Q", "quiting"): NF.navf_quiting_program, \
                                   (True, "Z", "starting"): NF.navf_command_starting_phase, \
                                   (True, "M", "get and check and add to df"): NF.navf_get_entry, \
                                   (True, "W", "get and check and add to df"): NF.navf_get_entry, \
                                   (True, "A", "ask update"): NF.navf_ask_if_update_needed, \
                                   (True, "A", "updating"): NF.navf_update_DF4_and_DF5, \
                                   (True, "A", "get input"): NF.navf_see_awards, \
                                   (True, "V", "ask update"): NF.navf_ask_if_update_needed, \
                                   (True, "V", "updating"): NF.navf_update_DF4_and_DF5, \
                                   (True, "V", "get input"): NF.navf_song_tag_viewer, \
                                   (True, "G", "ask update"): NF.navf_ask_if_update_needed, \
                                   (True, "G", "updating"): NF.navf_update_DF4_and_DF5, \
                                   (True, "G", "get input"): NF.navf_suggestions, \
                                   (True, "L", "ask update"): NF.navf_ask_if_update_needed, \
                                   (True, "L", "updating"): NF.navf_update_DF4_and_DF5, \
                                   (True, "L", "get input"): NF.navf_leaderboard, \
                                   (True, "T", "ask update"): NF.navf_ask_if_update_needed, \
                                   (True, "T", "get input"): NF.navf_stats, \
                                   (True, "F", "show formats"): NF.navf_show_formats, \
                                   (True, "H", "show help"): NF.navf_help, \
                                   (True, "U", "updating"): NF.navf_update_DF4_and_DF5, \
                                   (True, "S", "saving"): NF.navf_ask_save, \
                                   (True, "X", "ask save"): NF.navf_ask_save, \
                                   (True, "Q", "ask save"): NF.navf_ask_save}
    
map_dic = map_nav_input_to_functions_dict

def navigation (log, route, stage):
    #print(f"***log={log}, route={route},stage={stage}***")#???
    temp_log, temp_route, temp_stage = log, route, stage
    for key in map_dic.keys():
        if (log, route, stage) == key:
            func = map_dic[key]
            result = func(log, route, stage)
            try:
                temp_log, temp_route, temp_stage = result
            except:
                pass
    return temp_log, temp_route, temp_stage


#***** RUN *****#
GV.CurrentUser.reset_profile()

if __name__ == "__main__":
    MSG.welcoming_msgp()
    """
    while((state.log != False) or (state.route != "Q")):
        state.log, state.route, state.stage = navigation(state.log, state.route, state.stage)
    """
    while((state.log != False) or (state.route != "Q")):    
        try:
            state.log, state.route, state.stage = navigation(state.log, state.route, state.stage)
        except Exception as e:
            logger.error("Error in navigation step:\n%s", "".join(
            traceback.format_exception(type(e), e, e.__traceback__)
            ))
            MSG.alpha_test_error_msgp() 
            print("Details were saved to 'error_log.txt'.\n")
            print("Send the error_log.txt file to the developer to help improve the software. \n")
            state.route, state.stage = "Z", "starting"

    print("\n")
    MSG.exit_message_msgi()



