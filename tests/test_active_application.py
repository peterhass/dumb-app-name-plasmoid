"""Exercise production QML against a mock task model using a real Qt engine.

This checks reactive QML behavior, not KDE backend or panel integration.
Run with PySide6-Essentials installed and QT_QPA_PLATFORM=offscreen.
"""
import os
from enum import IntEnum
from pathlib import Path
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import (QAbstractListModel, QModelIndex, QObject, Property,
                            QEnum, Signal, Qt, QUrl)
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlComponent, QQmlEngine, qmlRegisterType, qmlRegisterUncreatableType


class AbstractTasksModel(QObject):
    class AdditionalRoles(IntEnum):
        AppName = int(Qt.UserRole) + 2
    QEnum(AdditionalRoles)


class TasksModel(QAbstractListModel):
    class GroupMode(IntEnum):
        GroupDisabled = 0
    QEnum(GroupMode)
    activeTaskChanged = Signal()
    instances = []

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rows = []
        self.active_row = -1
        self.instances.append(self)
        self.settings = {}

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.rows)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.rows):
            return None
        if role == AbstractTasksModel.AdditionalRoles.AppName:
            return self.rows[index.row()]
        return None

    @Property(QModelIndex, notify=activeTaskChanged)
    def activeTask(self):
        return self.index(self.active_row, 0) if self.active_row >= 0 else QModelIndex()

    def setting(key, value_type):
        return Property(value_type, lambda self: self.settings.get(key, False),
                        lambda self, value: self.settings.__setitem__(key, value))

    groupMode = setting("groupMode", int)
    filterByScreen = setting("filterByScreen", bool)
    filterByVirtualDesktop = setting("filterByVirtualDesktop", bool)
    filterByActivity = setting("filterByActivity", bool)

    def reset(self, names, active=-1):
        self.beginResetModel()
        self.rows = list(names)
        self.active_row = active
        self.endResetModel()
        self.activeTaskChanged.emit()

    def activate(self, row):
        self.active_row = row
        self.activeTaskChanged.emit()

    def rename(self, row, name):
        self.rows[row] = name
        self.dataChanged.emit(self.index(row, 0), self.index(row, 0),
                              [AbstractTasksModel.AdditionalRoles.AppName])


app = QGuiApplication([])
qmlRegisterType(TasksModel, "org.kde.taskmanager", 1, 0, "TasksModel")
qmlRegisterUncreatableType(AbstractTasksModel, "org.kde.taskmanager", 1, 0,
                          "AbstractTasksModel", "Enums only")


class ActiveApplicationTests(unittest.TestCase):
    def setUp(self):
        self.engine = QQmlEngine()
        self.component = QQmlComponent(self.engine)
        path = Path(__file__).resolve().parents[1] / "contents/ui/ActiveApplication.qml"
        self.component.loadUrl(QUrl.fromLocalFile(str(path)))
        self.assertFalse(self.component.isError(), str(self.component.errors()))
        self.tracker = self.component.create()
        self.assertIsNotNone(self.tracker, str(self.component.errors()))
        self.model = TasksModel.instances[-1]

    def tearDown(self):
        self.tracker.deleteLater()
        self.engine.deleteLater()
        app.processEvents()

    def name(self):
        app.processEvents()
        return self.tracker.property("name")

    def test_focus_changes_and_no_active_window(self):
        self.assertEqual(self.name(), "")
        self.model.reset(["Firefox", "Dolphin"], active=0)
        self.assertEqual(self.name(), "Firefox")
        self.model.activate(1)
        self.assertEqual(self.name(), "Dolphin")
        self.model.activate(-1)
        self.assertEqual(self.name(), "")

    def test_same_active_index_name_changes(self):
        self.model.reset(["Telegram Desktop"], active=0)
        self.assertEqual(self.name(), "Telegram")
        self.model.rename(0, "Gimp-3.0")
        self.assertEqual(self.name(), "Gimp")
        self.model.rename(0, "soffice.bin")
        self.assertEqual(self.name(), "LibreOffice")
        self.model.rename(0, "")
        self.assertEqual(self.name(), "")

    def test_model_reset_does_not_leave_stale_name(self):
        self.model.reset(["Kate project"], active=0)
        self.assertEqual(self.name(), "Kate")
        self.model.reset([])
        self.assertEqual(self.name(), "")
        self.model.reset(["Spotify Premium"], active=0)
        self.assertEqual(self.name(), "Spotify")

    def test_task_filters_are_disabled(self):
        for setting in ("filterByScreen", "filterByVirtualDesktop", "filterByActivity"):
            self.assertIs(self.model.settings[setting], False)
        self.assertEqual(self.model.settings["groupMode"], 0)


if __name__ == "__main__":
    unittest.main()
