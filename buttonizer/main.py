import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton
from PySide2.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)

        # load config in same folder

        # Open the YAML file
        import yaml
        with open('sample_config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

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

    def populate_categories(self):
        categories = set(cmd["category"] for cmd in self.config)
        self.category_dropdown.addItems(sorted(categories))

    def update_commands(self):
        # Clear previous command buttons
        for i in reversed(range(self.commands_layout.count())):
            self.commands_layout.itemAt(i).widget().setParent(None)

        # Get selected category
        selected_category = self.category_dropdown.currentText()

        # Add command buttons for the selected category
        for cmd in self.config:
            if cmd["category"] == selected_category:
                button = QPushButton(cmd["name"])
                button.clicked.connect(lambda _, command=cmd["command"]: exec(command))
                self.commands_layout.addWidget(button)


app = QApplication.instance()
exec = 0
if not app:
    exec = 1
    app = QApplication()
widget = MainWindow()
widget.show()
if exec:
    app.exec_()