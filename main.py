import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QPushButton
from PySide2.QtCore import Qt

# Sample configuration file content
config = [
    {"name": "Command 1", "category": "Category A", "command": "print('Command 1 executed')"},
    {"name": "Command 2", "category": "Category A", "command": "print('Command 2 executed')"},
    {"name": "Command 3", "category": "Category B", "command": "print('Command 3 executed')"},
    {"name": "Command 4", "category": "Category B", "command": "print('Command 4 executed')"},
]

class MainWindow(QMainWindow):
    def __init__(self, parent, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)

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
        categories = set(cmd["category"] for cmd in config)
        self.category_dropdown.addItems(sorted(categories))

    def update_commands(self):
        # Clear previous command buttons
        for i in reversed(range(self.commands_layout.count())):
            self.commands_layout.itemAt(i).widget().setParent(None)

        # Get selected category
        selected_category = self.category_dropdown.currentText()

        # Add command buttons for the selected category
        for cmd in config:
            if cmd["category"] == selected_category:
                button = QPushButton(cmd["name"])
                button.clicked.connect(lambda _, command=cmd["command"]: exec(command))
                self.commands_layout.addWidget(button)
                
                
MainWindow(QApplication.instance().blender_widget).show()
