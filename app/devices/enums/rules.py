from enum import Enum


class DiscreteActuatorsType(Enum):
    valve = "valve"
    switcher = "switcher"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class DiscreteStates:
    ON = 1
    OFF = 0


class RulesPossibleState:
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELED = "canceled"
