# Luminovo Challenge Script

## Overview

- Transforms stock data from Excel format into API-compliant JSON.
- Mock-sends data to Luminovo’s API for testing purposes.
- Logs operations and errors for easier debugging.
- Supports scheduled execution using Python APScheduler.

---

## File Structure

- **`Challenge.py`**: The main script for data transformation and mock API integration.
- **`Availability.xlsx`**: Sample Excel file containing stock data (to be replaced with daily exports).
- **`README.md`**: Documentation for installation and usage.
- **`luminovo_sync.log`**: Log file for debugging and tracking script execution.

---

## Prerequisites

### 1. **Python**:
- Ensure Python 3.8+ is installed on your system.
- Download Python from [python.org](https://www.python.org/).

### 2. **Dependencies**:
- Install required Python libraries:
    ```bash
    pip install pandas openpyxl apscheduler
    ```

### 3. **Files**:
- Ensure `Challenge.py` and `Availability.xlsx` are in the same directory.

### 4. **Environment Variable**:
- (Optional) Set `LUMINOVO_AUTH_TOKEN` if real API authentication is implemented.

---

## Setup Instructions

### 1. **Running the Script**:
- Run the script manually for testing:
    ```bash
    python Challenge.py
    ```
- Check `luminovo_sync.log` for logs and errors.

### 2. **Automated Scheduling**:
Use Task Scheduler (Windows):
1. Open Task Scheduler (`Win + R`, type `taskschd.msc`, press Enter).
2. Create a new task:
    - Name: "Luminovo Stock Sync"
    - Trigger: Daily at `2:00 AM`.The interval of syncing can be changed in the code.
    - Action: Start a program.
    - Program/script: Path to `python.exe` (e.g., `C:\Python39\python.exe`).
    - Add arguments: Full path to `Challenge.py` (e.g., `C:\Scripts\Challenge.py`).

### 3. **Testing the Schedule**:
- Verify the script runs correctly and generates logs.

---

## Troubleshooting

- **File Not Found**:
    - Ensure `Availability.xlsx` exists in the same directory as the script.

- **Missing Columns**:
    - Ensure the following columns are present in the Excel file:
        - `Internal Part Number`
        - `Available Stock`
        - `Total Stock`
        - `Unit Price`

- **Python Errors**:
    - Verify Python and all required libraries are installed.

- **Scheduler Issues**:
    - Check Task Scheduler logs for errors.

---

## Future Enhancements

- Replace `mock_send_to_api` with real API calls using authentication.
- Add email notifications for job completion or failure.

---


