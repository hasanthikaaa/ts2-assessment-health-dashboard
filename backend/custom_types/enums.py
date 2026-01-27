from enum import Enum


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class BPStage(str, Enum):
    NORMAL = "Normal"
    ELEVATED = "Elevated"
    STAGE_1 = "Stage 1"
    STAGE_2 = "Stage 2"
    HYPERTENSIVE_CRISIS = "Hypertensive Crisis"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AgeBand(str, Enum):
    ZERO_TO_SEVENTEEN = "0-17"
    EIGHTEEN_TO_THIRTY_NINE = "18-39"
    FORTY_TO_SIXTY_FOUR = "40-64"
    SIXTY_FIVE_PLUS = "65+"
