import yaml
import os
import brand
from tables import *
from parser_utility import *

MULTIATTACK_SPLICE_KEY = "\n%multiattack-splice-key\n"
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

monsters_by_habitat = {}
monsters_by_type = {}
monsters_by_cr = {}


def entry(header, body):
    return "\\entry{" + header + "}{" + body + "}"


def hitpoints(num, size, conbonus):
    return brand.diceroll(num, HIT_DIE_SIZE[size], conbonus * num)


def partition(title):
    return "\\textbf{" + title + "}" + NEWLINE + "\\halfline "


def ac(dex, bonus, reason):
    ac_string = str(10 + dex + bonus)
    if reason != "":
        ac_string += " (" + reason + ")"
    return ac_string


def cr(cr):
    return str(cr) + " (" + CR_TO_XP[cr] + " XP)"


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


def create_attack(attack, stats, params):
    attack_string = "\\entry{" + attack["name"] + "}{\\textit{"
    bonus = stats[attack["ability"]] + params["profbonus"]
    if "bonus" in attack:
        bonus += attack["bonus"]
    if attack["type"] == "mw":
        attack_string += "Melee Weapon Attack:} "
        attack_string += format_bonus(bonus) + " to hit, reach " + str(get_key_if_exists(attack, "reach", 5)) + " ft."
    elif attack["type"] == "rw":
        attack_string += "Ranged Weapon Attack:} "
        attack_string += format_bonus(bonus) + " to hit, range " + str(attack["range"]) + " ft."
    elif attack["type"] == "ms":
        attack_string += "Melee Spell Attack:} "
        attack_string += format_bonus(bonus) + " to hit, reach " + str(get_key_if_exists(attack, "reach", 5)) + " ft."
    elif attack["type"] == "rs":
        attack_string += "Ranged Spell Attack:} "
        attack_string += format_bonus(bonus) + " to hit, range " + str(attack["range"]) + " ft."
    else:
        print("ERROR: Unknown attack type \"" + attack["type"] + "\"")
        
    attack_string += ", " + get_key_if_exists(attack, "target", "one target") + "." + NEWLINE + "\\textit{Hit:} "
    attack_string += brand.parse_string(attack["onhit"], stats, params)
    if "special" in attack:
        attack_string += NEWLINE + brand.parse_string(attack["special"], stats, params)
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
        default_immunities = DEFAULT_IMMUNITIES[creature_type].copy()
    for immunity in immunities:
        if immunity[0:1] == "n/":
            if immunity[2:] in default_immunities:
                default_immunities.erase(immunity[2:])
        else:
            default_immunities.append(immunity)
    return comma_separate(sorted(default_immunities))


def spellcasting(slot_type, level, spells, stats, profbonus, name):
    string = "\\entry{Spellcasting}{"
    string += "The " + name + " is a " + format_index(level)
    string += "-level spellcaster. Its spellcasting ability is " + ABILITIES_SPELLOUT[SPELLCASTING_ABILITY[slot_type]]
    bonus = stats[SPELLCASTING_ABILITY[slot_type]] + profbonus
    string += " (spell save DC " + str(8 + bonus) + ", spell attack bonus " + format_bonus(bonus) + "). "
    string += "The " + name + " has the following spells prepared:" + NEWLINE
    string += "\\textbf{Cantrips:} " + brand.spell(comma_separate(sorted(spells[0])))
    slots = SPELL_SLOTS[slot_type][level - 1]
    for i in range(0, len(slots)):
        slot_num = slots[i]
        string += NEWLINE + "\\textbf{" + format_index(i + 1) + " Level"
        if slot_num != 0:
            string += " (" + str(slot_num) + " slots)"
        string += ":} " + brand.spell(comma_separate(sorted(spells[i + 1])))
    return string + "}"



def innate_spellcasting(ability, spells, stats, profbonus, name):
    string = "\\entry{Innate Spellcasting}{"
    string += "The " + possessive(name) + " spellcasting ability is " + ABILITIES_SPELLOUT[ability]
    bonus = stats[ability] + profbonus
    string += " (spell save DC " + str(8 + bonus) + ", spell attack bonus " + format_bonus(bonus) + "). "
    string += "The " + name + " can cast the following spells, requiring no material components:"
    for category in spells:
        string += NEWLINE + "\\textbf{" + category["frequency"].title() + ":} " + brand.spell(comma_separate(sorted(category["spells"])))
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
        print("ERROR: " + "Unnamed monster!")
        error = True
    else:
        monster_name = monster["name"]
        print(monster_name)
        if not "cr" in monster:
            print("ERROR: " + monster_name + " does not have a CR")
            error = True
        if not "size" in monster:
            print("ERROR: " + monster_name + " does not have a size")
            error = True
        if not "type" in monster:
            print("ERROR: " + monster_name + " does not have a type")
            error = True
        if not "hd" in monster:
            print("ERROR: " + monster_name + " does not have hit dice")
            error = True
        if not "speed" in monster:
            print("ERROR: " + monster_name + " does not have a speed")
            error = True
        elif not "land" in monster["speed"]:
            print("ERROR: " + monster_name + " does not have a land speed")
            error = True
        if not "stats" in monster:
            print("ERROR: " + monster_name + " does not have ability scores")
            error = True
    return error


def format_actions(actions, stats, params, key="effect"):
    action_string = ""
    action_name_dict = {}
    for action in actions:
        action_name_dict[action["name"]] = action
    for action_name in sorted(action_name_dict):
        action = action_name_dict[action_name]
        if action_name in PREBAKED_ABILITIES and not key in action:
            action[key] = PREBAKED_ABILITIES[action_name]
        if "uses" in action:
            action_name += " (" + action["uses"].title() + ")"
        # the "cost" clause is for legendary actions
        elif "cost" in action:
            action_name += " (Costs " + str(action["cost"]) + " Actions)"
        action_string += entry(action_name, brand.parse_string(action[key], stats, params)) + LINEBREAK
    return action_string


def abilities(abilities, stats, params):
    return format_actions(abilities, stats, params)


def variants(diffs, stats, params):
    return partition("Variants") + format_actions(diffs, stats, params, key="mods")


def description(descriptions, monster_type, name, include_default=True):
    string = ""
    for description in descriptions:
        string += entry(description["header"], description["text"])
    if monster_type in NATURES and include_default:
        description = NATURES[monster_type].copy()
        description["text"] = brand.parse_string(description["text"], {}, blank_params(name))
        string += entry(description["header"], description["text"])
    return string


def legendary_actions(actions, stats, params):
    string = partition("Legendary Actions") + "The " + params["name"] + " can take "
    if "uses" in actions:
        string += str(actions["uses"])
        actions = actions["actions"]
    else:
        string += "3"
    string += """ legendary actions, choosing from the options below. Only one legendary action option can
be used at a time, and only at the end of another creature's turn. The """ + params["name"] + """ regains spent
legendary actions at the start of its turn.""" + NEWLINE + LINEBREAK
    return string + format_actions(actions, stats, params)


def lair_actions(actions, params, stats={}):
    string = partition("Lair Actions") + """On initiative count 20 (losing initiative ties),
the """ + params["name"] + " can take one of the following lair actions. The " + params["name"] + """ can't
take the same lair action two rounds in a row:""" + NEWLINE + LINEBREAK
    return string + format_actions(actions, stats, params)


def create_regional_effects(effects, death_effect, params, stats={}):
    string = partition("Regional Effects") + "The region containing a legendary "
    string += possessive(params["name"]) + " lair is warped by the " + possessive(params["name"]) + """ magic,
creating one or more of the following effects:""" + NEWLINE + LINEBREAK
    string += format_actions(effects, stats, params) + " "
    string += brand.parse_string(death_effect, stats, params)
    return string


def lair(lair, params, stats={}):
    string = "\\subsection*{" + brand.articulate(True, possessive(params["name"])) + " Lair}"
    if "description" in lair:
        string += lair["description"] + NEWLINE + LINEBREAK
    if "actions" in lair:
        string += lair_actions(lair["actions"], params)
    if "regional-effects" in lair:
        regional_effects = lair["regional-effects"]
        string += create_regional_effects(regional_effects["effects"], regional_effects["ondeath"], params)

    return string


def reactions(actions, stats, params):
    return partition("Reactions") + format_actions(actions, stats, params)


def create_header(name, title=True, mark=True, label=True, addtoc=True):
    header = ""
    if label:
        header += "\\label{" + name + "}"
    if mark:
        header += "\\markboth{" + name + "}{" + name + "}"
    if addtoc:
        header += "\\addcontentsline{toc}{subsection}{" + name + "}"
    if title:
        header += "\\section*{" + name + "}\\halfline" + LINEBREAK
    return header


def create_monster(monster, title=True, mark=True, addtoc=True):
    if check_missing_fields(monster):
        return ""
    monster_string = ""
    header_name = headername(monster)
    short_name = shortname(monster)
    plainname = monster["name"]

    scores = monster["stats"]
    bonuses = ability_scores_to_bonuses(scores)
    profbonus = cr_to_prof(monster["cr"])

    params = {"name":short_name, "profbonus":profbonus}

    if "params" in monster:
        for param in monster["params"]:
            params[param] = monster["params"][param]
    monster_string += create_header(header_name, title=title, mark=mark, addtoc=addtoc)

    if "flavor" in monster:
        monster_string += "\\textit{" + monster["flavor"] + "}" + NEWLINE + LINEBREAK

    if "description" in monster:
        monster_string += description(monster["description"], monster["type"], plainname) + LINEBREAK

    monster_string += "\\textbf{" + plainname.upper() + "}" + NEWLINE
    alignment = "unaligned"
    if "alignment" in monster:
        alignment = monster["alignment"]
    if "swarm" in monster:
        monster_string += "\\textit{" + monster["size"].title() + " Swarm of " + (monster["swarm"] + " " + monster["type"]).title() + "s"
        swarm_ability = PREBAKED_ABILITIES["Swarm"].replace("[name]", short_name).replace("[swarmsize]", monster["swarm"].title())
        if "abilities" in monster:
            swarm_override = False
            for ability in monster["abilities"]:
                if ability["name"] == "Swarm":
                    swarm_override = True
                    break
            if not swarm_override:
                monster["abilities"].append({"name":"Swarm", "effect":swarm_ability})
        else:
            monster["abilities"] = [swarm_ability]
    else:
        monster_string += "\\textit{" + (monster["size"] + " " + monster["type"]).title()
    if "tags" in monster:
        monster_string += " (" + comma_separate(sorted(monster["tags"])) + ")"
    monster_string +=  ", " + alignment.title() + "}" + NEWLINE

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
        monster_string += comma_separate(sorted(monster["senses"])) + ", passive Perception "
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
        monster_string += abilities(monster["abilities"], bonuses, params)

    if "innate-spellcasting" in monster:
        ability = monster["innate-spellcasting"]
        monster_string += innate_spellcasting(ability["ability"], ability["spells"], bonuses, profbonus, short_name)
        monster_string += LINEBREAK
    
    if "spellcasting" in monster:
        ability = monster["spellcasting"]
        monster_string += spellcasting(ability["type"], ability["level"], ability["spells"], bonuses, profbonus, short_name)
        monster_string += LINEBREAK
    
    if "attacks" in monster or "actions" in monster:
        monster_string += partition("Actions") + MULTIATTACK_SPLICE_KEY

    if "attacks" in monster:
        attack_name_dict = {}
        for attack in monster["attacks"]:
            attack_name_dict[attack["name"]] = attack
        for attack_name in sorted(attack_name_dict):
            monster_string += create_attack(attack_name_dict[attack_name], bonuses, params) + LINEBREAK

    if "actions" in monster:
        action_name_dict = {}
        for action in monster["actions"]:
            if action["name"] == "Multiattack":
                monster_string = monster_string.replace(
                    MULTIATTACK_SPLICE_KEY,
                    format_actions([action], bonuses, params)
                )
                monster["actions"].remove(action)
                break
        monster_string += format_actions(monster["actions"], bonuses, params)

    if "reactions" in monster:
        monster_string += reactions(monster["reactions"], bonuses, params)
    
    if "legendary-actions" in monster:
        monster_string += legendary_actions(monster["legendary-actions"], bonuses, params)
    
    if "variants" in monster:
        monster_string += variants(monster["variants"], bonuses, params)

    if "lair" in monster:
        monster_string += lair(monster["lair"], params, stats=bonuses)
    
    add_to_appendices(monster)
    return monster_string


def add_to_appendices(monster):
    monstername = headername(monster)
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

    monster_plural = MONSTER_TYPE_PLURALS[monster["type"]]
    if monster_plural in monsters_by_type:
        monsters_by_type[monster_plural].append(monstername)
    else:
        monsters_by_type[monster_plural] = [monstername]
    monster_cr = cr_to_digit(monster["cr"])
    if monster_cr in monsters_by_cr:
        monsters_by_cr[monster_cr].append(monstername)
    else:
        monsters_by_cr[monster_cr] = [monstername]


def resolve_group(group, monsters):
    mark = group["headers"]["mark"]
    addtoc = group["headers"]["toc"]
    title = "title" in group["headers"] and group["headers"]["title"] == "monster"
    group_string = create_header(headername(group), mark=mark=="group", label=False, addtoc=addtoc=="group")
    if "flavor" in group:
        group_string += "\\textit{" + group["flavor"] + "}" + NEWLINE + LINEBREAK

    if "description" in group:
        group_type = ""
        group_shortname = shortname(group)
        if "type" in group:
            group_type = group["type"]
        group_string += description(group["description"], group_type, group_shortname, include_default=not title) + LINEBREAK

    monster_dict = {}
    if "sorttype" in group:
        if group["sorttype"] == "alphabetical":
            for monster in monsters:
                monster_dict[headername(monster)] = monster
        elif group["sorttype"] == "index":
            for monster in monsters:
                if monster["sortindex"] in monster_dict:
                    print("ERROR: Duplicate indicies in group " + group["name"])
                else:
                    monster_dict[monster["sortindex"]] = monster
    
    for index in sorted(monster_dict):
        monster = monster_dict[index]
        # Copy group attributes to monster
        for field in group:
            if not field in GROUP_ATTRIBUTES_NOT_TO_COPY:
                if type(group[field]) == list:
                    for item in group[field]:
                        if field in monster:
                            if type(item) == dict:
                                if "n/" + item["name"] in monster[field]:
                                    monster[field].remove("n/" + item["name"])
                                    continue
                            elif type(item) == str:
                                if "n/" + item in monster[field]:
                                    monster[field].remove("n/" + item)
                                    continue
                            monster[field].append(item)
                        else:
                            monster[field] = [item]

                elif type(group[field]) == str:
                    if not field in monster:
                        monster[field] = group[field]
        
        group_string += create_monster(monster, title=title, mark=mark=="monster", addtoc=addtoc=="monster") + LINEBREAK

    if "lair" in group:
        group_string += lair(group["lair"], blank_params(group["name"]))
    
    return group_string


def create_appendix_table(table):
    string = ""
    for section in sorted(table):
        section_name = section
        if type(section) != str:
            # assume it's a CR table
            section_name = "Challenge " + cr_to_string(section)
        string += "\\textbf{" + section_name.title() + "}" + NEWLINE + "\\begin{tabular*}{\\columnwidth}{@{\\extracolsep{\\fill}} lc}"
        for entry in table[section]:
            string += entry + "&p.\\pageref{" + entry + "}" + NEWLINE
        string += "\\end{tabular*}" + NEWLINE + LINEBREAK
    return string


def open_yaml(filepath):
    with open(filepath) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc, " in file ", filepath)


def get_yaml_from_directory(dirname):
    yaml_list = []
    if os.path.isdir(dirname):
        for item in os.listdir(dirname):
            path = os.path.join(dirname, item)
            if os.path.isfile(path):
                yaml_list.append(open_yaml(path))
            elif os.path.isdir(path):
                for yaml_dir in get_yaml_from_directory(path):
                    yaml_list.append(yaml_dir)
    return yaml_list


def create_alphabetic_header(letter):
    return "\\addcontentsline{toc}{section}{" + letter + "}"


def create_doc():
    latexfile = open("monsters.tex", "w")
    latexfile.write(PREAMBLE)

    monster_name_dict = {}
    group_name_map = {}
    for group in get_yaml_from_directory("groups"):
        monster_name_dict[headername(group)] = [group]
        group_name_map[group["name"]] = headername(group)
    
    for monster in get_yaml_from_directory("monsters"):
        monstername = headername(monster)
        if "group" in monster:
            monster_name_dict[group_name_map[monster["group"]]].append(monster)
        else:
            monster_name_dict[monstername] = monster

    current_alphabet_letter = "A"
    latexfile.write(create_alphabetic_header("A"))
    for monster_name in sorted(monster_name_dict):
        if monster_name[0] != current_alphabet_letter:
            current_alphabet_letter = monster_name[0]
            latexfile.write(create_alphabetic_header(current_alphabet_letter))
        if type(monster_name_dict[monster_name]) == list:
            group = monster_name_dict[monster_name]
            latexfile.write(resolve_group(group[0], group[1:]) + PAGEBREAK)
            continue
        monster = monster_name_dict[monster_name]
        latexfile.write(create_monster(monster) + PAGEBREAK)
        
    latexfile.write("\\markboth{Appendicies}{Appendicies}")
    latexfile.write(create_appendix_table(monsters_by_cr) + PAGEBREAK)
    latexfile.write(create_appendix_table(monsters_by_habitat) + PAGEBREAK)
    latexfile.write(create_appendix_table(monsters_by_type) + PAGEBREAK)
    latexfile.write(CONCLUSION)
    latexfile.close()


create_doc()
