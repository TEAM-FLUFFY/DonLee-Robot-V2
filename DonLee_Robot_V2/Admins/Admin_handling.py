# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee-Robot-V2/blob/Professor-99/LICENSE

import re
import time
from typing import List
from pyrogram.types import Message, InlineKeyboardButton
from DonLee_Robot_V2 import Config

COMMAND_HAND_LER = Config.COMMAND_HAND_LER

MATCH_MD = re.compile(r'\*(.*?)\*|'
                      r'_(.*?)_|'
                      r'`(.*?)`|'
                      r'(?<!\\)(\[.*?\])(\(.*?\))|'
                      r'(?P<esc>[*_`\[])')

LINK_REGEX = re.compile(r'(?<!\\)\[.+?\]\((.*?)\)')
BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))"
)


def button_markdown_parser(msg: Message) -> (str, List):
    # offset = len(args[2]) - len(raw_text)
    # set correct offset relative to command + notename
    markdown_note = None
    if msg.media:
        if msg.caption:
            markdown_note = msg.caption.markdown
    else:
        markdown_note = msg.text.markdown
    note_data = ""
    buttons = []
    if markdown_note is None:
        return note_data, buttons
    #
    if markdown_note.startswith(COMMAND_HAND_LER):
        args = markdown_note.split(None, 2)
        # use python's maxsplit to separate cmd and args
        markdown_note = args[2]
    prev = 0
    for match in BTN_URL_REGEX.finditer(markdown_note):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            # create a thruple with button label, url, and newline status
            if bool(match.group(4)) and buttons:
                buttons[-1].append(InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3)
                ))
            else:
                buttons.append([InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3)
                )])
            note_data += markdown_note[prev:match.start(1)]
            prev = match.end(1)
        # if odd, escaped -> move along
        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
    note_data += markdown_note[prev:]

    return note_data, buttons


def extract_time(time_val):
    if not any(time_val.endswith(unit) for unit in ('s', 'm', 'h', 'd')):
        return None
    unit = time_val[-1]
    time_num = time_val[:-1]  # type: str
    if not time_num.isdigit():
        return None

    if unit == 's':
        bantime = int(time.time() + int(time_num))
    elif unit == 'm':
        bantime = int(time.time() + int(time_num) * 60)
    elif unit == 'h':
        bantime = int(time.time() + int(time_num) * 60 * 60)
    elif unit == 'd':
        bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
    else:
        # how even...?
        return None
    return bantime