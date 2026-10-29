# Claude Code in Cursor: A Practical Guide for Learning and Building

**Purpose:** Help you use Claude Code as a coding partner inside Cursor without surrendering your understanding or control.

> Product details can change. Check the official Claude Code documentation linked at the end when a command or UI differs from your installation.

## 1. Understand the tools you have

- **Cursor** is the editor: files, search, terminal, diffs, and project navigation.
- **Claude Code** is an agentic coding assistant. Depending on its permissions and integration, it can inspect files, propose or make edits, run commands, and help verify changes.
- **`CLAUDE.md`** is persistent project guidance. It gives Claude durable facts and working rules; it is not the entire codebase and does not replace reading source files.
- **Git** records changes and gives you a way to review or restore work. It is your safety net, not a substitute for understanding changes.

## 2. Set up project context properly

1. Open the **actual project root** in Cursor, not just a single source file.
2. Put the provided `CLAUDE.md` in that root directory.
3. In Claude Code, ask it to read the project instructions and inspect the repository. A useful first prompt:

   > Read `CLAUDE.md`, then inspect the repository tree and the relevant gesture-recognition files. Do not edit anything yet. Summarize what exists, what is uncertain, and the smallest sensible next step.

4. Check whether the extension recognizes project instructions. If uncertain, ask Claude what project instruction files it has read. Do not assume a file was loaded just because it exists.
5. Keep project instructions concise, accurate, and updated. Put long explanations in separate documentation files and link to them from `CLAUDE.md` if needed.

### What belongs in `CLAUDE.md`?

Good:
- What the project is and what is currently being built.
- Architecture boundaries and key data shapes.
- Coding conventions and test commands.
- Important constraints and user preferences.
- Known bugs or current learning checkpoint.

Avoid:
- A full copy of every source file.
- Temporary details that will become stale tomorrow.
- Contradictory instructions.
- Secrets, API keys, passwords, or personal credentials.
- Claims that code works if it has not been tested.

## 3. The core workflow: investigate → plan → edit → verify → review

Use this loop for almost every meaningful change.

### Step 1 — Investigate first

Ask Claude to open the actual files and trace the data flow. For example:

> Find the current `translation_invariance` method. Read its callers and relevant types. Explain the input structure, output structure, and any problems. Do not edit yet.

This prevents advice based on an imagined codebase.

### Step 2 — Ask for a plan

> Propose the smallest safe change. List files to modify, expected behavior, edge cases, and how you will test it. Do not implement until I approve.

For a tiny typo fix, a separate planning phase may be unnecessary. For data-model changes, normalization, or architecture changes, it is valuable.

### Step 3 — Make a small change

> Implement only the approved change. Preserve existing conventions and unrelated work. Explain any non-obvious decisions.

Avoid vague prompts such as “fix everything,” “make it professional,” or “rewrite the project.” They invite broad changes that are difficult to review.

### Step 4 — Verify

Ask Claude to run the relevant tests or a small script. Require it to report:
- The exact command it ran.
- Whether it succeeded.
- Any tests it could not run.
- What the test proves—and what it does not prove.

For the current normalization work, useful checks include:
- Each hand produces an array of shape `(21, 3)`.
- After translation, the anchor row is approximately `[0, 0, 0]`.
- Original MediaPipe landmarks are not mutated.
- Each detected hand remains a separate array.
- Scale normalization makes the chosen reference distance approximately `1`.
- Rotation aligns the chosen reference direction using the intended coordinate convention.

### Step 5 — Review the diff

Ask:

> Show me the diff and explain every meaningful change. Point out any behavior change, assumption, untested path, or unnecessary edit. Do not commit anything.

Read the diff yourself. Reject changes you do not understand or do not want.

## 4. Prompting patterns that work well

A strong task prompt contains:
1. **Goal:** what outcome you want.
2. **Context:** relevant files, data shapes, constraints.
3. **Scope:** what may and may not change.
4. **Acceptance criteria:** observable conditions for success.
5. **Verification:** tests or checks to perform.

### Example: review only

> Review the normalization function. Inspect the actual file and relevant callers first. Explain bugs and their causes. Do not edit code. Focus only on translation normalization and the `(21, 3)` representation.

### Example: implement one step

> Implement translation normalization only. Preserve raw input, use the existing architecture, and return one NumPy array of shape `(21, 3)` per detected hand. Add focused tests for anchor-at-origin, input immutability, invalid shape, and multiple hands. Do not add scale, rotation, features, or classification. Run the tests and summarize the results.

### Example: learn a concept

> Teach me NumPy broadcasting using my actual expression `points - points[0]`. Explain the shapes of both operands, how the subtraction is applied, and why the result is correct. Then give me a tiny numerical example and ask me to predict the output before revealing it. Do not jump to the next topic.

### Example: diagnose a bug

> Reproduce the failure if possible. Trace the values and shapes before changing anything. State the root cause, the smallest fix, and a test that would fail before the fix and pass afterward.

### Example: architecture review

> Evaluate whether this module boundary is sensible. Compare the simplest viable design with one alternative. Explain trade-offs, but do not create or move files until I approve.

### Example: end-of-session checkpoint

> Summarize the work completed, files changed, tests and outcomes, known limitations, and the exact next step. Update project documentation only if it will remain useful. Do not claim unrun tests passed.

## 5. Use Plan Mode for risky or unclear tasks

When the task could affect multiple files or behavior is uncertain, use the available Plan Mode or plan-only permission mode in your Claude Code integration. First ask for inspection and a proposal; approve the approach before edits.

Use direct implementation for small, well-defined tasks. Do not spend more time planning than the task warrants.

## 6. Keep control of permissions and terminal commands

Claude Code may ask permission before editing files or running shell commands. Read each request.

- Prefer reviewing a command before allowing it.
- Do not enable broad permission bypass just to save clicks.
- Be cautious with commands that delete files, reset Git changes, overwrite directories, install software, modify system settings, publish, commit, or push.
- Never paste secrets into prompts or commit them to the repository.
- If Claude proposes a destructive command, ask what it will affect and request a safer alternative.
- Keep backups or use Git before substantial refactors.

The safest default is to grant only the access needed for the current task.

## 7. Use Git as a checkpoint system

Before a significant change:
1. Check the working tree and review existing modifications.
2. Make sure you know which changes are yours and which predate the task.
3. Use a commit or another backup checkpoint when appropriate.
4. Review `git diff` after Claude edits.
5. Test before deciding whether to keep the change.

Useful read-only commands, from the project terminal:

```bash
git status
git diff
git diff --stat
```

Do not run reset/clean commands just because Claude suggests them; they can discard work. Ask before destructive Git operations.

## 8. Keep the context useful, not enormous

Claude works best when the relevant context is clear.

- Work from the repository root.
- Name the relevant file or function.
- Ask Claude to inspect callers and tests when behavior crosses module boundaries.
- Put stable project-wide facts in `CLAUDE.md`.
- Keep temporary task details in the current prompt.
- Store durable decisions in documentation only when they are likely to matter later.
- If a conversation gets long, ask for a checkpoint and start a fresh task with that checkpoint plus the relevant files.
- Correct stale context promptly. Project instructions are guidance, not unquestionable truth.

Do not ask Claude to load every file when only two or three are relevant. Conversely, do not ask it to edit a function without reading that function and its dependencies.

## 9. A learning-first workflow for your gesture project

For each concept, follow this sequence:

1. **Understand:** Ask for the mathematical idea and assumptions.
2. **Predict:** Work out what the operation should do on a tiny example.
3. **Implement:** Change only that stage.
4. **Inspect:** Print shapes and selected values.
5. **Test:** Verify the mathematical property.
6. **Explain:** Ask Claude to explain the code line by line.
7. **Record:** Save the key result and next question.

For the current normalization stage:

### Translation
- Input: raw landmarks for one hand, shape `(21, 3)`.
- Operation: subtract the anchor point from every row.
- Expected property: the anchor becomes `[0, 0, 0]`.
- Invariance: adding the same offset to all original points should not change translated output (up to floating-point precision).
- Safety: do not mutate MediaPipe's original landmark objects.

### Scale
- Use one characteristic size per hand, such as the wrist-to-middle-MCP distance.
- Divide every translated point by that one scalar.
- Expected property: the selected reference distance becomes approximately `1`.
- Guard against zero or near-zero scale.

### Rotation
- First experiment: in-plane rotation around the z-axis using a defined reference vector.
- Expected property: that reference direction aligns with the chosen axis under the stated coordinate convention.
- Limitation: this is not full 3D rotation normalization.
- Test it separately before combining it with translation and scale.

Do not add feature extraction or classification until these three operations are understood and tested.

## 10. Common mistakes to avoid

- Asking Claude to “fix everything” without defining success.
- Trusting a confident explanation without inspecting the source.
- Accepting a large rewrite when a small correction would do.
- Letting the assistant change raw input objects in place without realizing it.
- Confusing a list of dictionaries with a numeric NumPy array.
- Assuming `(21, 3)` means three hands or 21 hands; it means 21 points, each with 3 coordinates.
- Treating a passing unit test as proof the whole application works.
- Letting generated tests merely repeat the implementation's assumptions.
- Allowing Claude to commit, push, delete, install, or publish without review.
- Keeping outdated project instructions indefinitely.

## 11. Useful Claude Code capabilities to learn gradually

Availability and names can vary by version and editor integration. Check the current help or official docs before relying on a command.

- **Project memory / `CLAUDE.md`:** persistent project instructions.
- **Plan mode:** inspect and plan before editing.
- **Slash commands:** built-in session commands; use the command list shown by your installed version.
- **Context/memory inspection:** check which instruction files are loaded.
- **Permission controls:** review and adjust what Claude can do.
- **Git integration:** inspect changes and understand project history.
- **MCP integrations:** connect external tools only when genuinely useful; review permissions and data access before connecting.
- **Subagents or parallel work:** useful for independent research/review tasks, but avoid splitting a small learning task into needless complexity.
- **Hooks and custom commands/skills:** advanced automation; learn only after the basic workflow is reliable.

## 12. A reusable task template

Copy and adapt this for substantial tasks:

```text
Goal:
[What I want to achieve]

Context:
[Relevant files, current behavior, data shapes]

Scope:
[What may change]
[What must not change]

Learning requirement:
Explain the important reasoning and mathematics. Do not hide the key idea behind code.

Workflow:
1. Inspect relevant files and callers.
2. Summarize current behavior and uncertainties.
3. Propose the smallest safe plan.
4. Wait for approval if the change is broad or risky.
5. Implement only the agreed scope.
6. Run relevant tests or verification.
7. Review the diff.

Acceptance criteria:
- [Observable requirement]
- [Edge case]
- [Expected output or invariant]

Constraints:
- Preserve unrelated user changes.
- Do not install dependencies, commit, push, publish, or perform destructive actions without permission.
- Do not claim unrun tests passed.
```

## 13. Official references

- Claude Code getting started: https://docs.anthropic.com/en/docs/claude-code/getting-started
- Claude Code CLI usage: https://docs.anthropic.com/en/docs/claude-code/cli-usage
- Claude Code memory / `CLAUDE.md`: https://docs.anthropic.com/en/docs/claude-code/memory
- Claude Code common workflows: https://docs.anthropic.com/en/docs/claude-code/common-tasks
- Claude Code permissions: https://docs.anthropic.com/en/docs/claude-code/iam

Documentation and commands can change. Prefer current official documentation when something differs from this guide or your installed extension.
