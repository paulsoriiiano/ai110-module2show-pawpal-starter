from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    name: str
    duration: int                       # in minutes
    priority: Priority
    pet: Optional[Pet] = None
    scheduled_time: Optional[str] = None  # e.g. "08:00"
    frequency: str = "daily"            # e.g. "daily", "twice daily", "weekly"


@dataclass
class Pet:
    name: str
    type: str                           # e.g. "dog", "cat", "fish"
    breed: str
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Owner:
    username: str
    name: str
    pets: List[Pet] = field(default_factory=list)
    plan: Optional[Plan] = None

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, pet: Pet, task: Task) -> None:
        pass

    def see_todays_tasks(self) -> List[Task]:
        pass


@dataclass
class Plan:
    date: str
    owner: Optional[Owner] = None
    tasks: List[Task] = field(default_factory=list)

    def generate_plan(self) -> Plan:
        pass

    def explain_plan(self) -> str:
        pass