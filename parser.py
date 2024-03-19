import yaml
from tables import *
from math import floor

NEWLINE = "\\\\"
LINEBREAK = "\\bigskip"
PAGEBREAK = "\n\\clearpage\n"
PREAMBLE = """\\documentclass[letterpaper, 12pt, twocolumn]{book}
\\usepackage{ragged2e}
\\usepackage[left=0.5in, right=0.5in, top=1in, bottom=1in]{geometry}
\\usepackage{graphicx}
\\def\\halfline{\\makebox[\\columnwidth]{\\rule{3.7in}{0.4pt}}\\\\}
\\def\\entry#1#2{\\textit{\\textbf{#1.}} #2\\\\}
\\begin{document}\\RaggedRight\\tableofcontents"""
CONCLUSION = """\\end{document}"""
SOURCE_YAML_NAME = "monsters"


def entry(header, body):
    return "\\entry{" + header + "}{" + body + "}"


def cr_to_prof(cr):
    if type(cr) == str:
        return 2
    else:
        return max(2, floor((cr - 1) / 4) + 2)


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
    attack_string = "\\entry{" + attack["name"] + "}{\\textit{"
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
    return attack_string + "}"


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


def cond_immunities(immunities, creature_type):
    default_immunities = []
    if creature_type in DEFAULT_IMMUNITIES:
        default_immunities = DEFAULT_IMMUNITIES[creature_type]
    for immunity in immunities:
        if immunity[0:1] == "n/":
            if immunity[2:] in default_immunities:
                default_immunities.erase(immunity[2:])
        else:
            default_immunities.append(immunity)
    return comma_separate(sorted(default_immunities))


def spellcasting(slot_type, level, spells, stats, profbonus, name):
    string = "\\entry{Spellcasting}{"
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
    return string + "}"


def possessive(name):
    if name[-1] == "s":
        return name + "'"
    else:
        return name + "'s"


def innate_spellcasting(ability, spells, stats, profbonus, name):
    string = "\\entry{Innate Spellcasting}{"
    string += "The " + possessive(name.lower()) + " spellcasting ability is " + ABILITIES_SPELLOUT[ability]
    bonus = stats[ability] + profbonus
    string += " (spell save DC " + str(8 + bonus) + ", spell attack bonus " + format_bonus(bonus) + "). "
    string += "The " + name.lower() + " can cast the following spells, requiring no material components:"
    for category in spells:
        string += NEWLINE + "\\textbf{" + category["frequency"].title() + ":} \\textit{"
        string += comma_separate(sorted(category["spells"])) + "}"
    return string + "}"


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


def format_actions(actions, name, stats, profbonus):
    action_string = ""
    action_name_dict = {}
    for action in actions:
        action_name_dict[action["name"]] = action
    for action_name in sorted(action_name_dict):
        action = action_name_dict[action_name]
        action_string += "\\entry{" + action["name"]
        if "uses" in action:
            action_string += " (" + action["uses"].title() + ")"
        # the "cost" clause is for legendary actions
        elif "cost" in action:
            action_string += " (Costs " + str(action["cost"]) + " Actions)"
        action_string += "}{"
        if action_name in PREBAKED_ABILITIES:
            raw_action = PREBAKED_ABILITIES[action_name]
            raw_action = raw_action.replace("[name]", name.lower())
            action_string += raw_action + "}"
        else:
            action_string += resolve_functions(action["effect"], stats, profbonus) + "}"
        action_string += LINEBREAK
    return action_string


def abilities(abilities, stats, profbonus, name):
    return format_actions(abilities, name, stats, profbonus)


def description(descriptions, monster_type, name):
    string = ""
    for description in descriptions:
        string += "\\entry{" + description["header"] + "}{" + description["text"] + "}"
    if monster_type in NATURES:
        description = NATURES[monster_type]
        description["text"] = description["text"].replace("[name]", name.lower())
        string += entry(description["header"], description["text"])
    return string


def legendary_actions(actions, name, stats, profbonus):
    string = "\\textbf{Legendary Actions}" + NEWLINE + "\\halfline The " + name.lower() + " can take "
    if "uses" in actions:
        string += str(actions["uses"])
        actions = actions["actions"]
    else:
        string += "3"
    string += """ legendary actions, choosing from the options below. Only one legendary action option can
be used at a time, and only at the end of another creature's turn. The """ + name.lower() + """ regains spent
legendary actions at the start of its turn.""" + NEWLINE + LINEBREAK
    return string + format_actions(actions, name, stats, profbonus)


def reactions(actions, name, stats, profbonus):
    string = "\\textbf{Reactions}" + NEWLINE + "\\halfline"
    return string + format_actions(actions, name, stats, profbonus)
        

def create_monster(monster, in_group=False):
    monster_string = ""
    if not in_group:
        monster_string = "\\section*{"
        header_name = ""
        if "headername" in monster:
            monster_string += monster["headername"] + "}"
            header_name = monster["headername"]
        else:
            monster_string += monster["name"] + "}"
            header_name = monster["name"]
        monster_string += "\\markboth{" + header_name + "}{" + header_name + "}"
        monster_string += "\\addcontentsline{toc}{subsection}{" + header_name + "}"

    if "flavor" in monster:
        monster_string += "\\textit{" + monster["flavor"] + "}" + NEWLINE + LINEBREAK

    if "description" in monster:
        monster_string += description(monster["description"], monster["type"], monster["name"]) + LINEBREAK

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
        monster_string += "\\textbf{Condition Immunities} "
        monster_string += cond_immunities(monster["cond-immune"], monster["type"]) + NEWLINE
    elif monster["type"] in DEFAULT_IMMUNITIES:
        monster_string += "\\textbf{Condition Immunities} "
        monster_string += cond_immunities([], monster["type"]) + NEWLINE

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

    monster_string += "\\textbf{Challenge} " + cr(monster["cr"]) + NEWLINE + LINEBREAK

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
        monster_string += "\\textbf{Actions}" + NEWLINE + "\\halfline\n%mabp\n"

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
                    entry("Multiattack", resolve_functions(action["effect"], bonuses, profbonus)) + LINEBREAK
                )
        for action_name in sorted(action_name_dict):
            action = action_name_dict[action_name]
            if action_name in PREBAKED_ABILITIES:
                raw_action = PREBAKED_ABILITIES[action_name]
                raw_action = raw_action.replace("[name]", monster["name"].lower())
                action["effect"] = raw_action
            monster_string += entry(action["name"], resolve_functions(action["effect"], bonuses, profbonus)) + LINEBREAK

    if "reactions" in monster:
        monster_string += reactions(monster["reactions"], monster["name"], bonuses, profbonus) + LINEBREAK
    
    if "legendary-actions" in monster:
        monster_string += legendary_actions(monster["legendary-actions"], monster["name"], bonuses, profbonus)
    
    return monster_string


def resolve_group(group, monsters):
    group_string = "\\section*{" + group["name"] + "}\\markboth{" + group["name"] + "}{" + group["name"] + "}"
    group_string += "\\addcontentsline{toc}{subsection}{" + group["name"] + "}"
    if "flavor" in group:
        group_string += "\\textit{" + group["flavor"] + "}" + NEWLINE + LINEBREAK

    if "description" in group:
        group_type = ""
        group_shortname = group["name"]
        if "type" in group:
            group_type = group["type"]
        if "shortname" in group:
            group_shortname = group["shortname"]
        group_string += description(group["description"], group_type, group_shortname) + LINEBREAK

    for monster in monsters:
        print(monster["name"])
        group_string += create_monster(monster, in_group=True) + LINEBREAK
    
    return group_string


def create_appendix_table():
    string = "\\begin{tabular*}{\\columnwidth}{@{\\extracolsep{\\fill}} clc}
    string += "\\textbf{CR} & \\textbf{Name} & \\textbf{Page} \\
    return string + "\\end{tabular*}"


def create_doc(filedict):
    latexfile = open("monsters.tex", "w")
    latexfile.write(PREAMBLE)

    monster_name_dict = {}
    monsters_by_habitat = {}
    monsters_by_type = {}
    monsters_by_cr = {}
    if "groups" in filedict:
        for group in filedict["groups"]:
            monster_name_dict[group["name"]] = [group]
    for monster in filedict["monsters"]:
        if check_missing_fields(monster):
            continue
        monstername = ""
        if "headername" in monster:
            monstername = monster["headername"]
        else:
            monstername = monster["name"]
        if "group" in monster:
            monster_name_dict[monster["group"]].append(monster)
        else:
            monster_name_dict[monstername] = monster

    for monster_name in sorted(monster_name_dict):
        if type(monster_name_dict[monster_name]) == list:
            group = monster_name_dict[monster_name]
            latexfile.write(resolve_group(group[0], group[1:]) + PAGEBREAK)
            continue
        print(monster_name)
        monster = monster_name_dict[monster_name]
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
        latexfile.write(create_monster(monster) + PAGEBREAK)

    latexfile.write(CONCLUSION)
    latexfile.close()


with open(SOURCE_YAML_NAME + ".yaml") as stream:
    try:
        create_doc(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
