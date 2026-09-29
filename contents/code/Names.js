// SPDX-License-Identifier: MIT
.pragma library

// Match the full application name.
var substitutions = [
    [/^Telegram Desktop$/, "Telegram"],
    [/^Gimp-.*$/, "Gimp"],
    [/^soffice\.bin$/, "LibreOffice"],
    [/^Spotify.*$/, "Spotify"],
    [/^Kate.*$/, "Kate"]
];

function substitute(name) {
    if (name === undefined || name === null) {
        return "";
    }

    var value = String(name).trim();
    for (var i = 0; i < substitutions.length; ++i) {
        if (substitutions[i][0].test(value)) {
            return substitutions[i][1];
        }
    }
    return value;
}
