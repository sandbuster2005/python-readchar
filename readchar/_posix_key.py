from ._base_key import *
# common
BACKSPACE = "\x7f"
import subprocess
import re
import sys
import logging

module = sys.modules[__name__]

def _remove( text : str, chrs : list[str] ) -> str:
    """
    cette fonction permet de remplacer dans word les string contenu dans chr par new
    """
    return [text := f"".join( text.split( chraracter ) ) for chraracter  in chrs ][-1]

name_correspondances = {
    "ESC"                : "kbs",        #backspace key
    "BEGIN"              : "kbeg",       #begin key
    "CLEAR_ALL_TAB"      : "ktbc",       #clear-all-tabs key
    "CLEAR"              : "kclr",       #clear-screen or erase key
    "CLEAR_TAB"          : "kctab",      #clear-tab key
    "BACK_TAB"           : "kcbt",       #back tab key
    "ENTER"              : "kent",       #enter key
    "DELETE"             : "kdch1",      #delete-character key
    "UNkbown"            : "kdl1",       #delete-line key
    "END"                : "kend",       #end key
    "END_OF_LINE"        : "kel",        #clear-to-end-of-line key
    "END_OF_SCREEN"      : "ked",        #clear-to-end-of-screen key
    "HOME"               : "khome",      #home key
    "INSERT_C"           : "kich1",      #insert-character key
    "INSERT_LINE"        : "kil1",       #insert-line key
    "HOME_DOWN"          : "kll",        #lower-left key (home down)
    "PAGE_UP"            : "knp",        #next-page key
    "PAGE_DOWN"          : "kpp",        #previous-page key
    "SCROLL_FORWARD"     : "kind",       #scroll-forward key
    "SCROLL_BACKWARD"    : "kri",        #scroll-backward key
    "SET_TAB"            : "khts",       #set-tab key
    "RIGHT"              : "kcuf1",      #right-arrow key
    "LEFT"               : "kcub1",      #left-arrow key
    "UP"                 : "kcuu1",      # up arrow key
    "DOWN"               : "kcud1",      # down-arrow key
    "PAD_UP_DOWN"        : "ka1",        #upper left of keypad
    "PAD_UP_RIGHT"       : "ka3",        #upper right of keypad
    "PAD_CENTER"         : "kb2",        #center of keypad
    "PAD_DOWN_LEFT"      : "kc1",        #lower left of keypad
    "PAD_DOWN_RIGHT"     : "kc3",        #lower right of keypad
    "SHIFT_EXIT"         : "kEXT",       #shifted exit key
    "SHIFT_FIND"         : "kFND",       #shifted find key
    "SHIFT_HELP"         : "kHLP",       #shifted help key
    "SHIFT_HOME"         : "kHOM",       #shifted home key
    "SHIFT_INSERT_C"     : "kIC",        #shifted insert-character key
    "SHIFT_LEFT"         : "kLFT",       #shifted left-arrow key
    "SHIFT_RIGHT"        : "kRIT",       #shifted right-arrow key
    "SHIFT_UP"           : "kUP",        #shifted up-arrow
    "SHIFT_DOWN"         : "kDN",        #shifted down-arrow
    "SHIFT_MESSAGE"      : "kMSG",       #shifted message key
    "SHIFT_MOVE"         : "kMOV",       #shifted move key
    "SHIFT_NEXT"         : "kNXT",       #shifted next key
    "SHIFT_OPTIONS"      : "kOPT",       #shifted options key
    "SHIFT_PREVIOUS"     : "kPRV",       #shifted previous key
    "SHIFT_PRINT"        : "kPRT",       #shifted print key
    "SHIFT_REDO"         : "kRDO",       #shifted redo key
    "SHIFT_REPLACE"      : "kRPL",       #shifted replace key
    "SHIFT_RESUME"       : "kRES",       #shifted resume key
    "SHIFT_SAVE"         : "kSAV",       #shifted save key
    "SHIFT_SUSPEND"      : "kSPD",       #shifted suspend key
    "SHIFT_UNDO"         : "kUND",       #shifted undo key
    "SHIFT_DELETE_LINE"  : "kDL",        #shifted delete line
    "SHIFT_DELETE_C"     : "kDC",        #shifted delete chracter
    "SHIFT_END"          : "kEND",       #shifted end key
    "F0"                 : "kf0",        #F0 function key
    "F1"                 : "kf1",        #F1 function key
    "F2"                 : "kf2",        #F2 function key
    "F3"                 : "kf3",        #F3 function key
    "F4"                 : "kf4",        #F4 function key
    "F5"                 : "kf5",        #F5 function key
    "F6"                 : "kf6",        #F6 function key
    "F7"                 : "kf7",        #F7 function key
    "F8"                 : "kf8",        #F8 function key
    "F9"                 : "kf9",        #F9 function key
    "F10"                : "kf10",       #F10 function key
    "F11"                : "kf11",       #F11 function key
    "F12"                : "kf12",       #F12 function key
    "F13"                : "kf13",       #F13 function key
    "F14"                : "kf14",       #F14 function key
    "F15"                : "kf15",       #F15 function key
    "F16"                : "kf16",       #F16 function key
    "F17"                : "kf17",       #F17 function key
    "F18"                : "kf18",       #F18 function key
    "F19"                : "kf19",       #F19 function key
    "F20"                : "kf20",       #F20 function key
    "F21"                : "kf21",       #F21 function key
    "F22"                : "kf22",       #F22 function key
    "F23"                : "kf23",       #F23 function key
    "F24"                : "kf24"        #F24 function key
}
normal_mode = [
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    "END",
    "BEGIN",
    "ENTER",
    "HOME",
    "PAD_CENTER",
    "PAD_UP_DOWN",
    "PAD_UP_RIGHT",
    "PAD_DOWN_LEFT",
    "PAD_DOWN_RIGHT"
]

data = subprocess.check_output(["infocmp","-x"])
print(data)
data = data.decode("utf-8")
data = _remove(data , ["\n","\t"," "]) # new line tabs and spaces
data = re.split("(?<=(?!\\\\).)," ,data) # split by "," and avoid "\,"
keys = {}  # create dico with existing key

for x in range( len(data) ):
    new_data = data[x].split("=")
    if len(new_data) > 1 and new_data[0][0] == "k": # is a key and is attributed
        keys[new_data[0]] = new_data[1]

for key in name_correspondances.keys():

    value = None

    if name_correspondances[key] in keys.keys():
        if key in normal_mode:
            print(keys[name_correspondances[key]])
            value = "\x1B" + "\x5B" + keys[name_correspondances[key]][3:] # terminals tend to be in normal mode and termnfo give app mode
        else:
            value = "\x1B" + keys[name_correspondances[key]][2:] # convert \E  to his code

    setattr(module,key,value)

    if not value:
        logging.warn(f'{key} is not supported on this device')

ENTER = LF
SUPR = DELETE
