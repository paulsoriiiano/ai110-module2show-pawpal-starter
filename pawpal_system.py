from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    duration: int       # in minutes
    priority: str       # e.g. "high", "medium", "low"


@dataclass
class Pet:
    name: str
    type: str           # e.g. "dog", "cat", "fish"
    breed: str
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Owner:
    username: str
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, pet: Pet, task: Task) -> None:
        pass

    def see_todays_tasks(self) -> List[Task]:
        pass


@dataclass
class Plan:
    date: str
    tasks: List[Task] = field(default_factory=list)

    def generate_plan(self) -> None:
        pass

    def explain_plan(self) -> str:
        pass