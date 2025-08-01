# ImageMorph Pro

ImageMorph Pro is a simple, open-source desktop application for converting image formats. It now supports batch conversion, a responsive dark theme, and a more fluid user experience.

## Features

*   Convert images between popular formats: PNG, JPG, WEBP, BMP, GIF.
*   **Batch conversion:** Convert multiple images at once.
*   **Responsive UI:** User interface remains responsive during long conversions.
*   **Dark Theme:** Modern and attractive dark mode interface.
*   Error handling for robust conversions.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Z-root-X/ImageMorph-Pro.git
    cd ImageMorphPro
    ```
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Activate your virtual environment (if you created one):
    ```bash
    source venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
2.  Run the application:
    ```bash
    python main.py
    ```
3.  Click "Browse..." to select one or more image files.
4.  Choose the desired output format from the dropdown menu.
5.  Click "Convert". If multiple files are selected, you will be prompted to choose a destination folder. If a single file is selected, you will choose the output file name and location.

## Development

### Running Tests

To run the unit tests, first install the development dependencies:

```bash
pip install -r requirements-dev.txt
pytest
```

### Linting

To check code style and quality using Ruff:

```bash
pip install -r requirements-dev.txt
ruff check .
```

## Building Executable

To create a standalone executable using PyInstaller:

```bash
pip install -r requirements-dev.txt
pyinstaller --onefile --windowed --name "ImageMorph Pro" main.py
```

The executable will be found in the `dist/` directory.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue. Ensure your code adheres to the project's style guidelines (checked by Ruff) and that all tests pass.