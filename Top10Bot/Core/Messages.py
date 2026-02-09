import GlobalVariables as GV
import Formatting as FORM
#Messages

def welcoming_msgp ():
    print(f"Welcome to the TOP10BOT Version {GV.software_version_GC}.\n\
We're Still in Alpha Test So We Thank You for Your Patience in Advance.\n\n\
Any Bugs Reported to {GV.developer_email_string_GC} will be Checked and Fixed ASAP.\n\
Let's Get Started.\n\n ")


def what_action_msg():
    return "What Action would You Like to do? "
    
def you_have_chosen_msg(choice):
    print("You Have Chosen to {choice}.\n")

def wrong_format_look_help_msgi():
    return input("Input is Not in the Correct TOP10 Format! Take a Look at Formats for More Info \
Press Enter to Continue. ")

def type_code_msgi ():
    return FORM.refine_user_input_to_single_capital_letter(input("Type the Letter Corresponding to Your Choice Here: "))

def enter_something_msgi (entry):
    return input(f"Enter {entry}: ")

def choose_an_action_msg():
    return "Enter Your Choice: "

def press_enter():
    input("Press the Enter Key to Continue.\n")

def exit_message_msgi ():
    input("Hope to See You Back Soon.\n \nPress the Enter Key to Quit.")

def print_message_showing_valid_inputs_using_dicts(valid_input_dict):
    for key, value in valid_input_dict.items():
        print(f"Type {key} to choose {value}")
    print("")

def invalid_input_msg():
    return "!!! Invalid Input, Please Try Again !!!"

def module_under_construction_msgi():
    input("Module Under Construction, Please Press Enter to Continue.")

def entry_protocol_msgi():
    input("""Your Entries Should be in the Following Format:
          
-First Line Should Indicate the Type of Entry,
-Next the Entry Should Come in the Standard TOP10 Format (Use the Help Command for More Info),
-After Finishing the Entry, Hit the Enter Key Multiple Times Until the Input Process is Done.

Hit the Enter Key to Continue...    
          """)

def show_help1_msgp():#???
    print("""
Help:
The Entries Should Come in the Following Format:
    
1-Each Song Name is Divided Between Song Name and Band or Artist Name by
    a "-" Symbol with a Space on Each Side of the "-" Symbol
    So No "-" Symbol with a Space on Each Side is Allowed in the Artist's Name
    Example #1: Katatonia - Night Comes Down (Judas Priest Cover)
    Example #2: Breaking Benjamin - Breaking the Silence
    Example #3: Ozzy Osbourne - Let it Die
    
2-Songs with Miltiple Artists Should be written in the Following Format:
    The Artist Part of the Song Should be indicated by the Word "Feat."
    After the Name of the Main Artist and the Next Artists After that
    will be separated by the "," Symbol
    Example #1, A Song with One Artist:    Crosby, Stills, Nash & Young - Woodstock
    Example #2, A Song with Two Artists:   Seether Feat. Amy Lee - Broken
    Example #3, A Song with Five Artists:  Corey Taylor Feat. Jason Christopher, Christian Martucci, Roy Mayorga, Satchel - Rainbow in the Dark (Dio Cover)
    Example #4, A Song with One Artist:    Derek and the Dominos - Layla
    Example #5, A Song with Two Artists:   Slash Feat. Myles Kennedy and the Conspirators - Anastasia
    Example #6, A Song with One Artist: Joan Jett & the Blackhearts - Bad Reputation
""")
    

def show_help2_msgp():
    print("""
3-The Monthly Entry Should Consist of a Line Describing the Entry Followed by
    10 Lines Each Attributed to a Song, The Emojies are not Necessary in the Entry.
    You Can See Some Examples for the User Named "Amir":
Example #1:
    
#Amir's Top 10 Songs of Esfand of 97

🆕Van Halen - Ain’t Talkin' 'Bout Love
🆕Avenged Sevenfold - Afterlife
🆕Slash’s Snakepit - Serial Killer
🆕Limp Bizkit - Lonely World
🆕Iron Maiden - If Eternity Should Fail
🆕Ozzy Osbourn - I Just Want You
🆕Iron Maiden - Powerslave
🤘🏻Slash Feat. Myles Kennedy - Back from Cali
🤘🏻Black Sabbath - God is Dead?
🆕Blackfield - End of the World

Example #2:
            
#Amir's Top 10 Songs of Dey of 04

🆕Slipknot - Psychosocial
🥇Anthrax - The Devil You Know
🥉Alice in Chains - Hollow
🤘🏻Slipknot - Snuff
🆕The Mamas & The Papas - California Dreamin'
🆕Slipknot - Custer
🤘🏻Nine Inch Nails - Every Day is Exactly the Same
🤘🏻Creed - One Last Breath
🆕Korn - Another Brick in the Wall (Parts 1, 2, 3 - Pink Floyd Cover)
🥉Seal - Kiss from a Rose
          """)
          
def show_help3_msgp():#???
    print("""
4- Award Entries Should Consist of a Line at the Top that Indicates this Entry
is for Awards. After that for Each Specific Entry there Should be a line to 
Introduce the Specific Entry.
At the Time 1 Type of Opinionated Entry for Songs and 3 Types of Opinionated
Entries for Bands and Artists are Supported.
Note that You Should Not add Entries for Songs and also for Bands and Artists
at the Same Time.
The Following Examples would Illustrate Acceptable Entries.

Example #1, Song Award Entries:
    
#Amir's Awards for Songs in the Year 03

Opinionated Top 10 Songs of the Year 03
🥇Anthrax - The Devil You Know
🥈Soen - Sincere
🥉Alice in Chains - Down in a Hole
4️⃣Submersed - Price of Fame
5️⃣Submersed - Piano Song
6️⃣Tool - Schism
7️⃣Submersed - Answers
8️⃣Alter Bridge - Show Me a Sign
9️⃣U2 - Song for Someone
🔟Alter Bridge - Broken Wings
          
Example #2, Single Artist Award Entry:
    
#Amir's Awards for Bands and Artists in the Year 03
    
Opinionated Top 10 Bands and Artists of the Year 03
🥇Submersed
🥈Soen
🥉Alter Bridge
4️⃣Eminem
5️⃣Alice in Chains
6️⃣Tool
7️⃣Godsmack
8️⃣Hamilton (Original Broadway Cast Recording)
9️⃣Anthrax
🔟Poets of the Fall
          
Example #3, Multiple Artist Award Entries:
    
#Amir's Awards for Bands and Artists in the Year 03
    
Opinionated Top 10 Bands and Artists of the Year 03
🥇Submersed
🥈Soen
🥉Alter Bridge
4️⃣Eminem
5️⃣Alice in Chains
6️⃣Tool
7️⃣Godsmack
8️⃣Hamilton (Original Broadway Cast Recording)
9️⃣Anthrax
🔟Poets of the Fall

#MorriconeAward of the Year 00 for Lifetime Achievements of a Band or Artist
🏅Richard Clayderman

Award for the New-Comer Band or Artist of the Year 03
🏅Suno AI (Music Creator)

          """)
          
def alpha_test_error_msgp():
    print("\n⚠️ Something went wrong in this step. ⚠️ We are still in Alpha test so some minor errors are expected. ⚠️\
The app will try to continue.")

def show_about_msgp():
    print("""
The Top 10 Project started in early 2019 as a fun project among brothers,
Ali & Amir Zarghami.

The idea was simple:
let's take notes of the music we enjoy the most in a specific period to monitor
how our taste in music changes over time, and also to dversify our music taste
let's periodically designate some band or artist and focus more on them. 

Since the musci you listen to is a great reflection of your mental state and
also it's something indirect to measure other aspects of ones mindset, we found
it a fun side-project which did not take much time from us.

Over the years as time went by we added new aspects to the project and changed
some, but the core of the project remained the same.

However some of these new aspects were time consuming. So in order to make some
of these tasks easier to execute this program was born. First as an idea and now
in practice.

I would encourage you and others to join taking track of your music taste and
come with us on this journey.
          """)
    press_enter()
    
def show_credits_msgp():
    print("""
This program was conceptualized and coded by Amir Zarghami.
Contact developer at: Amir.Zarghami.13@Gmail.Com
          """)
    press_enter()

def show_formats_msgp():
    show_help1_msgp()
    press_enter()
    show_help2_msgp()
    press_enter()
    show_help3_msgp()
    press_enter()
    
def show_help_msgp():
    print("How to Use the Top 10 Bot and Each Command:\n\n")
    print("M or Monthly Entry, is Used to Add New Monthly Entries to DataBase.\nAcceptable Entry Formats are Visibile via the F or Format Command.\n")
    print("W or Award Entry, is Used to Add New Award Entries to DataBase.\nAcceptable Entry Formats are Visible via the F or Format Command.\n")
    print("L or LeaderBoard, Shows the Top Songs and Top Artists or Bands Based on Existing Monthly Entries.\nThe Scors are Somewhat Arbitrary Based on a Scoring Matrix but may be Usefull to Give You an Overall Overview.\n")
    print("T or Stats, Shows the Overall Stats for a Specific Song or Band or Artist Based on Existing Monthly and Award Entries.\n")
    print("V or View, Shows the Tag Corresponding to a Song Based on Previous Entries.\n")
    print("A or Award List, Shows the Awards for a Specific Year Based on Previous Entries.\n")
    print("G or Suggestions, Makes Suggestions for Opinionated Awards Based on Monthly Entries and an Arbitrary Scoring Matrix.\n")
    print("H or Help, Is what You are Currently Reading!\n")
    print("F or Format, Illustrates the Acceptable Entry Formats for Monthly Entris or Award Entries\n")
    print("U or Update, Updates All the Profile Tables Based on Monthly and Award Entris.\n")
    print("S or Save, Saves Your Inputs and Updates and Generally Your Progress to Your Profile.\n")
    print("X or Exit, Exits Your Current Profile without Exiting the Program Entirely.\n")
    print("Q or Quit, Quits the Program.\n")
    press_enter()
    print("If You Have Added Monthly Entries or Award Entries, We Recommend You to Update Your Tables Before Expecting any Output from the Bot.\nIt would be highly Possible for the Output to be Inaccurate if You Do Not Do So.\n")
    press_enter()
    
    

