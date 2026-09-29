// SPDX-License-Identifier: MIT
import QtQml
import org.kde.taskmanager as TaskManager
import "../code/Names.js" as Names

QtObject {
    id: root

    // Update the name binding when model data changes.
    // The active QModelIndex can stay the same when the name changes.
    property int modelRevision: 0
    readonly property string name: {
        const revision = modelRevision;
        if (!tasksModel) {
            return "";
        }
        return Names.substitute(tasksModel.data(tasksModel.activeTask,
                                               TaskManager.AbstractTasksModel.AppName));
    }

    property TaskManager.TasksModel tasksModel: TaskManager.TasksModel {
        groupMode: TaskManager.TasksModel.GroupDisabled
        // Include tasks from all monitors, virtual desktops, and activities.
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
