from __future__ import annotations

from enum import Enum


class ProcurementSlotKey(str, Enum):
    MAIN = "MAIN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class ProcurementValueMode(str, Enum):
    SCALAR = "SCALAR"
    PERSON_SINGLE = "PERSON_SINGLE"
    PERSON_LIST = "PERSON_LIST"
    TEAM_SINGLE = "TEAM_SINGLE"
    TEAM_LIST = "TEAM_LIST"
    EPISODE = "EPISODE"


class CoordinationStatusKey(str, Enum):
    OPEN = "OPEN"


class FavoriteTypeKey(str, Enum):
    PATIENT = "PATIENT"
    EPISODE = "EPISODE"
    COLLOQUIUM = "COLLOQUIUM"
    COORDINATION = "COORDINATION"


class TaskScopeKey(str, Enum):
    ALL = "ALL"
    PATIENT = "PATIENT"
    EPISODE = "EPISODE"
    COORDINATION_PROTOCOL = "COORDINATION_PROTOCOL"


class TaskStatusKey(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TaskKindKey(str, Enum):
    TASK = "TASK"
    EVENT = "EVENT"


class PriorityKey(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
