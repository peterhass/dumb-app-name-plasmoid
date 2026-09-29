# Instructions for coding agents

## Language

- Use Simplified Technical English in user messages, documentation, comments, commit messages, and widget text. Use short, active sentences and consistent terms. Keep API names, commands, paths, legal text, and SPDX identifiers exact.

## Widget constraints

- This is a Plasma 6 QML widget. Do not add a C++ plugin or external process unless requested. Keep the widget ID in `metadata.json` and the MIT license unless requested to change them.
- `contents/ui/ActiveApplication.qml` reads `TaskManager.AbstractTasksModel.AppName` from the active task. Keep task grouping disabled and screen, virtual desktop, and activity filters off. Model data can change without a new active index; keep the label updated on model changes. Do not use window or document titles as application names.
- Keep name substitutions in `contents/code/Names.js`. Match the full application name with case-sensitive rules.
- `contents/ui/main.qml` uses `PlasmaComponents.Label` for the panel text color and system font. Keep theme and font updates live; change only the font weight to bold. Keep the background transparent, the text plain and on one line, and the right-end ellipsis. Do not add icons or window buttons. Show an empty label when no name is available, except for the text placeholder in edit mode.

## Checks and packaging

- Run `node tests/names.test.cjs` for name rules. Run `.venv/bin/python tests/test_active_application.py` for task-model changes. These tests use a substitute task model, not the installed Plasma model or panel. They run without a display server.
- To set up Qt test tools: `python3 -m venv .venv` and `.venv/bin/pip install PySide6-Essentials==6.11.2`. Parse both QML files with `.venv/bin/pyside6-qmlformat contents/ui/main.qml > /dev/null` and `.venv/bin/pyside6-qmlformat contents/ui/ActiveApplication.qml > /dev/null`.
- On Arch Linux with Plasma 6, run `/usr/lib/qt6/bin/qmllint contents/ui/main.qml contents/ui/ActiveApplication.qml`. Use this Qt 6 path: the unqualified command can be Qt 5. The type check needs installed Plasma QML modules and does not run in CI.
- Run `python3 scripts/package.py` when package instructions or packaged files change. It packages `metadata.json`, `LICENSE`, `README.md`, and all files under `contents/` into `dist/dumb-app-name-plasmoid.plasmoid`. `dist/` is ignored; do not commit its contents.
- Run `git diff --check` for changes. For theme, font, and monitor behavior, use the manual checks in `README.md`. Do not report Plasma behavior as tested unless you tested it in Plasma. State which checks ran and which could not run.
