import sys, os
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton
from PySide2.QtCore import Qt
import yaml
from pathlib import Path


CONFIG_ENV_VAR = 'BUTTONIZER_CONFIG_DIRS'
widget = None


class MainWindow(QMainWindow):
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
        config_paths = []
        for config_dir in config_dirs:
            if os.path.isdir(config_dir):
                config_paths.extend(Path(config_dir).rglob('*.yaml'))

        # Open the YAML file(s)
        self.configs = []
        for config_path in config_paths:
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

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Populate categories dropdown and initial commands
        self.populate_categories()
        self.update_commands()

    @property
    def all_commands(self):
        all_configs = []
        for config in self.configs:
            all_configs.extend(config)
        return all_configs

    def populate_categories(self):
        categories = set(cmd["category"] for cmd in self.all_commands)
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