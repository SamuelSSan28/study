# AGENTS.md

## Repository purpose

This repository contains weekly software engineering practice projects.
The objective is learning through implementation, experimentation, and documentation.

## Required reading

Before creating or significantly modifying a project, read:

- `docs/project-standard.md`
- `docs/engineering-principles.md`
- `docs/documentation-standard.md`
- `docs/testing-and-experiments.md`
- `docs/tech-selection.md`

## Core rules

- Keep projects small and focused; prefer depth over feature count.
- Do not introduce infrastructure without a learning reason.
- Every project must include a reproducible experiment.
- Document important architectural trade-offs.
- Choose technology according to the learning objective, not habit.
- Do not hide the studied concept behind a ready-made library.
- Preserve a project's original learning objective when modifying it.

## Project structure

Each project lives at `projects/<number>-<project-name>/` and normally contains:

- `README.md`
- `STUDY.md`
- `DECISIONS.md`
- source code
- tests

## Definition of done

A project is complete when the core learning objective works, relevant tests pass, the main experiment is reproducible, observations are documented, and architectural decisions and trade-offs are explained.
