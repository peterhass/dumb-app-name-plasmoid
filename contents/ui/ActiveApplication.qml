// SPDX-License-Identifier: MIT
import QtQml
import org.kde.taskmanager as TaskManager
import "../code/Names.js" as Names

QtObject {
    id: root

    // data() is a method, so explicitly invalidate the binding when model
    // data changes even if the active QModelIndex itself stays the same.
    property int modelRevision: 0
    readonly property string name: {
        const revision = modelRevision;
        if (!tasksModel) {
            return "";
        }
        return Names.substitute(tasksModel.data(tasksModel.activeTask,
                                               TaskManager.AbstractTasksModel.AppName));
    }

    property QtObject tasksModel: TaskManager.TasksModel {
        groupMode: TaskManager.TasksModel.GroupDisabled
        // The active window may be on any monitor, desktop, or activity.
        filterByScreen: false
        filterByVirtualDesktop: false
        filterByActivity: false
    }

    property QtObject modelConnections: Connections {
        target: root.tasksModel
        function onDataChanged() { root.modelRevision += 1; }
        function onModelReset() { root.modelRevision += 1; }
        function onRowsInserted() { root.modelRevision += 1; }
        function onRowsRemoved() { root.modelRevision += 1; }
    }
}
