# Instructions for coding agents

These instructions apply to all files in this repository.

## Language

Use Simplified Technical English for all communication and documentation.
This rule includes:

- Messages to the user and progress reports.
- README files and other documentation.
- Code comments and Python docstrings.
- Commit messages, pull request descriptions, and issue text.
- Text that the widget shows to the user.

Use short sentences, common words, and active voice.
Give one instruction in each sentence.
Use the same term for the same object or function.
Explain technical terms when the reader needs the explanation.
Avoid idioms, unnecessary words, and unclear abbreviations.
Use numbered steps for procedures.

Keep API names, code identifiers, commands, paths, and application names exact.
Keep legal license text and SPDX identifiers exact.

## Project purpose

The widget shows the active application name in a Plasma 6 panel.
Keep the widget small. Use QML and the Plasma task model.
Do not add a custom C++ plugin or an external process without a user request.

Keep these functions:

- Read the application name from `TaskManager.AbstractTasksModel.AppName`.
- Track the active task across all monitors.
- Keep screen, virtual desktop, and activity filters disabled.
- Use the panel text color and the system font. Keep the text bold.
- Update the label when the theme or font changes.
- Use a transparent background and one line of plain text.
- Replace excess text at the right end with an ellipsis.
- Keep the widget free of icons and window buttons.
- Show an empty label when no active application name is available.

Keep the name rules in `contents/code/Names.js`.
Match the full application name. Keep matches case-sensitive.
Do not use the window title or document title as an application name.

## Files

| Path | Purpose |
| --- | --- |
| `metadata.json` | Plasma package information and widget identity. |
| `contents/ui/main.qml` | Panel label and layout. |
| `contents/ui/ActiveApplication.qml` | Active task and application name. |
| `contents/code/Names.js` | Application name rules. |
| `scripts/package.py` | Installation file creation. |
| `tests/names.test.cjs` | Application name tests. |
| `tests/test_active_application.py` | QML tests with a test task model. |
| `.github/workflows/check.yml` | Automated checks and package creation. |
| `README.md` | Installation, use, and test instructions. |

## Make changes

Read the related files before you edit them.
Keep changes within the user request.
Keep existing user changes.
Keep the widget ID and the MIT license unless the user requests a change.
Keep generated files in `dist/`. Do not commit them.
Update the documentation when a change affects installation or use.

## Check changes

For documentation changes, run `git diff --check`.
If you change package instructions or packaged files, also run `python3 scripts/package.py`.

For code changes, run the related checks:

```sh
node tests/names.test.cjs
.venv/bin/python tests/test_active_application.py
.venv/bin/pyside6-qmlformat contents/ui/main.qml > /dev/null
.venv/bin/pyside6-qmlformat contents/ui/ActiveApplication.qml > /dev/null
python3 scripts/package.py
git diff --check
```

Use the test setup instructions in `README.md` if the Qt tools are not installed.
Add tests when a change adds behavior or corrects a defect.

The QML tests use a test task model. They do not check actual Plasma panel behavior.
Use the manual checks in `README.md` for theme, font, and monitor changes.
State which checks passed. State which checks you could not run.
Do not report actual Plasma behavior as tested unless you tested it in Plasma.

## Deliver changes

Use a short commit message that describes the change.
Commit or publish changes when the user has authorized that action.
In the final report, describe the result, the checks, and any remaining limits.
