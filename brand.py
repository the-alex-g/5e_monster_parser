from math import floor
from tables import *
from parser_utility import *

FUNCTIONS_REQUIRING_PROFBONUS = ["save", "opposedcheck"]


# returns in the form of "result (dice + bonus)"
def diceroll(num, size, *bonuses):
    total_bonus = 0
    for bonus in bonuses:
        total_bonus += bonus
    total = floor(num * (size / 2 + 0.5)) + total_bonus
    string = str(total) + " (" + str(num) + "d" + str(size)
    if total_bonus != 0:
        if total_bonus > 0:
            string += " + "
        else:
            string += " - "
        string += str(abs(total_bonus))
    return string + ")"


# returns in the form of "DC challenge Ability saving throw"
def save(ability, abilitybonus, profbonus):
    dc = 8 + abilitybonus + profbonus
    ability_name = ""
    if ability != "w/none":
        ability_name = ABILITIES_SPELLOUT[ability[2:]] + " "
    return "DC " + str(dc) + " " + ability_name + "saving throw"


# returns in the form of "DC challenge Ability saving throw"
def basicsave(ability, difficulty):
    ability_name = ""
    if ability != "w/none":
        ability_name = ABILITIES_SPELLOUT[ability[2:]] + " "
    return "DC " + str(difficulty) + " " + ability_name + "saving throw"


# returns the name with the proper indefinite article prefixed to it
def articulate(capitalized, *name):
    name = separate(name, " ")
    string = "a"
    if name[0].lower() in ["a", "e", "i", "o", "u"]:
        string += "n"
    if capitalized:
        string = string.title()
    return string + " " + name


# returns in the form of "DC challenge Ability (Skill) check"
def check(dc, *skill):
    skill = separate(skill, " ")
    return "DC " + str(dc) + " " + ABILITIES_SPELLOUT[SKILL_ABILITY[skill]] + " (" + SKILL_PRETTYNAME[skill] + ") check"


def opposedcheck(ability, abilitybonus, profbonus):
    dc = 8 + abilitybonus + profbonus
    ability_name = ""
    if ability != "w/none":
        ability_name = ABILITIES_SPELLOUT[ability[2:]] + " "
    return "DC " + str(dc) + " " + ability_name + "check"


def math(*stuff):
    return eval(separate(stuff, " "))


# returns in the form of "score (bonus)"
def stat(score):
    return str(score) + " (" + format_bonus(score_to_bonus(score)) + ")"


# returns spellname in italics
def spell(*spellname):
    return "\\textit{" + separate(spellname, " ") + "}"


# returns monster name in bold
def monster(*monstername):
    return "\\textbf{" + separate(monstername, " ") + "}"


# collects all parameters as a brand-recognized string group
def bind(*stuff):
    return "<" + separate(stuff, " ") + ">"


# returns a table mapping the roll of a die to ampersand-separated entries
def dicetable(diesize, title, *entries):
    endline = "\\\\\\hline"
    tablestring = "\\\\\\begin{tabular}{|l|l|}\\hline1d" + str(diesize) + "&" + title + endline
    entry_strings = []
    entry_string = ""
    for item in entries:
        if item == "&":
            entry_strings.append(entry_string)
            entry_string = ""
        else:
            entry_string += str(item) + " "
    entry_strings.append(entry_string)
    for i in range(0, diesize):
        tablestring += str(i + 1) + "&" + entry_strings[i] + endline
    tablestring += "\\end{tabular}"
    return tablestring


# returns a bulleted list of all items
def bulletlist(*items):
    return "\\\\\\begin{itemize}" + get_list_body(items) + "\\end{itemize}"


def numberlist(*items):
    return "\\\\\\begin{enumerate}" + get_list_body(items) + "\\end{enumerate}"


def get_list_body(items):
    list_body = ""
    entry = ""
    for item in items:
        if item == "&":
            list_body += "\\item " + entry
            entry = ""
        else:
            entry_string += str(item) + " "
    return list_body + "\\item " + entry


# builds and executes function from bracketed command string
def format_and_execute(field, stats, profbonus):
    formatted_field = ""
    in_function_body = False
    in_string_block = False
    arg_text = ""
    function_name = ""
    # the extra space at the end of field causes the last argument to be processed
    for char in field + " ":
        if char == "<":
            in_string_block = True
        elif char == ">":
            in_string_block = False
        elif char == " " and not in_string_block:
            if in_function_body:
                if formatted_field[-1] != "(":
                    formatted_field += ", "
                if arg_text in ABILITY_LIST:
                    arg_text = str(stats[arg_text])
                elif not arg_text.isdigit() and not arg_text == "True" and not arg_text == "False":
                    arg_text = "\"" + arg_text + "\""
                formatted_field += arg_text
                arg_text = ""
            else:
                formatted_field += "("
                in_function_body = True
        else:
            if in_function_body:
                arg_text += char
            else:
                formatted_field += char
                function_name += char
    if function_name in FUNCTIONS_REQUIRING_PROFBONUS:
        formatted_field += ", " + str(profbonus)
    return eval(formatted_field + ")")


# processes a string to extract and execute all bracketed command sequences
def resolve_functions(string, stats, profbonus):
    updated_string = ""
    field = ""
    field_started = False
    indentation_level = 0
    nested = False
    for char in string:
        if char == "[":
            if field_started:
                indentation_level += 1
                nested = True
                field += "["
            else:
                field_started = True
        elif char == "]":
            if indentation_level > 0:
                indentation_level -= 1
                field += "]"
            else:
                field_started = False
                if nested:
                    field = resolve_functions(field, stats, profbonus)
                updated_string += format_and_execute(field, stats, profbonus)
                field = ""
                nested = False
        elif field_started:
            field += char
        else:
            updated_string += char
    return updated_string


# processes all bracketed commands in the given string
def parse_string(string, stats, params):
    for key in params:
        string = string.replace("[" + key + "]", str(params[key]))
    return resolve_functions(string, stats, params["profbonus"])
