from enum import Enum


class DiscreteActuatorsType(Enum):
    irrigation = 'irrigation'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class DiscreteStates:
    ON = 1
    OFF = 0


class RulesState:
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    SUCCESSFUL = 'successful'
    ERROR = 'error'
    CANCELED = 'canceled'
