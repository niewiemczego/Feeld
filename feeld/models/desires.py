from enum import Enum
from typing import Literal

DesiresRelationshipType = Literal[
    "CASUAL",
    "CELIBATE",
    "CONNECTION",
    "DATES",
    "ENM",
    "FRIENDSHIPS",
    "FUN",
    "FWB",
    "INTIMACY",
    "MONOGAMY",
    "OPEN_RELATIONSHIP",
    "POLY",
    "RELATIONSHIP",
]

DesiresGroupType = Literal[
    "COUPLES", "GROUP", "SINGLES", "THREESOME", "FF", "MM", "MF", "FFM", "MMF", "FFF", "MMM", "FFFF", "MMMM", "MFMF"
]

DesiresKinksType = Literal[
    "AFTERCARE",
    "BDSM",
    "BONDAGE",
    "BRAT",
    "BRAT_TAMER",
    "COMMUNICATION",
    "CUDDLING",
    "DOMINANTS",
    "EDGING",
    "EXPLORATION",
    "FLIRTING",
    "FOREPLAY",
    "GGG",
    "KINK",
    "KISSING",
    "MASSAGE",
    "PARTIES",
    "ROLE_PLAY",
    "ROUGH",
    "SENSUAL",
    "SUBMISSIVES",
    "SWITCH",
    "TEXTING",
    "TOYS",
    "WATCHING",
]

DesiresType = Literal[DesiresRelationshipType, DesiresGroupType, DesiresKinksType]


class DesiresRelationship(Enum):
    CASUAL = "Casual"
    CELIBATE = "Celibate"
    CONNECTION = "Connection"
    DATES = "Dates"
    ENM = "ENM"
    FRIENDSHIPS = "Friendships"
    FUN = "Fun"
    FWB = "FWB"
    INTIMACY = "Intimacy"
    MONOGAMY = "Monogamy"
    OPEN_RELATIONSHIP = "Open relationship"
    POLY = "Poly"
    RELATIONSHIP = "Relationship"


class DesiresGroup(Enum):
    COUPLES = "Couples"
    GROUP = "Group"
    SINGLES = "Singles"
    THREESOME = "Threeway"
    FF = "FF"
    MM = "MM"
    MF = "MF"
    FFM = "FFM"
    MMF = "MMF"
    FFF = "FFF"
    MMM = "MMM"
    FFFF = "FFFF"
    MMMM = "MMMM"
    MFMF = "MFMF"


class DesiresKinks(Enum):
    AFTERCARE = "Aftercare"
    BDSM = "BDSM"
    BONDAGE = "Bondage"
    BRAT = "Being a brat"
    BRAT_TAMER = "Being a brat tamer"
    COMMUNICATION = "Communication"
    CUDDLING = "Cuddling"
    DOMINANTS = "Being dominant"
    EDGING = "Edging"
    EXPLORATION = "Exploration"
    FLIRTING = "Flirting"
    FOREPLAY = "Foreplay"
    GGG = "GGG"
    KINK = "Kink"
    KISSING = "Kissing"
    MASSAGE = "Massage"
    PARTIES = "Parties"
    ROLE_PLAY = "Role Play"
    ROUGH = "Rough"
    SENSUAL = "Sensual"
    SUBMISSIVES = "Being submissive"
    SWITCH = "Being a switch"
    TEXTING = "Texting"
    TOYS = "Toys"
    WATCHING = "Watching"
