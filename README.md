# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
====================================================
              PAWPAL — TODAY'S SCHEDULE             
                 Owner: Jamie Smith                 
====================================================
Plan for 2026-07-06:

  Buddy (Golden Retriever)
  STATUS   TASK                 TIME    PRIORITY MINS   FREQUENCY   
  ------------------------------------------------------------------
  [    ]   Morning Walk         07:00   HIGH     30     daily       
  [    ]   Feeding              08:00   HIGH     10     twice daily 
  [    ]   Enrichment Play      17:00   MEDIUM   20     daily       

  Luna (Siamese)
  STATUS   TASK                 TIME    PRIORITY MINS   FREQUENCY   
  ------------------------------------------------------------------
  [    ]   Medication           09:00   HIGH     5      daily       
  [    ]   Grooming             14:00   LOW      15     weekly      
====================================================
  Total care time: 80 min across 5 tasks
====================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with verbose per-test output:
python -m pytest -v

# Run with coverage:
python -m pytest --cov
```

`tests/test_pawpal.py` covers the core scheduling behaviors:

- **Sorting correctness** — tasks come back in chronological order, unscheduled tasks sort last, same-time tasks break ties by priority, and an empty task list doesn't error.
- **Recurrence logic** — completing a `"daily"` task spawns a next-day occurrence attached to the same pet, while non-recurring frequencies (e.g. `"once"`) spawn nothing.
- **Conflict detection** — `Scheduler.detect_conflicts()` flags tasks that share an exact time slot and stays silent when times don't collide.
- **Basic task/pet behavior** — marking a task complete updates its status, and adding a task to a pet updates that pet's task list.

Sample test output:

```
============================= test session starts ==============================
collected 10 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 10%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 20%]
tests/test_pawpal.py::test_sort_by_time_orders_tasks_chronologically PASSED [ 30%]
tests/test_pawpal.py::test_sort_by_time_puts_unscheduled_tasks_last PASSED [ 40%]
tests/test_pawpal.py::test_sort_by_time_breaks_ties_by_priority PASSED   [ 50%]
tests/test_pawpal.py::test_sort_by_time_handles_empty_list PASSED        [ 60%]
tests/test_pawpal.py::test_mark_complete_on_daily_task_creates_next_day_occurrence PASSED [ 70%]
tests/test_pawpal.py::test_mark_complete_on_non_recurring_frequency_spawns_nothing PASSED [ 80%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED [ 90%]
tests/test_pawpal.py::test_detect_conflicts_ignores_distinct_times PASSED [100%]

============================== 10 passed in 0.02s ==============================
```

Confidence Level: ★★★☆☆ (3/5)

The core behaviors requested — sorting, recurrence, and conflict detection — are tested and passing (10/10), so I'm confident in the happy paths and the specific edge cases we covered (ties, unscheduled tasks, non-recurring frequencies, empty lists). There are still several edge cases that remain untested.


## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks chronologically by `scheduled_time` (parsed to minutes-since-midnight internally via `Scheduler._time_key()`). Unscheduled tasks sort last; tasks tied on the same time fall back to priority as a tiebreaker. Called automatically by `generate_plan()`. |
| Filtering | `Owner.filter_tasks(pet_name=None, completed=None)` | Narrows the owner's full task list by pet name and/or completion status — pass either, both, or neither to get everything. Used by the CLI demo and available to the Streamlit UI for "show me just Buddy's tasks" or "show me what's still pending." |
| Conflict handling | `Scheduler.detect_conflicts()` | Lightweight check that groups scheduled tasks by exact start time and flags any slot shared by more than one task (same pet or across different pets). Returns a list of warning strings rather than raising — `generate_plan()` stores them in `Scheduler.conflicts`, and `explain_plan()` prints them in a `WARNINGS:` section instead of crashing the program. |
| Recurring tasks | `Task.mark_complete()` → `Task._spawn_next_occurrence()` | Completing a `"daily"` or `"weekly"` task automatically creates the next occurrence and attaches it to the same pet. The next `due_date` is computed with `timedelta(days=1)` or `timedelta(weeks=1)` (see `RECURRENCE_INTERVALS`) added to the completed task's `due_date`. Non-recurring frequencies (e.g. `"twice daily"`) are left alone — `mark_complete()` just returns `None`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
