// Test the widget JavaScript. Remove the pragma that only QML supports.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../contents/code/Names.js'), 'utf8');
const context = vm.createContext({});
vm.runInContext(source.replace(/^\.pragma library\s*$/m, ''), context);
const cases = [
    ['Telegram Desktop', 'Telegram'], ['Gimp-3.0', 'Gimp'],
    ['soffice.bin', 'LibreOffice'], ['Spotify Premium', 'Spotify'],
    ['Kate — project', 'Kate'], ['Firefox', 'Firefox'], ['Dolphin', 'Dolphin'],
    ['Spotify', 'Spotify'], ['Kate', 'Kate'], ['Gimp', 'Gimp'],
    ['My Spotify App', 'My Spotify App'], ['sofficeXbin', 'sofficeXbin'],
    ['Telegram Desktop Beta', 'Telegram Desktop Beta'],
    ['<b>Firefox</b>', '<b>Firefox</b>'], ['  Dolphin  ', 'Dolphin'],
    ['', ''], [null, ''], [undefined, '']
];
for (const [input, expected] of cases) {
    assert.equal(context.substitute(input), expected, `Input: ${input}`);
}
console.log(`${cases.length} application-name cases passed`);
