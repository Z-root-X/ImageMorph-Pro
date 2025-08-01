# src/ui/main_window.py
import os
import sys

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from src.core.converter import convert_image


# Worker thread for image conversion
class ConversionWorker(QThread):
    progress_updated = pyqtSignal(int)
    file_converted = pyqtSignal(str, str)
    conversion_finished = pyqtSignal(bool, list)

    def __init__(self, files, output_format, output_folder):
        super().__init__()
        self.files = files
        self.output_format = output_format
        self.output_folder = output_folder

    def run(self):
        all_success = True
        error_messages = []
        total_files = len(self.files)

        for i, input_path in enumerate(self.files):
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_filename = f"{base_name}.{self.output_format.lower()}"
            output_path = os.path.join(self.output_folder, output_filename)

            self.file_converted.emit(os.path.basename(input_path), f"Converting {i+1}/{total_files}...")

            success, message = convert_image(input_path, self.output_format, output_path)
            if not success:
                all_success = False
                error_messages.append(f"Failed to convert {os.path.basename(input_path)}: {message}")

            self.progress_updated.emit(int(((i + 1) / total_files) * 100))

        self.conversion_finished.emit(all_success, error_messages)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageMorph Pro")
        self.setGeometry(100, 100, 600, 280) # Slightly larger window to accommodate progress bar
        self.selected_files = [] # Initialize selected_files

        # Set a dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #f0f0f0;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50; /* Green */
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                color: #f0f0f0;
            }
            QComboBox {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                color: #f0f0f0;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                /* image: url(down_arrow.png); */ /* Placeholder for a custom arrow icon */
            }
            QStatusBar {
                background-color: #3c3c3c;
                color: #f0f0f0;
                border-top: 1px solid #555;
            }
            QMenuBar {
                background-color: #3c3c3c;
                color: #f0f0f0;
            }
            QMenuBar::item:selected {
                background-color: #555;
            }
            QMenu {
                background-color: #3c3c3c;
                color: #f0f0f0;
                border: 1px solid #555;
            }
            QMenu::item:selected {
                background-color: #555;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #3c3c3c;
                color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 5px;
            }
        """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20) # Add some padding
        main_layout.setSpacing(15) # Increase spacing between elements

        # Title Label
        title_label = QLabel("ImageMorph Pro")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold)) # Larger, bold font
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # File selection layout
        file_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("No files selected...")
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.path_edit)
        file_layout.addWidget(self.browse_button)
        main_layout.addLayout(file_layout)

        # Format selection and conversion layout
        action_layout = QHBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPG", "WEBP", "BMP", "GIF"])
        self.format_combo.setMinimumWidth(150) # Give combo box a minimum width
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_file)
        action_layout.addWidget(self.format_combo)
        action_layout.addWidget(self.convert_button)
        main_layout.addLayout(action_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide() # Hide initially
        main_layout.addWidget(self.progress_bar)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Menu bar
        self._create_menu_bar()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def browse_file(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Image(s)", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp);;All Files (*)"
        )
        if files:
            self.selected_files = files
            if len(files) == 1:
                self.path_edit.setText(files[0])
                self.status_bar.showMessage(f"Selected: {os.path.basename(files[0])}")
            else:
                self.path_edit.setText(f"{len(files)} files selected")
                self.status_bar.showMessage(f"{len(files)} files selected for conversion.")
        else:
            self.selected_files = []
            self.path_edit.clear()
            self.status_bar.showMessage("Ready")

    def convert_file(self):
        if not self.selected_files:
            self.status_bar.showMessage("Error: Please select at least one input file first.")
            return

        output_format = self.format_combo.currentText()

        if len(self.selected_files) == 1:
            input_path = self.selected_files[0]
            suggested_filename = os.path.splitext(os.path.basename(input_path))[0] + f".{output_format.lower()}"
            output_path, _ = QFileDialog.getSaveFileName(
                self, "Save As", suggested_filename, f"{output_format} Files (*.{output_format.lower()});;All Files (*)"
            )
            if output_path:
                self.status_bar.showMessage("Converting...")
                self.set_ui_enabled(False)
                self.progress_bar.show()
                self.progress_bar.setValue(0)

                # Single file conversion (still use worker for consistency and future expansion)
                self.worker = ConversionWorker([input_path], output_format, os.path.dirname(output_path))
                self.worker.progress_updated.connect(self.update_progress)
                self.worker.file_converted.connect(self.update_file_status)
                self.worker.conversion_finished.connect(
                    lambda success, errors: self.conversion_complete(success, errors, output_path)
                )
                self.worker.start()
            else:
                self.status_bar.showMessage("Conversion cancelled.")
        else:
            output_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
            if output_folder:
                self.status_bar.showMessage(f"Converting {len(self.selected_files)} images...")
                self.set_ui_enabled(False)
                self.progress_bar.show()
                self.progress_bar.setValue(0)

                self.worker = ConversionWorker(self.selected_files, output_format, output_folder)
                self.worker.progress_updated.connect(self.update_progress)
                self.worker.file_converted.connect(self.update_file_status)
                self.worker.conversion_finished.connect(self.conversion_complete)
                self.worker.start()
            else:
                self.status_bar.showMessage("Conversion cancelled.")

    def set_ui_enabled(self, enabled):
        self.browse_button.setEnabled(enabled)
        self.format_combo.setEnabled(enabled)
        self.convert_button.setEnabled(enabled)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_file_status(self, filename, message):
        self.status_bar.showMessage(f"{message} {filename}")

    def conversion_complete(self, success, errors, single_file_output_path=None):
        self.set_ui_enabled(True)
        self.progress_bar.hide()
        self.progress_bar.setValue(0)

        if success:
            if single_file_output_path:
                QMessageBox.information(self, "Success",
                                        f"Successfully converted.\nSaved to: {single_file_output_path}")
            else:
                QMessageBox.information(self, "Success", "All selected images converted successfully!")
            self.status_bar.showMessage("Ready")
        else:
            self.status_bar.showMessage("Conversion completed with errors.")
            QMessageBox.critical(self, "Conversion Errors", "\n".join(errors))

    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About ImageMorph Pro",
            "ImageMorph Pro\nVersion 1.0\nDeveloped by Zihad Hasan"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
