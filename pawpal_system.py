from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


# How far out to schedule the next occurrence when a recurring task is completed.
RECURRENCE_INTERVALS = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


@dataclass
class Task:
    name: str
    duration: int                         # in minutes
    priority: Priority
    pet: Optional[Pet] = None
    scheduled_time: Optional[str] = None  # e.g. "08:00"
    frequency: str = "daily"              # e.g. "daily", "twice daily", "weekly"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> Optional[Task]:
        """Mark this task as completed; recurring tasks spawn their next occurrence."""
        self.completed = True
        return self._spawn_next_occurrence()

    def reset(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    def _spawn_next_occurrence(self) -> Optional[Task]:
        """For 'daily'/'weekly' tasks, create the next occurrence due_date + interval away."""
        interval = RECURRENCE_INTERVALS.get(self.frequency)
        if interval is None:
            return None
        next_task = Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            pet=self.pet,
            scheduled_time=self.scheduled_time,
            frequency=self.frequency,
            due_date=self.due_date + interval,
        )
        if self.pet:
            self.pet.add_task(next_task)
        return next_task


@dataclass
class Pet:
    name: str
    type: str                             # e.g. "dog", "cat", "fish"
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        task.pet = self
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return this pet's tasks that are not yet completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    username: str
    name: str
    pets: List[Pet] = field(default_factory=list)
    scheduler: Optional[Scheduler] = None

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def add_task(self, pet: Pet, task: Task) -> None:
        """Add a task to the given pet."""
        pet.add_task(task)

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return this owner's tasks, optionally narrowed by pet name and/or completion status."""
        all_tasks = [task for pet in self.pets for task in pet.tasks]
        if pet_name is not None:
            all_tasks = [t for t in all_tasks if t.pet and t.pet.name == pet_name]
        if completed is not None:
            all_tasks = [t for t in all_tasks if t.completed == completed]
        return all_tasks

    def see_todays_tasks(self) -> List[Task]:
        """Return all of this owner's pets' tasks, sorted by priority then time."""
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
    conflicts: List[str] = field(default_factory=list)

    def _time_key(self, task: Task) -> tuple:
        """Sort key: chronological time, unscheduled tasks last, priority as tiebreaker."""
        minutes = None
        if task.scheduled_time:
            try:
                hh, mm = task.scheduled_time.split(":")
                minutes = int(hh) * 60 + int(mm)
            except (ValueError, AttributeError):
                minutes = None
        return (minutes is None, minutes or 0, -task.priority.value)

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks chronologically by scheduled_time (unscheduled tasks last)."""
        tasks = self.tasks if tasks is None else tasks
        return sorted(tasks, key=self._time_key)

    def generate_plan(self) -> Scheduler:
        """Build the sorted task plan for this scheduler's owner and date."""
        if not self.owner:
            return self
        all_tasks = [task for pet in self.owner.pets for task in pet.tasks]
        self.tasks = self.sort_by_time(all_tasks)
        self.conflicts = self.detect_conflicts(self.tasks)
        return self

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Lightweight conflict check: group scheduled tasks by exact start time and
        warn whenever more than one task (same pet or different pets) shares a slot."""
        tasks = self.tasks if tasks is None else tasks
        by_time: dict[str, List[Task]] = {}
        for task in tasks:
            if task.scheduled_time:
                by_time.setdefault(task.scheduled_time, []).append(task)

        warnings = []
        for time_str, group in by_time.items():
            if len(group) > 1:
                names = ", ".join(
                    f"{t.name} ({t.pet.name if t.pet else 'Unassigned'})" for t in group
                )
                warnings.append(f"Conflict at {time_str}: {names}")
        return warnings

    def explain_plan(self) -> str:
        """Render the generated plan as a human-readable, per-pet table."""
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

        if self.conflicts:
            lines.append("\n  WARNINGS:")
            for warning in self.conflicts:
                lines.append(f"  - {warning}")

        return "\n".join(lines)
