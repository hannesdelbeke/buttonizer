import sys, os
from PySide2.QtWidgets import QApplication, QPushButton, QMenu, QAction, QDialog, QLabel, QLineEdit, \
    QMessageBox, QStyle, QMainWindow, QVBoxLayout, QWidget, QComboBox, QDockWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
import yaml
from pathlib import Path
import subprocess


CONFIG_ENV_VAR = 'BUTTONIZER_CONFIG_DIRS'
widget = None


def open_config_folder(config_folder_path):
    # Open folder in file explorer or file manager
    if os.path.isdir(config_folder_path):
        if sys.platform.startswith("win"):
            subprocess.Popen(f'explorer "{config_folder_path}"')
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", config_folder_path])
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", config_folder_path])


class MainWindow(QDockWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)

        self.setObjectName("ButtonizerMainWindow")

        # load config in same folder

        # get env var
        env_var = os.environ.get(CONFIG_ENV_VAR)
        if env_var:
            config_dirs = env_var.split(";")
        else:
            config_dirs = [os.path.dirname(__file__)]

        # find all yamls in the dirs, with 
        self.config_paths = []
        for config_dir in config_dirs:
            if os.path.isdir(config_dir):
                self.config_paths.extend(Path(config_dir).rglob('*.yaml'))

        # Open the YAML file(s)
        self.configs = []
        for config_path in self.config_paths:
            with open(config_path, 'r') as file:
                self.configs.append(yaml.safe_load(file))

        # Create the central widget and main layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Create dropdown for categories
        self.category_dropdown = QComboBox()
        self.category_dropdown.currentIndexChanged.connect(self.update_commands)
        layout.addWidget(self.category_dropdown)


        # Create command buttons container
        self.commands_container = QWidget()
        self.commands_layout = QVBoxLayout(self.commands_container)
        layout.addWidget(self.commands_container)

        layout.addStretch()

        # Create "Add Command" button
        add_command_button = QPushButton("Add Command")
        add_command_button.clicked.connect(self.add_command)
        layout.addWidget(add_command_button)

        # Add folder button
        folder_button = QPushButton(" show config")
        folder_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DirIcon))
        folder_button.setToolTip("Open Config Folder")
        folder_button.clicked.connect(self.open_config_folder)
        layout.addWidget(folder_button)

        # Set the central widget
        # self.setCentralWidget(central_widget)
        self.setWidget(central_widget)

        # Populate categories dropdown and initial commands
        self.populate_categories()
        self.update_commands()

    def open_config_folder(self):
        open_config_folder(self.config_paths[0].parent)

    @property
    def all_commands(self):
        all_configs = []
        for config in self.configs:
            all_configs.extend(config)
        return all_configs

    def populate_categories(self):
        categories = set(cmd["category"] for cmd in self.all_commands)
        self.category_dropdown.clear()
        self.category_dropdown.addItems(sorted(categories))

    def update_commands(self):
        # Clear previous command buttons
        for i in reversed(range(self.commands_layout.count())):
            self.commands_layout.itemAt(i).widget().setParent(None)

        # Get selected category
        selected_category = self.category_dropdown.currentText()

        # Add command buttons for the selected category
        for cmd in self.all_commands:
            if cmd["category"] == selected_category:
                button = QPushButton(cmd["name"])
                button.clicked.connect(lambda _=None, command=cmd["command"]: exec(command))
                self.commands_layout.addWidget(button)
                
                # Create context menu
                menu = QMenu(button)
                edit_action = QAction("Edit", button)
                edit_action.triggered.connect(lambda _=None, cmd=cmd: self.edit_command(cmd))
                delete_action = QAction("Delete", button)
                delete_action.triggered.connect(lambda _=None, cmd=cmd: self.delete_command(cmd))
                menu.addAction(edit_action)
                menu.addAction(delete_action)

                # Set context menu for button
                button.setContextMenuPolicy(Qt.CustomContextMenu)
                button.customContextMenuRequested.connect(lambda pos, button=button, menu=menu: self.show_context_menu(pos, button, menu))

                
    def show_context_menu(self, pos, button, menu):
        menu.exec_(button.mapToGlobal(pos))

    def add_command(self):

        new_command = {
            "name": "NAME",
            "category": self.category_dropdown.currentText(),
            "command": "print('2')"
        }

        if self.edit_command_user_input(new_command):
            # Add new command to config
            self.configs[0].append(new_command)  # todo add to current config, handle multiple configs
            self.save_config()
            self.update_commands()  # Update UI

    def edit_command_user_input(self, cmd):
        """
        Edits the command through mutable reference (edit the original dict for the command)
        cmd: the command to edit
        returns True if the command was edited, False if it was cancelled
        """

        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Command")

        # Create widgets
        name_label = QLabel("Name:")
        name_edit = QLineEdit(cmd["name"])
        command_label = QLabel("Command:")
        command_edit = QLineEdit(cmd["command"])

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(name_edit)
        layout.addWidget(command_label)
        layout.addWidget(command_edit)
        dialog.setLayout(layout)

        # Create OK and Cancel buttons
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)

        # Add buttons to layout
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Update command
            cmd["name"] = name_edit.text()
            cmd["command"] = command_edit.text()
            return True
        return False

    def edit_command(self, cmd):
            self.edit_command_user_input(cmd)

            # Save config
            self.save_config()

            # Update UI
            self.update_commands()

    def delete_command(self, cmd):
        # Confirm deletion
        confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete the command '{cmd['name']}'?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            # Remove command
            # self.all_commands.remove(cmd)

            # Remove command from config
            for config in self.configs:
                if cmd in config:
                    config.remove(cmd)

            # Save config
            self.save_config()

            # Update UI
            self.update_commands()

    def save_config(self):
        # Save config to all config files
        env_var = os.environ.get(CONFIG_ENV_VAR)
        if env_var:
            config_dirs = env_var.split(";")
        else:
            config_dirs = [os.path.dirname(__file__)]

        for config_dir in config_dirs:
            if os.path.isdir(config_dir):
                for config_path in Path(config_dir).rglob('*.yaml'):
                    with open(config_path, 'w') as f:
                        yaml.safe_dump(self.all_commands, f)

def show() -> MainWindow:
    global widget
    app = QApplication.instance()
    exec = 0
    if not app:
        exec = 1
        app = QApplication()
    widget = MainWindow()
    widget.show()
    if exec:
        app.exec_()
    return widget


if __name__ == '__main__':
    show()
