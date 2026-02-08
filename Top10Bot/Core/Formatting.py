# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 19:08:57 2026

@author: Lenovo
"""
import GlobalVariables as GV
import regex as re
#Formatting

def format_first_upper_rest_lower(name):
    if len(name) == 0:
        print("check1")
        return name
    new_name = name[0].upper()
    for no in range(1, len(name)):
        new_name += name[no].lower()
    return new_name

def check_input_validity_in_list(input_being_checked, valid_answers_list):
    for item in valid_answers_list:
        if input_being_checked==item:
            return True
    return False

def remove_numbers_from_string(text):
    cleaned_text = re.sub(r'\d', '', text)
    return cleaned_text

#Input: user input    Output: single capital letter
def refine_user_input_to_single_capital_letter(raw_user_input):
    if len(raw_user_input)==0:
        return raw_user_input
    else:
        return raw_user_input[0].upper()

def check_year(num, first_or_any):
    if type(num) == int or (type(num)== float and num%1==0):
        if first_or_any == "f":
            if 0<=num<100:
                return True
        if first_or_any == "a":
            if 0<=num<200:
                return True
    return False

def remove_space_keep_first_part(name):
    return name.split()[0]


def remove_chars_from_string(input_string, chars_to_remove):
    chars_set = set(chars_to_remove)
    new_string = "".join([char for char in input_string if char not in chars_set])
    return new_string

# Pre-compile patterns for speed
_KEYCAP_RE = re.compile(r'^[0-9#*]\uFE0F?\u20E3$')          # 4️⃣ / 4⃣ / #️⃣ / *️⃣
_FLAG_RE   = re.compile(r'^\p{Regional_Indicator}{2}$')    # 🇬🇧 etc.

# Emoji detection:
# - \p{Emoji_Presentation}: chars that default to emoji presentation
# - \p{Extended_Pictographic}: broad set of pictographic emoji (covers most modern emoji)
_EMOJIISH_RE = re.compile(r'(\p{Emoji_Presentation}|\p{Extended_Pictographic})')

def demojify(text: str):
    if text is None:
        return text

    clusters = re.findall(r"\X", text)

    def is_emoji_cluster(c: str) -> bool:
        # Keycap emoji sequences (digit/#/* + optional VS16 + enclosing keycap)
        if _KEYCAP_RE.match(c):
            return True

        # Country flags are regional-indicator pairs
        if _FLAG_RE.match(c):
            return True

        # Most other emoji (including ZWJ sequences) contain at least one
        # Emoji_Presentation or Extended_Pictographic code point
        if _EMOJIISH_RE.search(c):
            return True

        return False

    cleaned = "".join(c for c in clusters if not is_emoji_cluster(c))

    # Optional: tidy spaces
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned



def check_if_is_monthly_entry(text, name, valid_values):
    text_no_space = text.replace(" ", "")
    name_pattern = re.escape(name)
    values_pattern = "|".join(map(re.escape, valid_values))
    # Pattern (note spaces removed)
    pattern1 = fr"^#{name_pattern}'sTop10Songsof({values_pattern})of([0-9]{{2}})$"
    pattern2 = fr"^#{name_pattern}’sTop10Songsof({values_pattern})of([0-9]{{2}})$"
    match1 = re.match(pattern1, text_no_space, re.IGNORECASE)
    match2 = re.match(pattern2, text_no_space, re.IGNORECASE)
    match = match1 or match2
    return bool(match)

def check_if_is_song_award_entry_first_line(text, name):
    text_no_space = text.replace(" ", "")
    name_pattern = re.escape(name)
    pattern1 = fr"^#{name_pattern}'sAwardsforSongsintheyear([0-9]{{2}})$"
    pattern2 = fr"^#{name_pattern}’sAwardsforSongsintheyear([0-9]{{2}})$"
    match1 = re.match(pattern1, text_no_space, re.IGNORECASE)
    match2 = re.match(pattern2, text_no_space, re.IGNORECASE)
    match = match1 or match2
    return bool(match)

def check_if_is_artist_award_entry_first_line(text, name):
    text_no_space = text.replace(" ", "")
    name_pattern = re.escape(name)
    pattern1 = fr"^#{name_pattern}'sAwardsforBandsandArtistsintheYear([0-9]{{2}})$"
    pattern2 = fr"^#{name_pattern}’sAwardsforBandsandArtistsintheYear([0-9]{{2}})$"
    match1 = re.match(pattern1, text_no_space, re.IGNORECASE)
    match2 = re.match(pattern2, text_no_space, re.IGNORECASE)
    match = match1 or match2
    return bool(match)

def check_if_is_song_op_award(text):
    text_no_space = text.replace(" ", "")
    if text_no_space[:-2] == "OpinionatedTop10SongsoftheYear":
        try:
            year = int(text_no_space[-2:])
            return True
        except:
            return False
    return False

def check_if_is_artist_op_award(text):
    text_no_space = text.replace(" ", "")
    if text_no_space[:-2] == "OpinionatedTop10BandsandArtistsoftheYear":
        try:
            year = int(text_no_space[-2:])
            return True
        except:
            return False
    return False

def check_if_is_newcomer_award(text):
    text_no_space = text.replace(" ", "")
    if text_no_space[:-2] == "AwardfortheNew-ComerBandorArtistoftheYear":
        try:
            year = int(text_no_space[-2:])
            return True
        except:
            return False
    return False

def check_if_is_morricone_award(text):
    text_no_space = text.replace(" ", "")
    if remove_numbers_from_string(text_no_space) == "#MorriconeAwardoftheYearforLifetimeAchievementsofaBandorArtist":
        return True
    else:
        return False   

def pad_number(num, n):
    num = int(num)
    return str(num).zfill(n)
   
def add_string_to_num(num, string):
    return string + str(num)

def take_ID_give_number(ID):
    ID = ID[3:]
    return int(ID)

def strip_only_empty_or_whitespace_lines(multiline_string):
    lines = multiline_string.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

def demojify_multilines(multiline_string):
    lines = multiline_string.splitlines()
    demojified_lines = [demojify(line) for line in lines]
    return "\n".join(demojified_lines)



