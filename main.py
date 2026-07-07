from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def main():
    # --- Setup ---
    owner = Owner(username="jsmith", name="Jamie Smith")

    buddy = Pet(name="Buddy", type="dog", breed="Golden Retriever")
    luna  = Pet(name="Luna",  type="cat", breed="Siamese")

    owner.add_pet(buddy)
    owner.add_pet(luna)

    # --- Tasks for Buddy (added out of chronological order) ---
    owner.add_task(buddy, Task(
        name="Enrichment Play",
        duration=20,
        priority=Priority.MEDIUM,
        scheduled_time="17:00",
        frequency="daily",
    ))
    owner.add_task(buddy, Task(
        name="Morning Walk",
        duration=30,
        priority=Priority.HIGH,
        scheduled_time="07:00",
        frequency="daily",
    ))
    feeding = Task(
        name="Feeding",
        duration=10,
        priority=Priority.HIGH,
        scheduled_time="08:00",
        frequency="twice daily",
    )
    owner.add_task(buddy, feeding)
    feeding.mark_complete()

    # Conflicting task: same time (09:00) as Luna's "Medication" below, on a different pet.
    owner.add_task(buddy, Task(
        name="Vet Check-in",
        duration=15,
        priority=Priority.MEDIUM,
        scheduled_time="09:00",
        frequency="daily",
    ))

    # --- Tasks for Luna (also added out of chronological order) ---
    owner.add_task(luna, Task(
        name="Grooming",
        duration=15,
        priority=Priority.LOW,
        scheduled_time="14:00",
        frequency="weekly",
    ))
    owner.add_task(luna, Task(
        name="Medication",
        duration=5,
        priority=Priority.HIGH,
        scheduled_time="09:00",
        frequency="daily",
    ))

    # --- Generate and print schedule ---
    scheduler = Scheduler(date="2026-07-06", owner=owner)
    scheduler.generate_plan()

    width = 52
    print("=" * width)
    print(" PAWPAL — TODAY'S SCHEDULE".center(width))
    print(" Owner: Jamie Smith".center(width))
    print("=" * width)
    print(scheduler.explain_plan())
    print("=" * width)
    total = sum(t.duration for t in scheduler.tasks)
    print(f"  Total care time: {total} min across {len(scheduler.tasks)} tasks")
    print("=" * width)

    # --- Demo: detect_conflicts() catches the double-booked 09:00 slot ---
    print()
    if scheduler.conflicts:
        print("Conflicts detected:")
        for warning in scheduler.conflicts:
            print(f"  ! {warning}")
    else:
        print("No conflicts detected.")

    # --- Demo: sort_by_time() on tasks that were added out of order ---
    print()
    print("Chronological order (sort_by_time):")
    for t in scheduler.sort_by_time():
        status = "done" if t.completed else "pending"
        pet_name = t.pet.name if t.pet else "Unassigned"
        print(f"  {t.scheduled_time or '--:--'}  {pet_name:<8} {t.name:<16} [{status}]")

    # --- Demo: filter_tasks() by pet name and by completion status ---
    print()
    print("Buddy's tasks only (filter_tasks(pet_name='Buddy')):")
    for t in owner.filter_tasks(pet_name="Buddy"):
        print(f"  {t.name}")

    print()
    print("Pending tasks only (filter_tasks(completed=False)):")
    for t in owner.filter_tasks(completed=False):
        print(f"  {t.name}")

    print()
    print("Luna's pending tasks (filter_tasks(pet_name='Luna', completed=False)):")
    for t in owner.filter_tasks(pet_name="Luna", completed=False):
        print(f"  {t.name}")


if __name__ == "__main__":
    main()
