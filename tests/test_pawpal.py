from datetime import timedelta

from pawpal_system import Task, Pet, Priority, Scheduler


def test_mark_complete_changes_status():
    task = Task(name="Feed", duration=10, priority=Priority.MEDIUM)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rex", type="dog", breed="Labrador")
    task = Task(name="Walk", duration=30, priority=Priority.HIGH)
    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1


# --- Sorting correctness -----------------------------------------------

def test_sort_by_time_orders_tasks_chronologically():
    scheduler = Scheduler(date="2026-07-06")
    late = Task(name="Dinner", duration=15, priority=Priority.LOW, scheduled_time="18:00")
    early = Task(name="Breakfast", duration=15, priority=Priority.LOW, scheduled_time="07:00")
    mid = Task(name="Walk", duration=30, priority=Priority.LOW, scheduled_time="12:30")

    ordered = scheduler.sort_by_time([late, early, mid])

    assert [t.name for t in ordered] == ["Breakfast", "Walk", "Dinner"]


def test_sort_by_time_puts_unscheduled_tasks_last():
    scheduler = Scheduler(date="2026-07-06")
    scheduled = Task(name="Feed", duration=10, priority=Priority.LOW, scheduled_time="09:00")
    unscheduled = Task(name="Groom", duration=20, priority=Priority.HIGH)

    ordered = scheduler.sort_by_time([unscheduled, scheduled])

    assert [t.name for t in ordered] == ["Feed", "Groom"]


def test_sort_by_time_breaks_ties_by_priority():
    scheduler = Scheduler(date="2026-07-06")
    low = Task(name="Brush", duration=5, priority=Priority.LOW, scheduled_time="08:00")
    high = Task(name="Medicine", duration=5, priority=Priority.HIGH, scheduled_time="08:00")

    ordered = scheduler.sort_by_time([low, high])

    assert [t.name for t in ordered] == ["Medicine", "Brush"]


def test_sort_by_time_handles_empty_list():
    scheduler = Scheduler(date="2026-07-06")

    assert scheduler.sort_by_time([]) == []


# --- Recurrence logic -----------------------------------------------------

def test_mark_complete_on_daily_task_creates_next_day_occurrence():
    pet = Pet(name="Rex", type="dog", breed="Labrador")
    task = Task(name="Feed", duration=10, priority=Priority.MEDIUM, frequency="daily")
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert next_task.name == task.name
    assert next_task.pet is pet
    assert next_task in pet.tasks


def test_mark_complete_on_non_recurring_frequency_spawns_nothing():
    task = Task(name="Vet visit", duration=60, priority=Priority.HIGH, frequency="once")

    next_task = task.mark_complete()

    assert next_task is None


# --- Conflict detection -----------------------------------------------

def test_detect_conflicts_flags_duplicate_times():
    scheduler = Scheduler(date="2026-07-06")
    task_a = Task(name="Feed", duration=10, priority=Priority.MEDIUM, scheduled_time="08:00")
    task_b = Task(name="Walk", duration=30, priority=Priority.LOW, scheduled_time="08:00")

    conflicts = scheduler.detect_conflicts([task_a, task_b])

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
    assert "Feed" in conflicts[0] and "Walk" in conflicts[0]


def test_detect_conflicts_ignores_distinct_times():
    scheduler = Scheduler(date="2026-07-06")
    task_a = Task(name="Feed", duration=10, priority=Priority.MEDIUM, scheduled_time="08:00")
    task_b = Task(name="Walk", duration=30, priority=Priority.LOW, scheduled_time="09:00")

    conflicts = scheduler.detect_conflicts([task_a, task_b])

    assert conflicts == []
