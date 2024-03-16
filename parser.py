import yaml
from math import floor

ABILITIES_SPELLOUT = {
    "str":"Strength",
    "dex":"Dexterity",
    "con":"Constitution",
    "int":"Intelligence",
    "wis":"Wisdom",
    "cha":"Charisma"
}
ABILITY_LIST = ["str", "dex", "con", "int", "wis", "cha"]
HIT_DIE_SIZE = {
    "tiny":4,
    "small":6,
    "medium":8,
    "large":10,
    "huge":12,
    "gargantuan":20
}
SKILL_ABILITY = {
    "athletics":"str",
    "acrobatics":"dex",
    "sleight of hand":"dex",
    "stealth":"dex",
    "arcana":"int",
    "history":"int",
    "investigation":"int",
    "nature":"int",
    "religion":"int",
    "animal handling":"wis",
    "insight":"wis",
    "medicine":"wis",
    "perception":"wis",
    "survival":"wis",
    "deception":"cha",
    "intimidation":"cha",
    "performance":"cha",
    "persuasion":"cha"
}
SKILL_PRETTYNAME = {
    "athletics":"Athletics",
    "acrobatics":"Acrobatics",
    "sleight of hand":"Sleight of Hand",
    "stealth":"Stealth",
    "arcana":"Arcana",
    "history":"History",
    "investigation":"Investigation",
    "nature":"Nature",
    "religion":"Religion",
    "animal handling":"Animal Handling",
    "insight":"Insight",
    "medicine":"Medicine",
    "perception":"Perception",
    "survival":"Survival",
    "deception":"Deception",
    "intimidation":"Intimidation",
    "performance":"Performance",
    "persuasion":"Persuasion"
}
CR_TO_XP = {
    0:"10",
    "1/8":"25",
    "1/4":"50",
    "1/2":"100",
    1:"200",
    2:"450",
    3:"700",
    4:"1,100",
    5:"1,800",
    6:"2,300",
    7:"2,900",
    8:"3,900",
    9:"5,000",
    10:"5,900",
    11:"7,200",
    12:"8,400",
    13:"10,000",
    14:"11,500",
    15:"13,000",
    16:"15,000",
    17:"18,000",
    18:"20,000",
    19:"22,000",
    20:"25,000",
    21:"33,000",
    22:"41,000",
    23:"50,000",
    24:"62,000",
    25:"75,000",
    26:"90,000",
    27:"105,000",
    28:"120,000",
    29:"135,000",
    30:"155,000",
}
NEWLINE = "\\\\"


filedict = {}


def cr_to_prof(cr):
    if type(cr) == str:
        return 2
    else:
        return min(2, floor((cr - 1) / 4) + 2)


def diceroll(num, size, bonus):
    total = floor(num * (size / 2 + 0.5)) + bonus
    string = str(total) + " (" + str(num) + "d" + str(size)
    if bonus != 0:
        if bonus > 0:
            string += " + "
        else:
            string += " - "
        string += str(bonus)
    return string + ")"


def save(ability, abilitybonus, profbonus):
    dc = 8 + abilitybonus + profbonus
    return "DC " + str(dc) + " " + ABILITIES_SPELLOUT[ability] + " saving throw"


def hitpoints(num, size, conbonus):
    return diceroll(num, HIT_DIE_SIZE[size], conbonus * num)


def ac(dex, bonus, reason):
    ac_string = str(10 + dex + bonus)
    if reason != "":
        ac_string += " (" + reason + ")"
    return ac_string

def cr(cr):
    return str(cr) + " (" + CR_TO_XP[cr] + " XP)"


def score_to_bonus(score):
    return floor(score / 2) - 5


def ability_scores_to_bonuses(stats):
    bonusdict = {}
    for ability in stats:
        bonusdict[ability] = score_to_bonus(stats[ability])
    return bonusdict


def comma_separate(array):
    string = ""
    for item in array:
        if string != "":
            string += ", "
        string += str(item)
    return string


def skill_profs(skill_prof_list, stats, profbonus):
    skill_profs_dict = {}
    for skill in skill_prof_list:
        if skill in skill_profs_dict:
            skill_profs_dict[skill] += profbonus
        else:
            skill_profs_dict[skill] = stats[SKILL_ABILITY[skill]] + profbonus
    skill_profs_string = ""
    for skill in skill_profs_dict:
        if skill_profs_string != "":
            skill_profs_string += ", "
        bonus = skill_profs_dict[skill]
        skill_profs_string += SKILL_PRETTYNAME[skill] + " "
        if bonus >= 0:
            skill_profs_string += "+"
        skill_profs_string += str(bonus)
    return skill_profs_string


def save_profs(save_prof_list, stats, profbonus):
    save_profs_dict = {}
    for save in save_prof_list:
        if save in save_profs_dict:
            save_profs_dict[save] += profbonus
        else:
            save_profs_dict[save] = stats[save] + profbonus
    save_profs_string = ""
    for save in save_profs_dict:
        if save_profs_string != "":
            save_profs_string += ", "
        bonus = save_profs_dict[save]
        save_profs_string += save.capitalize() + " "
        if bonus >= 0:
            save_profs_string += "+"
        save_profs_string += str(bonus)
    return save_profs_string


def format_and_execute(field, stats):
    formatted_field = ""
    in_function_body = False
    arg_text = ""
    for char in field:
        if char == " ":
            if in_function_body:
                if arg_text in ABILITY_LIST:
                    arg_text = str(stats[arg_text])
                formatted_field += arg_text + ", "
                arg_text = ""
            else:
                formatted_field += "("
                in_function_body = True
        else:
            if in_function_body:
                arg_text += char
            else:
                formatted_field += char
    if arg_text in ABILITY_LIST:
        arg_text = str(stats[arg_text])
    return eval(formatted_field + arg_text + ")")


def resolve_functions(string, stats):
    updated_string = ""
    field = ""
    field_started = False
    for char in string:
        if char == "[":
            field_started = True
        elif char == "]":
            field_started = False
            updated_string += format_and_execute(field, stats)
            field = ""
        elif field_started:
            field += char
        else:
            updated_string += char
    return updated_string


def create_stat_table(scores, bonuses):
    table = "\\begin{footnotesize}\\noindent\\begin{tabular}{llllll}\\hline" + NEWLINE
    for ability in ABILITY_LIST:
        table += "\\textbf{" + ability.upper() + "}"
        if ability != "cha":
            table += "&"
    table += NEWLINE
    for ability in ABILITY_LIST:
        table += str(scores[ability]) + " ("
        bonus = bonuses[ability]
        if bonus >= 0:
            table += "+"
        table += str(bonus) + ")"
        if ability != "cha":
            table += "&"
    table += NEWLINE + NEWLINE + "\\hline\\end{tabular}\\end{footnotesize}"
    return table


def create_attack(attack, stats, profbonus):
    attack_string = "\\noindent\\textit{\\textbf{" + attack["name"] + ".} "
    if attack["type"] == "mwa":
        attack_string += "Melee Weapon Attack:} "
        bonus = stats[attack["ability"]] + profbonus
        if bonus >= 0:
            attack_string += "+"
        attack_string += str(bonus) + " to hit, reach " + str(attack["reach"]) + "ft., " + attack["target"] + "." + NEWLINE
    attack_string += "\\textit{Hit:} " + resolve_functions(attack["onhit"], stats)
    if "special" in attack:
        attack_string += NEWLINE + attack["special"]
    return attack_string


def dmg_attributes(attributes):
    standard_attributes = []
    special_attribute = ""
    for attr in attributes:
        if "," in attr:
            special_attribute = attr
        else:
            standard_attributes.append(attr)
    standard_attributes.sort()
    attribute_string = comma_separate(standard_attributes)
    if special_attribute != "":
        attribute_string += "; " + special_attribute
    return attribute_string


def create_monster(monster):
    monster_string = "\\subsection*{"
    if "headername" in monster:
        monster_string += monster["headername"]
    else:
        monster_string += monster["name"]
    monster_string += "}"
    if "flavor" in monster:
        monster_string += "\\textit{" + monster["flavor"] + "}" + NEWLINE + NEWLINE

    monster_string += "\\textbf{" + monster["name"].upper() + "}" + NEWLINE
    monster_string += "\\textit{" + (monster["size"] + " " + monster["type"] + ", " + monster["alignment"]).title() + "}" + NEWLINE

    scores = monster["stats"]
    bonuses = ability_scores_to_bonuses(scores)
    profbonus = cr_to_prof(monster["cr"])

    acbonus = 0
    acreason = ""
    if "ac" in monster:
        acbonus = monster["ac"][0]
        acreason = monster["ac"][1]
    monster_string += "\\textbf{Armor Class} " + ac(bonuses["dex"], acbonus, acreason) + NEWLINE

    monster_string += "\\textbf{Hit Points} " + hitpoints(monster["hd"], monster["size"], bonuses["con"]) + NEWLINE

    monster_string += "\\textbf{Speed} "
    for speed_type in monster["speed"]:
        if speed_type == "land":
            monster_string += str(monster["speed"][speed_type]) + " ft."
        else:
            monster_string += ", " + speed_type + " " + str(monster["speed"][speed_type]) + " ft."
    monster_string += NEWLINE

    monster_string += create_stat_table(scores, bonuses) + NEWLINE

    if "saves" in monster:
        monster_string += "\\textbf{Saving Throws} " + save_profs(monster["saves", bonuses, profbonus]) + NEWLINE

    if "skills" in monster:
        monster_string += "\\textbf{Skills} " + skill_profs(monster["skills"].sort(), bonuses, profbonus) + NEWLINE

    if "vulnerable" in monster:
        monster_string += "\\textbf{Damage Vulnerabilities} " + dmg_attributes(monster["vulnerable"]) + NEWLINE

    if "resist" in monster:
        monster_string += "\\textbf{Damage Resistances} " + dmg_attributes(monster["resist"]) + NEWLINE

    if "immune" in monster:
        monster_string += "\\textbf{Damage Immunities} " + dmg_attributes(monster["immune"]) + NEWLINE

    if "cond-immune" in monster:
        monster_string += "\\textbf{Condition Immunities} " + comma_separate(monster["cond-immune"]) + NEWLINE
    
    monster_string += "\\textbf{Senses} "
    if "senses" in monster:
        monster_string += monster["senses"] + ", "
    monster_string += "passive Perception " + str(10) + NEWLINE # this is a problem
    
    monster_string += "\\textbf{Languages "
    if "languages" in monster:
        monster_string += "}" + monster["languages"]
    else:
        monster_string += "---}"
    monster_string += NEWLINE

    monster_string += "\\textbf{Challenge} " + cr(monster["cr"])

    print(monster_string)


    
            

with open("monsters.yaml") as stream:
    try:
        filedict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#print(diceroll(2, 4, 1))
#print(hitpoints (10, "small", 1))
#print(save("str", 2, 2))
#print(format_and_execute("diceroll 2 4 str", {"str":2}))
#print(skill_profs(["athletics", "acrobatics", "acrobatics"], {"str":-3, "dex":1}, 2))
#print(save_profs(["str", "dex", "dex"], {"str":-3, "dex":1}, 2))
#print(score_to_bonus(10))

create_monster(filedict)

