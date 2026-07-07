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
    duration: int                         # in minutes
    priority: Priority
    pet: Optional[Pet] = None
    scheduled_time: Optional[str] = None  # e.g. "08:00"
    frequency: str = "daily"              # e.g. "daily", "twice daily", "weekly"
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def reset(self) -> None:
        self.completed = False


@dataclass
class Pet:
    name: str
    type: str                             # e.g. "dog", "cat", "fish"
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        task.pet = self
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    username: str
    name: str
    pets: List[Pet] = field(default_factory=list)
    scheduler: Optional[Scheduler] = None

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def add_task(self, pet: Pet, task: Task) -> None:
        pet.add_task(task)

    def see_todays_tasks(self) -> List[Task]:
        all_tasks = [task for pet in self.pets for task in pet.tasks]
        return sorted(all_tasks, key=lambda t: (
            -t.priority.value,
            t.scheduled_time or "99:99"
        ))


@dataclass
class Scheduler:
    date: str
    owner: Optional[Owner] = None
    tasks: List[Task] = field(default_factory=list)

    def generate_plan(self) -> Scheduler:
        if not self.owner:
            return self
        all_tasks = [task for pet in self.owner.pets for task in pet.tasks]
        self.tasks = sorted(all_tasks, key=lambda t: (
            -t.priority.value,
            t.scheduled_time or "99:99"
        ))
        return self

    def explain_plan(self) -> str:
        if not self.tasks:
            return "No tasks scheduled."

        col_status = 8
        col_task   = 20
        col_time   = 7
        col_pri    = 8
        col_mins   = 6
        col_freq   = 12
        header = (
            f"  {'STATUS':<{col_status}} {'TASK':<{col_task}} {'TIME':<{col_time}}"
            f" {'PRIORITY':<{col_pri}} {'MINS':<{col_mins}} {'FREQUENCY':<{col_freq}}"
        )
        divider = "  " + "-" * (col_status + col_task + col_time + col_pri + col_mins + col_freq + 5)

        lines = [f"Plan for {self.date}:"]
        by_pet: dict[str, List[Task]] = {}
        for task in self.tasks:
            key = task.pet.name if task.pet else "Unassigned"
            by_pet.setdefault(key, []).append(task)

        for pet_name, tasks in by_pet.items():
            pet = tasks[0].pet
            breed_str = f" ({pet.breed})" if pet else ""
            lines.append(f"\n  {pet_name}{breed_str}")
            lines.append(header)
            lines.append(divider)
            for task in tasks:
                status   = "[done]" if task.completed else "[    ]"
                time_str = task.scheduled_time or "--:--"
                lines.append(
                    f"  {status:<{col_status}} {task.name:<{col_task}} {time_str:<{col_time}}"
                    f" {task.priority.name:<{col_pri}} {task.duration:<{col_mins}} {task.frequency:<{col_freq}}"
                )
        return "\n".join(lines)
