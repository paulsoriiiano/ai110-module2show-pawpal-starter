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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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
