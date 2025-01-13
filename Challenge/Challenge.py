import os
import pandas as pd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Logging Configuration
LOG_FILE = "luminovo_sync.log"

def log_message(message):
    """Log messages to a file."""
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")
    print(message)

def load_excel(file_path):
    """Load the Excel file containing stock data."""
    log_message("Checking if the file exists...")
    # Checking if the file exists
    if not os.path.exists(file_path):
        log_message(f"Error: File '{file_path}' does not exist. Skipping this run.")
        return None

    # Attempt to read the file
    try:
        log_message(f"Loading data from {file_path}.")
        dataframe = pd.read_excel(file_path)

        # Checking if required columns are present
        required_columns = ["Internal Part Number", "Available Stock", "Total Stock", "Unit Price"]
        missing_columns = [col for col in required_columns if col not in dataframe.columns]
        if missing_columns:
            log_message(f"Error: Missing required columns: {missing_columns}. Skipping this run.")
            return None

        return dataframe
    except Exception as e:
        log_message(f"Error loading file '{file_path}': {e}. Skipping this run.")
        return None

def transform_data(dataframe):
    """Transform the dataframe into a mock JSON payload format."""
    payload = []
    for _, row in dataframe.iterrows():
        payload.append({
            "availability": {
                "available_stock": row.get("Available Stock", 0),
                "total_stock": row.get("Total Stock", 0)
            },
            "part": {
                "internal_part_number": str(row.get("Internal Part Number", "N/A"))
            },
            "prices": [{
                "unit_price": row.get("Unit Price", 0.0),
                "currency": "EUR"
            }],
            "supplier": {
                "supplier_number": "SUP12345"
            },
            "packaging": "Bag",
            "price_type": "Standard",
            "unit_of_measurement": {
                "quantity": 1,
                "unit": "Piece"
            },
            "import_context": "Daily stock update"
        })
    log_message("Data transformed successfully.")
    return payload

def mock_send_to_api(payload):
    """Mock sending data to the API."""
    log_message("Mock: Preparing to send data to the API...")
    log_message(f"Mock: Payload contains {len(payload)} records.")
    log_message("Mock: Data 'sent' successfully. (No actual API call was made)")

def sync_stock(scheduler):
    """Main function to handle stock synchronization."""
    log_message("Sync stock job started.")
    file_path = "Availability.xlsx"  # Ensure the file is in the working directory
    log_message(f"Current working directory: {os.getcwd()}")

    # Check if the file exists before proceeding
    dataframe = load_excel(file_path)
    if dataframe is None:
        log_message(f"Sync stock job skipped due to missing or invalid file '{file_path}'.")
        return  # Skip the current job run if the file is missing or invalid

    try:
        payload = transform_data(dataframe)
        mock_send_to_api(payload)
    except Exception as e:
        log_message(f"An error occurred during job execution: {e}")

if __name__ == "__main__":
    log_message("Starting the script...")
    scheduler = BackgroundScheduler()
    # Schedule the job every minute to allow enough time for processing
    scheduler.add_job(sync_stock, "cron", hour=2, args=[scheduler], max_instances=1)
    #scheduler.add_job(sync_stock, "interval, minutes=1, args=[scheduler, max_instances=1])
    scheduler.start()
    log_message("Stock sync scheduler started. Press Ctrl+C to exit.")

    try:
        while True:
            pass  # Keep the script running
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        log_message("Scheduler stopped.")
