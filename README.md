# Document Processing

## Prerequisites

- **Windows**: Install `gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe` from [this link](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe). Check envrionment variables for ../GTK3-Runtime Win64/bin should be in your path. Restart the system if an error occurs.
- **Linux**: Follow the installation steps for WeasyPrint on [Linux](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#linux).
- **macOS**: Install WeasyPrint using Homebrew with the command: `brew install weasyprint`.

## Installation

1. Install the required Python libraries using pip:

   ```bash
   pip install -r requirements.txt
   ```

2. Optionally, create and activate a virtual environment:

  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  venv\Scripts\activate    # Windows
   ```
## Usage
1. Run the script using Python
  ```bash
  python main.py
  ```
2. The script will open an interface to upload a JPG or PNG image for processing.

After processing, the JSON output file will be saved as feed.json, and the resulting text file will be saved as results.txt.
