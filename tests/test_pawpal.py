from pawpal_system import Task, Pet, Priority


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
