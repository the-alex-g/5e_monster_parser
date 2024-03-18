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
FULL_SPELLCASTER = [
    [2],
    [3],
    [4, 2],
    [4, 3],
    [4, 3, 2],
    [4, 3, 3],
    [4, 3, 3, 1],
    [4, 3, 3, 2],
    [4, 3, 3, 3, 1],
    [4, 3, 3, 3, 2],
    [4, 3, 3, 3, 2, 1],
    [4, 3, 3, 3, 2, 1],
    [4, 3, 3, 3, 2, 1, 1],
    [4, 3, 3, 3, 2, 1, 1],
    [4, 3, 3, 3, 2, 1, 1, 1],
    [4, 3, 3, 3, 2, 1, 1, 1],
    [4, 3, 3, 3, 2, 1, 1, 1, 1],
    [4, 3, 3, 3, 3, 1, 1, 1, 1],
    [4, 3, 3, 3, 3, 2, 1, 1, 1],
    [4, 3, 3, 3, 3, 2, 2, 1, 1],
]
SEMI_SPELLCASTER = [
    [],
    [2],
    [3],
    [3],
    [4, 2],
    [4, 2],
    [4, 3],
    [4, 3],
    [4, 3, 2],
    [4, 3, 2],
    [4, 3, 3],
    [4, 3, 3],
    [4, 3, 3, 1],
    [4, 3, 3, 1],
    [4, 3, 3, 2],
    [4, 3, 3, 2],
    [4, 3, 3, 3, 1],
    [4, 3, 3, 3, 1],
    [4, 3, 3, 3, 2],
    [4, 3, 3, 3, 2],
]
WARLOCK = [
    [1],
    [2],
    [0, 2],
    [0, 2],
    [0, 0, 2],
    [0, 0, 2],
    [0, 0, 0, 2],
    [0, 0, 0, 2],
    [0, 0, 0, 0, 2],
    [0, 0, 0, 0, 2],
    [0, 0, 0, 0, 3],
    [0, 0, 0, 0, 3],
    [0, 0, 0, 0, 3],
    [0, 0, 0, 0, 3],
    [0, 0, 0, 0, 3],
    [0, 0, 0, 0, 3],
    [0, 0, 0, 0, 4],
    [0, 0, 0, 0, 4],
    [0, 0, 0, 0, 4],
    [0, 0, 0, 0, 4],
]
SPELL_SLOTS = {
    "bard":FULL_SPELLCASTER,
    "cleric":FULL_SPELLCASTER,
    "druid":FULL_SPELLCASTER,
    "paladin":SEMI_SPELLCASTER,
    "ranger":SEMI_SPELLCASTER,
    "sorceror":FULL_SPELLCASTER,
    "warlock":WARLOCK,
    "wizard":FULL_SPELLCASTER
}
SPELLCASTING_ABILITY = {
    "bard":"cha",
    "cleric":"wis",
    "druid":"wis",
    "paladin":"cha",
    "ranger":"wis",
    "sorceror":"cha",
    "warlock":"cha",
    "wizard":"int"
}
PREBAKED_ABILITIES = [
    "Spider Climb",
    "Nimble Escape"
]
NEWLINE = "\\\\"
LINEBREAK = NEWLINE + "\\bigskip"
PREAMBLE = """\\documentclass[letterpaper, 12pt, twocolumn]{book}
\\usepackage{ragged2e}
\\usepackage[left=0.5in, right=0.5in, top=1in, bottom=1in]{geometry}
\\usepackage{graphicx}
\\def\\halfline{\\noindent\\makebox[\\columnwidth]{\\rule{3.7in}{0.4pt}}\\\\}
\\begin{document}\\RaggedRight"""
CONCLUSION = """\\end{document}"""
SOURCE_YAML_NAME = "monsters"


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


def format_index(index):
    if index == 1:
        return "1st"
    elif index == 2:
        return "2nd"
    elif index == 3:
        return "3rd"
    else:
        return str(index) + "th"


def save(ability, abilitybonus, profbonus):
    dc = 8 + abilitybonus + profbonus
    return "DC " + str(dc) + " " + ABILITIES_SPELLOUT[ability[2:]] + " saving throw"


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


def format_bonus(bonus):
    if bonus >= 0:
        return "+" + str(bonus)
    else:
        return str(bonus)


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
        skill_profs_string += format_bonus(bonus)
    return {"string":skill_profs_string, "dict":skill_profs_dict}


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
        save_profs_string += format_bonus(bonus)
    return save_profs_string


def format_and_execute(field, stats, profbonus):
    formatted_field = ""
    in_function_body = False
    arg_text = ""
    function_name = ""
    for char in field:
        if char == " ":
            if in_function_body:
                if arg_text in ABILITY_LIST:
                    arg_text = str(stats[arg_text])
                elif not arg_text.isdigit():
                    formatted_field += "\""
                    arg_text += "\""
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
                function_name += char
    if arg_text in ABILITY_LIST:
        arg_text = str(stats[arg_text])
    formatted_field += arg_text
    if function_name == "save":
        formatted_field += ", " + str(profbonus)
    return eval(formatted_field + ")")


def resolve_functions(string, stats, profbonus):
    updated_string = ""
    field = ""
    field_started = False
    for char in string:
        if char == "[":
            field_started = True
        elif char == "]":
            field_started = False
            updated_string += format_and_execute(field, stats, profbonus)
            field = ""
        elif field_started:
            field += char
        else:
            updated_string += char
    return updated_string


def create_stat_table(scores, bonuses):
    table = """\\smallskip
    \\begin{footnotesize}
    \\noindent
    \\resizebox{\\columnwidth}{!}{
    \\begin{tabular}{llllll}
    \\hline""" + NEWLINE
    for ability in ABILITY_LIST:
        table += "\\textbf{" + ability.upper() + "}"
        if ability != "cha":
            table += "&"
    table += NEWLINE
    for ability in ABILITY_LIST:
        table += str(scores[ability]) + " (" + format_bonus(bonuses[ability]) + ")"
        if ability != "cha":
            table += "&"
    table += NEWLINE + NEWLINE + """\\hline
    \\end{tabular}}
    \\end{footnotesize}
    \\smallskip"""
    return table


def create_attack(attack, stats, profbonus):
    attack_string = "\\noindent\\textit{\\textbf{" + attack["name"] + ".} "
    bonus = stats[attack["ability"]] + profbonus
    if "bonus" in attack:
        bonus += attack["bonus"]
    if attack["type"] == "mw":
        attack_string += "Melee Weapon Attack:} "
        attack_string += format_bonus(bonus) + " to hit, reach " + str(attack["reach"]) + " ft."
    elif attack["type"] == "rw":
        attack_string += "Ranged Weapon Attack:} "
        attack_string += format_bonus(bonus) + " to hit, range " + str(attack["reach"])
    elif attack["type"] == "ms":
        attack_string += "Melee Spell Attack:} "
        attack_string += format_bonus(bonus) + " to hit, reach " + str(attack["reach"]) + " ft."
    elif attack["type"] == "rw":
        attack_string += "Ranged Spell Attack:} "
        attack_string += format_bonus(bonus) + " to hit, range " + str(attack["reach"])
        
    attack_string += ", " + attack["target"] + "." + NEWLINE + "\\textit{Hit:} " + resolve_functions(attack["onhit"], stats, profbonus)
    if "special" in attack:
        attack_string += NEWLINE + resolve_functions(attack["special"], stats, profbonus)
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


def spellcasting(slot_type, level, spells, stats, profbonus, name):
    string = "\\textbf{\\textit{Spellcasting.}} "
    string += "The " + name.lower() + " is a " + format_index(level)
    string += "-level spellcaster. Its spellcasting ability is " + ABILITIES_SPELLOUT[SPELLCASTING_ABILITY[slot_type]]
    bonus = stats[SPELLCASTING_ABILITY[slot_type]] + profbonus
    string += " (spell save DC " + str(8 + bonus) + ", spell attack bonus " + format_bonus(bonus) + "). "
    string += "The " + name.lower() + " has the following spells prepared:" + NEWLINE
    string += "\\textbf{Cantrips:} \\textit{" + comma_separate(sorted(spells[0])) + "}"
    slots = SPELL_SLOTS[slot_type][level - 1]
    for i in range(0, len(slots)):
        slot_num = slots[i]
        string += NEWLINE + "\\textbf{" + format_index(i + 1) + " Level"
        if slot_num != 0:
            string += " (" + str(slot_num) + " slots)"
        string += ":} \\textit{"
        string += comma_separate(sorted(spells[i + 1])) + "}"
    return string


def possessive(name):
    if name[-1] == "s":
        return name + "'"
    else:
        return name + "'s"


def innate_spellcasting(ability, spells, stats, profbonus, name):
    string = "\\textbf{\\textit{Innate Spellcasting.}} "
    string += "The " + possessive(name.lower()) + " spellcasting ability is " + ABILITIES_SPELLOUT[ability]
    bonus = stats[ability] + profbonus
    string += " (spell save DC " + str(8 + bonus) + ", spell attack bonus " + format_bonus(bonus) + "). "
    string += "The " + name.lower() + " can cast the following spells, requiring no material components:"
    for category in spells:
        string += NEWLINE + "\\textbf{" + category["frequency"].title() + ":} \\textit{"
        string += comma_separate(sorted(category["spells"])) + "}"
    return string


def speeds(speed_dict):
    speed_string = str(speed_dict["land"]) + " ft."
    speed_type_list = sorted(speed_dict)
    for speed_type in speed_type_list:
        if speed_type != "land":
            if speed_type == "fly-hover":
                speed_string += ", fly " + str(speed_dict[speed_type]) + " ft. (hover)"
            else:
                speed_string += ", " + speed_type + " " + str(speed_dict[speed_type]) + " ft."
    return speed_string


def check_missing_fields(monster):
    error = False
    monster_name = ""
    if not "name" in monster:
        print("Unnamed monster!")
        error = True
    else:
        monster_name = monster["name"]
        if not "cr" in monster:
            print(monster_name + " does not have a CR")
            error = True
        if not "size" in monster:
            print(monster_name + " does not have a size")
            error = True
        if not "type" in monster:
            print(monster_name + " does not have a type")
            error = True
        if not "hd" in monster:
            print(monster_name + " does not have hit dice")
            error = True
        if not "speed" in monster:
            print(monster_name + " does not have a speed")
            error = True
        elif not "land" in monster["speed"]:
            print(monster_name + " does not have a land speed")
            error = True
        if not "stats" in monster:
            print(monster_name + " does not have ability scores")
            error = True
    return error


def get_baked_ability(ability_name, stats, profbonus, name):
    if ability_name == "Spider Climb":
        return "The " + name.lower() + " can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check."
    if ability_name == "Nimble Escape":
        return "The " + name.lower() + " can take the Disengage or Hide action as a bonus action on each of its turns."


def abilities(abilities, stats, profbonus, name):
    ability_string = ""
    ability_name_dict = {}
    for ability in abilities:
        ability_name_dict[ability["name"]] = ability
    for ability_name in sorted(ability_name_dict):
        ability = ability_name_dict[ability_name]
        ability_string += "\\textbf{\\textit{" + ability["name"] + ".}} "
        if ability_name in PREBAKED_ABILITIES:
            ability_string += get_baked_ability(ability_name, stats, profbonus, name) + LINEBREAK
        else:
            ability_string += resolve_functions(ability["effect"], stats, profbonus) + LINEBREAK
    return ability_string


def create_monster(monster):
    monster_string = "\\subsection*{"
    if "headername" in monster:
        monster_string += monster["headername"]
    else:
        monster_string += monster["name"]
    monster_string += "}"

    if "flavor" in monster:
        monster_string += "\\textit{" + monster["flavor"] + "}" + LINEBREAK

    if "description" in monster:
        for description in monster["description"]:
            monster_string += "\\textbf{\\textit{" + description["header"] + ".}} "
            monster_string += description["text"] + NEWLINE
        monster_string += "\\bigskip"

    monster_string += "\\textbf{" + monster["name"].upper() + "}" + NEWLINE
    alignment = "unaligned"
    if "alignment" in monster:
        alignment = monster["alignment"]        
    monster_string += "\\textit{" + (monster["size"] + " " + monster["type"]).title()
    if "tags" in monster:
        monster_string += " (" + comma_separate(sorted(monster["tags"])) + ")"
    monster_string +=  ", " + alignment.title() + "}" + NEWLINE

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

    monster_string += "\\textbf{Speed} " + speeds(monster["speed"]) + NEWLINE    

    monster_string += create_stat_table(scores, bonuses) + NEWLINE

    if "saves" in monster:
        monster_string += "\\textbf{Saving Throws} " + save_profs(monster["saves"], bonuses, profbonus) + NEWLINE

    skill_prof_dict = {}
    if "skills" in monster:
        skills = skill_profs(sorted(monster["skills"]), bonuses, profbonus)
        skill_prof_dict = skills["dict"]
        monster_string += "\\textbf{Skills} " + skills["string"] + NEWLINE

    if "vulnerable" in monster:
        monster_string += "\\textbf{Damage Vulnerabilities} " + dmg_attributes(monster["vulnerable"]) + NEWLINE

    if "resist" in monster:
        monster_string += "\\textbf{Damage Resistances} " + dmg_attributes(monster["resist"]) + NEWLINE

    if "immune" in monster:
        monster_string += "\\textbf{Damage Immunities} " + dmg_attributes(monster["immune"]) + NEWLINE

    if "cond-immune" in monster:
        monster_string += "\\textbf{Condition Immunities} " + comma_separate(sorted(monster["cond-immune"])) + NEWLINE
    
    monster_string += "\\textbf{Senses} "
    if "senses" in monster:
        monster_string += comma_separate(sorted(monster["senses"])) + ", "
    monster_string += "passive Perception "
    if "perception" in skill_prof_dict:
        monster_string += str(10 + skill_prof_dict["perception"])
    else:
        monster_string += str(10 + bonuses["wis"])
    monster_string += NEWLINE
    
    monster_string += "\\textbf{Languages "
    if "languages" in monster:
        monster_string += "}" + comma_separate(sorted(monster["languages"])).title()
    else:
        monster_string += "---}"
    monster_string += NEWLINE

    monster_string += "\\textbf{Challenge} " + cr(monster["cr"]) + LINEBREAK

    if "abilities" in monster:
        monster_string += abilities(monster["abilities"], bonuses, profbonus, monster["name"])

    if "innate-spellcasting" in monster:
        ability = monster["innate-spellcasting"]
        monster_string += innate_spellcasting(ability["ability"], ability["spells"], bonuses, profbonus, monster["name"])
        monster_string += LINEBREAK
    
    if "spellcasting" in monster:
        ability = monster["spellcasting"]
        monster_string += spellcasting(ability["type"], ability["level"], ability["spells"], bonuses, profbonus, monster["name"])
        monster_string += LINEBREAK
    
    if "attacks" in monster or "actions" in monster:
        monster_string += "\\textbf{Actions}" + NEWLINE + "\\halfline"

    monster_string += "\n%mabp\n"

    if "attacks" in monster:
        attack_name_dict = {}
        for attack in monster["attacks"]:
            attack_name_dict[attack["name"]] = attack
        for attack_name in sorted(attack_name_dict):
            monster_string += create_attack(attack_name_dict[attack_name], bonuses, profbonus) + LINEBREAK

    if "actions" in monster:
        action_name_dict = {}
        for action in monster["actions"]:
            if action["name"].lower() != "multiattack":
                action_name_dict[action["name"]] = action
            else:
                monster_string = monster_string.replace(
                    "%mabp",
                    "\\textbf{\\textit{Multiattack.}} " + resolve_functions(action["effect"], bonuses, profbonus) + LINEBREAK
                )
        for action_name in sorted(action_name_dict):
            action = action_name_dict[action_name]
            monster_string += "\\textbf{\\textit{" + action["name"] + ".}} "
            monster_string += resolve_functions(action["effect"], bonuses, profbonus) + LINEBREAK
            

    return monster_string


def create_doc(filedict):
    latexfile = open("monsters.tex", "w")
    latexfile.write(PREAMBLE)

    monster_name_dict = {}
    monsters_by_habitat = {}
    monsters_by_type = {}
    monsters_by_cr = {}
    for monster in filedict["monsters"]:
        if check_missing_fields(monster):
            continue
        monstername = ""
        if "headername" in monster:
            monstername = monster["headername"]
        else:
            monstername = monster["name"]
        if "habitat" in monster:
            for region in monster["habitat"]:
                if region in monsters_by_habitat:
                    monsters_by_habitat[region].append(monstername)
                else:
                    monsters_by_habitat[region] = [monstername]
        elif "any" in monsters_by_habitat:
            monsters_by_habitat["any"].append(monstername)
        else:
            monsters_by_habitat["any"] = [monstername]

        if monster["type"] in monsters_by_type:
            monsters_by_type[monster["type"]].append(monstername)
        else:
            monsters_by_type[monster["type"]] = [monstername]
        if monster["cr"] in monsters_by_cr:
            monsters_by_cr[monster["cr"]].append(monstername)
        else:
            monsters_by_cr[monster["cr"]] = [monstername]
        monster_name_dict[monstername] = monster

    for monster_name in sorted(monster_name_dict):
        print(monster_name)
        monster = monster_name_dict[monster_name]
        latexfile.write(create_monster(monster))
        latexfile.write("\\newpage")

    latexfile.write(CONCLUSION)
    latexfile.close()


with open(SOURCE_YAML_NAME + ".yaml") as stream:
    try:
        create_doc(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)

