# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

1. Owner/User:
    - Attributes
        - Username
        - Name
        - owns pet(s) (weak has-a relationship)
    - Actions
        - add a pet
        - add task
        - see today's tasks
2. Pet
    - Attributes
        - Name
        - Type/Breed (dog, cat, fish, etc.)
        - has task(s) (weak has-a relationship)
3. Task
    - Duration
    - Priority
4. Plan
    - organizes tasks (consists-of relationship)

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, I made some changes. There were a few missing relationships and logic bottlenecks:
1. Define task priority as `Enum`: makes tasks sortable by priority
2. Add `plan` attribute to `Owner`: connects owner to their active plan

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The Scheduler only considers time at the moment. The implementation for detecting conflicts is simple, lightweight logic, so it doesn't take into account the priority of a task.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The Scheduler logic for detecting conflicts is by grouping tasks by start time and checking if the start time has 2 or more tasks for it. It doesn't take into account time blocks. That tradeoff is reasonable for the first pass implementation, in my opinion. However, for a more robust and production-ready implementation, it is not enough.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
