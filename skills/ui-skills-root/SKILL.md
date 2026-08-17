---
name: ui-skills-root
description: Use automatically for UI-related work to select the smallest useful UI Skills context through the ui-skills CLI before implementation.
license: MIT
metadata:
  author: ibelick
  version: "1.0.0"
---

# UI Skills Root

You are the routing layer for UI Skills.

This skill is shown by `ui-skills start` and is also available in the registry.

Use it automatically when an agent in Codex, Cursor, or Claude Code has a clear UI goal: building, changing, reviewing, debugging, or polishing an interface.

If the goal is unclear, ask one short question.

If the goal is clear, choose the right category, load the smallest useful skill context, then implement without asking for confirmation.

## Protocol

1. decide if the task is UI-related
2. if not, continue normally without loading a UI skill
3. identify the likely category from the goal and stack
4. run `ui-skills list --category <category>`
5. select the smallest useful skill set
6. run `ui-skills get <slug>` only for the selected skill(s)
7. implement using that context

Do not run `ui-skills start` during a normal UI task. It only prints this routing skill. Use it only to inspect or reinstall the routing instructions.

## CLI

```bash
ui-skills start
ui-skills categories
ui-skills list --category <category>
ui-skills get <slug>
```

The CLI is installed globally via npm (`npm i -g ui-skills`). If the command is not found, fall back to `npx ui-skills <command>`.

Do not export the entire registry by default. The registry is intended for on-demand selection; persist a skill locally only when it needs to be enforced as a standing project or agent rule.

## Selection Rules

Prefer 1 skill.

Use 2 only when the task needs two clear angles.

Use 3 only for broad review, redesign, or multi-surface work.

Never use more than 3.

Route by topic, then stack, then specificity.

Prefer specific skills over broad skills.

Prefer framework-specific skills when the stack is obvious.

For quick cleanup, prefer the most specific craft, visual, or layout skill available.

If unsure, inspect categories and pick the safest narrow skill.
