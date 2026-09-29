// SPDX-License-Identifier: MIT
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.components as PlasmaComponents
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: root
    preferredRepresentation: fullRepresentation
    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground

    readonly property real padding: Kirigami.Units.smallSpacing
    readonly property real maximumLabelWidth: Kirigami.Units.gridUnit * 12
    readonly property real naturalWidth: Math.min(label.implicitWidth, maximumLabelWidth)

    Layout.minimumWidth: Kirigami.Units.gridUnit * 2
    Layout.preferredWidth: Math.max(Layout.minimumWidth, naturalWidth)
    Layout.maximumWidth: Layout.preferredWidth
    Layout.minimumHeight: label.implicitHeight + padding * 2
    Layout.preferredHeight: Layout.minimumHeight

    ActiveApplication { id: activeApplication }

    fullRepresentation: PlasmaComponents.Label {
        id: label
        text: activeApplication.name
        textFormat: Text.PlainText
        font.bold: true
        // PlasmaComponents.Label inherits the panel's Kirigami theme and
        // system font. Keep all font attributes except weight at defaults.
        elide: Text.ElideRight
        maximumLineCount: 1
        wrapMode: Text.NoWrap
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignLeft
        leftPadding: root.padding
        rightPadding: root.padding
    }
}
