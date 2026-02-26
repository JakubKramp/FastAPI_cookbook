import enum
from dataclasses import dataclass


class SexEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"


class ActivityFactor(str, enum.Enum):
    little = "Little/no exercise"
    one_time = "Exercise 1-2 times/week"
    two_times = "Exercise 2-3 times/week"
    three_times = "Exercise 3-5 times/week"
    every_day = "Exercise 6-7 times/week"
    professional_athlete = "Professional athlete"

@dataclass
class Range:
    low: int
    high: int

    @property
    def label(self) -> str:
        return f"{self.low}-{self.high} years"

    def __contains__(self, value: int) -> bool:
        return self.low <= value <= self.high


RANGES = [
    Range(1, 3),
    Range(4, 8),
    Range(9, 13),
    Range(14, 18),
    Range(19, 50),
    Range(51, 70),
]

