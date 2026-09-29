# dumb-app-name-plasmoid

A tiny Plasma 6 widget: just the active application's name, in bold.

- Uses Plasma's task model and its `AppName` role, not the window/document title.
- Follows the panel's text color and system font, including live theme changes.
  Only the font weight is overridden.
- Transparent background, one line, no icons or window buttons.
- Tracks the active application across all monitors. Screen, virtual desktop,
  and activity filters are disabled.
- Long names are elided on the right; preferred width is capped at 12 grid units
  (about 216 pixels with typical font settings).
- Shows an empty label when there is no active task or its application name is
  unavailable. It does not retain a stale name or substitute a document title.

## Name substitutions

These case-sensitive regular expressions match the **whole application name**:

| Name pattern | Label |
| --- | --- |
| `Telegram Desktop` | Telegram |
| `Gimp-.*` | Gimp |
| `soffice\.bin` | LibreOffice |
| `Spotify.*` | Spotify |
| `Kate.*` | Kate |

Unknown names are preserved. Edit `contents/code/Names.js` to change the rules.
Names come from Plasma's application metadata; a name already supplied as
`LibreOffice Writer`, for example, stays `LibreOffice Writer`.

## Install on Arch Linux / Plasma 6

No compilation or custom C++ plugin is needed. In a Plasma 6 installation,
`kpackagetool6` is supplied by the `kpackage` package.

```sh
git clone https://github.com/peterhass/dumb-app-name-plasmoid.git
cd dumb-app-name-plasmoid
kpackagetool6 --type Plasma/Applet --install .
```

Then open your panel's **Add Widgets** dialog, search for
**dumb-app-name-plasmoid**, and add it. A horizontal panel is the intended layout.
If it does not appear immediately, log out and back in.

To update an existing installation:

```sh
git pull --ff-only
kpackagetool6 --type Plasma/Applet --upgrade .
```

Log out and back in after updating so Plasma reloads the QML.

To remove:

```sh
kpackagetool6 --type Plasma/Applet --remove com.github.peterhass.dumb-app-name-plasmoid
```

## Build an installable file

```sh
python3 scripts/package.py
```

This writes `dist/dumb-app-name-plasmoid.plasmoid`. Install it with:

```sh
kpackagetool6 --type Plasma/Applet --install dist/dumb-app-name-plasmoid.plasmoid
```

## Checks

```sh
node tests/names.test.cjs
# Optional development dependency; not needed to use the widget:
python3 -m venv .venv
.venv/bin/pip install PySide6-Essentials
.venv/bin/python tests/test_active_application.py
```

The Qt tests load the production tracking QML with a mock Plasma task model.
They cover focus changes, same-index name changes, resets, missing names, and
disabled filters. They do not substitute for running the widget in Plasma.

Before considering a release tested on your system:

1. Switch between Firefox and Dolphin, including windows on another monitor.
2. Check each substituted application name.
3. Switch between light and dark Plasma themes while the widget is visible;
   change the system font and confirm the bold label follows it.
4. Focus the desktop, close the active window, and switch virtual desktops.
5. Use an application with a long name to verify truncation.

## License

MIT. See [LICENSE](LICENSE).
