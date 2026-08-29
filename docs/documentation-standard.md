# Documentation Standard

Documentation must explain the implemented project rather than provide a generic encyclopedia entry. Prefer short claims supported by code, tests, profiler output, timings, logs, or a reproducible observation.

## `README.md`

Use these sections where applicable:

1. Problem
2. Learning goals
3. Architecture
4. How to run
5. Main experiment
6. Tests
7. Optional extensions

The README is the entry point. A reader should be able to run the project and reproduce its central behavior without reading every source file.

## `STUDY.md`

Record what happened during implementation and experimentation:

- initial hypothesis;
- experiment procedure;
- observed result;
- explanation connected to the implementation;
- remaining questions.

Prefer: “Selecting an issue notified all listeners, but the cached search snapshot retained its reference and Search did not commit.”

Avoid: “Referential equality is the comparison of references.”

If an experiment has not been run, label its expected result as a hypothesis rather than presenting it as evidence.

## `DECISIONS.md`

Only record decisions that materially affect the lesson or architecture. Each entry should contain:

- **Decision**
- **Context**
- **Why**
- **Trade-offs**
- **When to reconsider**

Do not use decision records for formatting choices or routine implementation details.

## Style

- Write in concise English.
- Explain motivation before mechanics.
- Link to primary documentation when it improves reproducibility.
- Keep commands copyable and paths relative to the project or repository root.
- Distinguish verified observations from expectations and recommendations.
