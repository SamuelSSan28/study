# Study Project Standard

## Purpose

A study project is a small implementation designed to answer a concrete engineering question. Its value comes from making behavior observable, not from feature count.

## Workflow

```text
Problem → Learning goals → MVP → Implementation
        → Experiment → Observation → Documentation → Extensions
```

Use the steps in order. Extensions are optional and must not obscure the main experiment.

## Questions every project must answer

- What am I trying to understand?
- What is the smallest implementation that demonstrates it?
- What failure or behavior can I reproduce?
- What did I observe?
- What trade-off did the solution introduce?

## Scope

1. State the problem and the behavior to investigate.
2. Define two to five learning goals.
3. Build the smallest runnable implementation that exposes the behavior.
4. Create a reproducible experiment with an expected observation.
5. Add tests at the boundaries where a regression would invalidate the lesson.
6. Record evidence and observations in `STUDY.md`.
7. Record consequential choices in `DECISIONS.md`.

Avoid unrelated authentication, deployment, databases, design systems, or abstractions unless they are part of the learning objective.

## Required project files

- `README.md`: problem, goals, architecture, setup, experiment, tests, and extensions.
- `STUDY.md`: evidence-based observations from implementing and running the project.
- `DECISIONS.md`: relevant decisions, context, trade-offs, and reconsideration triggers.
- Source and tests needed to reproduce the lesson.

## Definition of done

- The core behavior works and can be explained end to end.
- Relevant automated checks pass, or environmental limitations are recorded precisely.
- Another person can reproduce the main experiment.
- Observed results, including surprises or failures, are documented.
- Important decisions describe costs as well as benefits.
