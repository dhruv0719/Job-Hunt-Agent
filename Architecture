# AI Job Hunt Agent - System Architecture

---

## Introduction

The AI Job Hunt Agent is a planner-driven multi-agent system designed to automate the repetitive and research-intensive parts of job hunting while keeping humans in control of every external action.

Instead of relying on a single large AI model, the system delegates responsibilities to specialized agents coordinated by a central Planner. This approach produces modular, explainable, reusable, and reliable workflows while ensuring that important decisions remain transparent and easy to debug.

---

# Design Principles

- Planner owns the workflow.
- Agents have a single responsibility.
- Humans approve every external action.
- Reuse previous work whenever possible.
- Share only relevant context.
- Keep agents modular and replaceable.
- Every factual output must be grounded.
- Fail safely instead of guessing.
- Components should remain loosely coupled.
- Every workflow should be explainable and observable.

---

# Overall System Architecture

```text
                    User
                      │
                      ▼
              Planner / Orchestrator
                      │
                      ▼
              Shared Memory Layer
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Company        Company Research   JD Matching
 Discovery          Agent             Agent
      │               │                │
      └───────────────┼────────────────┘
                      ▼
             Resume Tailoring Agent
                      │
                      ▼
          Cover Letter / Outreach Agent
                      │
                      ▼
             Human Review Dashboard
                      │
          Approve / Pause / Cancel
                      │
                      ▼
             Application Tracker
```

The user provides their profile, career goals, and preferences. The Planner coordinates the execution of specialized agents while using the shared memory layer to exchange only relevant information. Every external action is routed through the Human Review Dashboard before being completed.

---

# Core Components

| Component | Responsibility |
|------------|----------------|
| Planner | Coordinates workflow, state, retries, task scheduling, and agent execution |
| Discovery Agent | Finds companies matching the user's skills and preferences |
| Research Agent | Collects, verifies, and summarizes company information |
| JD Matching Agent | Matches open roles against the user's profile |
| Resume Agent | Tailors the resume based on the Job Description |
| Draft Agent | Generates cover letters and outreach drafts |
| Human Review | Reviews, edits, approves, pauses, or cancels workflows |
| Application Tracker | Maintains application history and workflow status |

---

# Planner / Orchestrator

The Planner is the central decision-making component of the system.

Rather than allowing agents to communicate directly, every agent reports its result back to the Planner. The Planner evaluates the current workflow state, determines the next action, manages retries, monitors execution progress, and updates the workflow state.

### Responsibilities

- Start workflows
- Schedule agents
- Track workflow state
- Manage retries
- Handle failures
- Route outputs between agents
- Monitor execution progress
- Pause, resume, or cancel workflows
- Notify the user about workflow progress

The Planner is responsible for orchestration only. It never performs specialized work such as company research or resume generation.

---

# Agent Philosophy

Every agent in the system follows the same design philosophy.

- Have one responsibility.
- Receive structured input.
- Produce structured output.
- Never manage the overall workflow.
- Report results back to the Planner.
- Be modular and replaceable.
- Never directly modify global workflow state.
- Never communicate directly with another agent.

---

# Workflow Lifecycle

```text
User

↓

Planner

↓

Company Discovery

↓

Planner

↓

Company Research

↓

Planner

↓

JD Matching

↓

Planner

↓

Resume Tailoring

↓

Planner

↓

Cover Letter / Outreach

↓

Human Review

↓

Application Tracker
```

Every stage reports back to the Planner before another task begins.

---

# Memory Architecture

```text
               Shared Memory

        ┌────────┼──────────┐

        │        │          │

   User Memory  Company   Workflow
                 Memory    Memory

                    │

          Application History
```

### User Memory

Stores long-term information about the candidate.

Examples

- Resume
- Skills
- Projects
- GitHub
- LinkedIn
- Career goals
- Preferences

---

### Company Memory

Stores information collected during company research.

Examples

- Company summary
- Products
- Clients
- Tech stack
- Careers page
- Recent news
- Research sources

---

### Workflow Memory

Stores temporary information during execution.

Examples

- Current workflow state
- Intermediate agent outputs
- Pending tasks
- Current progress

---

### Application History

Stores historical application data.

Examples

- Companies applied
- Resume versions
- Cover letters
- Application dates
- Interview status
- Response history

---

# State Management

The Planner is the single owner of workflow state.

Agents receive the current state as input but cannot modify it directly.

State is updated after every completed task, allowing workflows to be paused, resumed, or recovered without restarting the entire pipeline.

Typical workflow states include:

- Pending
- Running
- Waiting
- Review
- Completed
- Failed
- Cancelled

---

# Agent Communication

Agents never communicate directly with one another.

Instead, every agent returns its output to the Planner.

The Planner validates the output, updates workflow state, and determines which agent should execute next.

This centralized communication model simplifies debugging, monitoring, retries, and future scalability.

---

# Execution Model

The system follows a Planner-driven execution model.

- Planner creates the execution plan.
- Independent tasks may execute in batches.
- Agents retry failed tasks up to a configurable threshold.
- Long-running workflows can be paused or resumed.
- Users may cancel execution at any time.
- Every execution step is logged for future reference.

---

# Human-in-the-Loop

The system is designed to keep humans in control of all external actions.

Users can:

- Review outputs
- Edit generated content
- Pause execution
- Resume execution
- Cancel execution
- Approve workflows

No email, application, or external communication is performed without explicit user approval.

---

# Failure Handling

Failures are treated as part of the normal workflow.

Typical execution flow:

```text
Agent Failure

↓

Retry

↓

Retry

↓

Retry

↓

Planner Evaluation

↓

Human Notification (if needed)
```

The Planner determines whether a workflow should continue, retry, or stop based on the type of failure and configured retry limits.

---

# Future Architecture

The architecture is intentionally designed to evolve.

Potential future improvements include:

- Multi-user support
- Distributed agent execution
- Scheduled workflows
- Automatic company watchlists
- Learning from previous applications
- Smarter planning strategies
- Additional specialized agents