import enum


Sex = [("male", "Male"), ("female", "Female")]


class ActivityFactor(str, enum.Enum):
    little = "Little/no exercise"
    one_time = "Exercise 1-2 times a week"
    two_times = "Exercise 2-3 times a week"
    three_times = "Exercise 3-5 times a week"
    every_day = "Exercise 6-7 times a week"
    professional_athlete = "Professional Athlete"
