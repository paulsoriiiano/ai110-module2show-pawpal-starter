from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def main():
    # --- Setup ---
    owner = Owner(username="jsmith", name="Jamie Smith")

    buddy = Pet(name="Buddy", type="dog", breed="Golden Retriever")
    luna  = Pet(name="Luna",  type="cat", breed="Siamese")

    owner.add_pet(buddy)
    owner.add_pet(luna)

    # --- Tasks for Buddy ---
    owner.add_task(buddy, Task(
        name="Morning Walk",
        duration=30,
        priority=Priority.HIGH,
        scheduled_time="07:00",
        frequency="daily",
    ))
    owner.add_task(buddy, Task(
        name="Feeding",
        duration=10,
        priority=Priority.HIGH,
        scheduled_time="08:00",
        frequency="twice daily",
    ))
    owner.add_task(buddy, Task(
        name="Enrichment Play",
        duration=20,
        priority=Priority.MEDIUM,
        scheduled_time="17:00",
        frequency="daily",
    ))

    # --- Tasks for Luna ---
    owner.add_task(luna, Task(
        name="Medication",
        duration=5,
        priority=Priority.HIGH,
        scheduled_time="09:00",
        frequency="daily",
    ))
    owner.add_task(luna, Task(
        name="Grooming",
        duration=15,
        priority=Priority.LOW,
        scheduled_time="14:00",
        frequency="weekly",
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


if __name__ == "__main__":
    main()
