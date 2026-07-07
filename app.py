from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Task, Priority, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(username="jordan", name=owner_name)
else:
    st.session_state.owner.name = owner_name

owner: Owner = st.session_state.owner

st.markdown("### Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed", value="")

if st.button("Add pet"):
    if any(p.name == pet_name for p in owner.pets):
        st.warning(f"{pet_name} is already added.")
    else:
        owner.add_pet(Pet(name=pet_name, type=species, breed=breed))

if owner.pets:
    st.write("Current pets:", ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("### Add a Task")
if not owner.pets:
    st.info("Add a pet before scheduling tasks.")
else:
    pet_for_task = st.selectbox("Pet", owner.pets, format_func=lambda p: p.name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    scheduled_time = st.text_input("Scheduled time (e.g. 08:00)", value="08:00")
    frequency = st.text_input("Frequency", value="daily")

    if st.button("Add task"):
        owner.add_task(
            pet_for_task,
            Task(
                name=task_title,
                duration=int(duration),
                priority=Priority[priority_label.upper()],
                scheduled_time=scheduled_time,
                frequency=frequency,
            ),
        )

    pending = owner.see_todays_tasks()
    if pending:
        st.write("Current tasks:")
        st.table(
            [
                {
                    "pet": t.pet.name if t.pet else "",
                    "title": t.name,
                    "duration_minutes": t.duration,
                    "priority": t.priority.name,
                    "time": t.scheduled_time,
                    "frequency": t.frequency,
                }
                for t in pending
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(date=str(date.today()), owner=owner)
    scheduler.generate_plan()
    st.session_state.scheduler = scheduler

if "scheduler" in st.session_state:
    st.code(st.session_state.scheduler.explain_plan())
