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
DEFAULT_IMMUNITIES = {
    "elemental":[
        "exhaustion",
        "paralyzed",
        "petrified",
        "poisoned",
        "unconcious"
    ],
    "plant":[
        "exhaustion",
        "blinded",
        "deafened",
    ],
    "fiend":[
        "poisoned",
        "exhaustion",
    ],
    "ooze":[
        "blinded",
        "deafened",
        "exhaustion",
        "prone",
    ],
    "construct":[
        "charmed",
        "frightened",
        "exhaustion",
        "paralyzed",
        "petrified",
        "poisoned"
    ],
    "undead":[
        "exhaustion",
        "poisoned"
    ]
}
NATURES = {
    "elemental":{
        "header":"Elemental Nature",
        "text":"[articulate True [name]] does not require air, food, drink, or sleep."
    },
    "undead":{
        "header":"Undead Nature",
        "text":"[articulate True [name]] does not require air, food, drink, or sleep."
    },
    "construct":{
        "header":"Constructed Nature",
        "text":"[articulate True [name]] does not require air, food, drink, or sleep."
    },
    "fiend":{
        "header":"Fiendish Nature",
        "text":"[articulate True [name]] does not require air, food, drink, or sleep."
    },
    "celestial":{
        "header":"Celestial Nature",
        "text":"[articulate True [name]] does not require air, food, drink, or sleep."
    },
    "ooze":{
        "header":"Ooze",
        "text":"[articulate True [name]] does not require air or sleep."
    },
    "plant":{
        "header":"Plant",
        "text":"[articulate True [name]] does not require sleep."
    }
}
MONSTER_TYPE_PLURALS = {
    "elemental":"elementals",
    "undead":"undead",
    "construct":"constructs",
    "fiend":"fiends",
    "celestial":"celestials",
    "ooze":"oozes",
    "plant":"plants",
    "humanoid":"humanoids",
    "giant":"giants",
    "monstrosity":"monstrosities",
    "fey":"fey",
    "dragon":"dragons",
    "aberration":"aberrations",
    "beast":"beasts",
}
PREBAKED_ABILITIES = {
    "Spider Climb":"The [name] can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check.",
    "Nimble Escape":"The [name] can take the Disengage or Hide action as a bonus action on each of its turns.",
    "Sunlight Sensitivity":"While in sunlight, the [name] has disadvantage on attack rolls, as well as on Wisdom (Perception) checks that rely on sight.",
    "Legendary Resistance":"If the [name] fails a saving throw, it can choose to succeed instead.",
    "Avoidance":"If the [name] is subject to an effect that allows it to make a Dexterity saving throw to take only half damage, it instead takes no damage if it succeeds on the saving throw, and only half damage if it fails.",
    "Frightful Presence":"Each creature of the [possessive [name]] choice that is within 120 feet and aware of it must succeed on a [save w/wis cha] or become frightened for 1 minute. A creature repeats the saving throw at the end of each of its turns, ending the effect on itself on a success. If the creature's saving throw is successful or the effect ends for it, the creature is immune to the [possessive [name]] Frightful Presence for the next 24 hours.",
    "Earthwalk":"The [name] can walk through unworked earth as if it were air, leaving no trace of its passage.",
    "Siege Monster":"The [name] deals double damage to structures.",
    "Swarm":"The [name] can fit through any gap large enough for a [swarmsize] creature, cannot regain hit points or gain temporary hit points, takes twice as much damage from area-of-effect sources, can enter the spaces of other creatures, and other creatures can enter the swarm's space.",
    "Rooted":"The [name] has advantage on saving throws made to resist being moved or knocked prone.",
    "Stench":"Any creature other than [articulate False [name]] that starts its turn within 5 feet of the [name] must succeed on a [save w/con con], being poisoned until the start of the creature's next turn. On a successful saving throw, the creature is immune to the stench of all [name]s for 1 hour.",
    "Amphibious":"The [name] can breathe both air and water with equal ease.",
    "Aquatic":"The [name] can only breathe underwater.",
    "Pack Tactics":"The [name] has advantage on an attack roll against a creature if at least one of the [possessive [name]] allies is within 5 feet of the creature and the ally isn't incapacitated.",
    "Magic Resistance":"The [name] has advantage on saving throws to resist spells and other magical effects.",
    "Immutable Form":"The [name] is immune to spells and other effects that would alter its form.",
    "Parry":"The [name] adds [profbonus] to its AC against one melee attack that would hit it. In order to do so, the [name] must see the attacker and be wielding a weapon.",
    "Web Sense":"While in contact with a web, the [name] knows the exact location of any other creature in contact with the same web.",
    "Web Walker":"The [name] ignores movement restrictions caused by webbing.",
    "Damage Transfer":"While the [name] is attached to a creature, it takes half damage from all attacks directed against it, and the creature it is attached to takes the other half.",
    "Amorphous":"The [name] can move through a space as narrow as 1 inch wide without squeezing.",
}
GROUP_ATTRIBUTES_NOT_TO_COPY = ["name", "sorttype", "flavor", "description", "include-monster-headers", "lair"]
